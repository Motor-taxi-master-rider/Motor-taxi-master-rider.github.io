---
layout: post
title: Python垃圾处理机制
tags:
- Gc
- Memory_management
categories:
- Python
description: note of python garbage collections documents.
---


# Description
本文环境为python3.6。与c中拥有的malloc和free不同，python中的内存是编译器自动完成，因此我们并不需要时刻关心内存的使用情况。在[Things you need to know about garbage collection in Python](https://rushter.com/blog/python-garbage-collector/)一文中给我们详细介绍了python gc的具体实现及细节，本文主要参考该博客来对python垃圾处理机制做一些总结。

# 内存管理
在python中小于512k的对象是会在内存中缓存的，这就导致小于256的整形及一些短字符串在程序中实际共享了同一个内存地址。像这样，python为了提高对内存操作的效率及减少碎片，在通用内存分配器上假设了一个特殊的管理器————`PyMalloc`。在[cpython](https://github.com/python/cpython/blob/ad051cbce1360ad3055a048506c09bc2a5442474/Objects/obmalloc.c#L534)中，内存模型被形容为大致如下：

```
_____   ______   ______       ________
[ int ] [ dict ] [ list ] ... [ string ]       Python core         |
+3 | <----- Object-specific memory -----> | <-- Non-object memory --> |
_______________________________       |                           |
[   Python's object allocator   ]      |                           |
+2 | ####### Object memory ####### | <------ Internal buffers ------> |
______________________________________________________________    |
[          Python's raw memory allocator (PyMem_ API)          ]   |
+1 | <----- Python memory (under PyMem manager's control) ------> |   |
__________________________________________________________________
[    Underlying general-purpose allocator (ex: C library malloc)   ]
0 | <------ Virtual memory allocated for the python process -------> |
=========================================================================
_______________________________________________________________________
[                OS-specific Virtual Memory Manager (VMM)               ]
-1 | <--- Kernel dynamic storage allocation & management (page-based) ---> |
__________________________________   __________________________________
[                                  ] [                                  ]
-2 | <-- Physical memory: ROM/RAM --> | | <-- Secondary storage (swap) --> |
```

python中占用内存较大的对象会被分配到标准的c内存分配器，小对象分配器则由三个级别的抽象构成`Arena`、`Pool`、`Block`。

## Block
Block（块）是固定大小（8-512k）的内存块。为了方便起见，这些块被分为64类：

<table><thead><tr><th>Request in bytes</th><th>Size of allocated block</th><th>size class idx</th></tr></thead><tbody><tr><td>1-8</td><td>8</td><td>0</td></tr><tr><td>9-16</td><td>16</td><td>1</td></tr><tr><td>17-24</td><td>24</td><td>2</td></tr><tr><td>25-32</td><td>32</td><td>3</td></tr><tr><td>33-40</td><td>40</td><td>4</td></tr><tr><td>41-48</td><td>48</td><td>5</td></tr><tr><td>...</td><td>...</td><td>...</td></tr><tr><td>505-512</td><td>512</td><td>63</td></tr></tbody></table>

## Pool
Pool（池）是相同大小Block（块）的集合。通常来说，池的大小等于内存页的大小。固定块的大小能减少内存碎片的产生————当一个对象被销毁的时候，内存管理器能轻松地将相同大小的对象装载入块中。

在cpython中，池被定义为如下结构：

```c
/* Pool for small blocks. */
struct pool_header {
    union { block *_padding;
            uint count; } ref;          /* number of allocated blocks    */
    block *freeblock;                   /* pool's free list head         */
    struct pool_header *nextpool;       /* next pool of this size class  */
    struct pool_header *prevpool;       /* previous pool       ""        */
    uint arenaindex;                    /* index into arenas of base adr */
    uint szidx;                         /* block size class index        */
    uint nextoffset;                    /* bytes to virgin block         */
    uint maxnextoffset;                 /* largest valid nextoffset      */
};
```

池使用的是双向链表的结构，`nextpool`和`prevpool`字段指向链表节点。`szidx`字段保存了上文提到的该池的大小类别的序号（size class index），而`ref.count`字段则储存了被占用了的块的数量。`arenaindex`储存了该池在所在的内存空间的序号。对于`freeblock`则是这么解释的：

```
pool->freeblock points to the start of a singly-linked list of free blocks within the pool.  
When a block is freed, it's inserted at the front of its pool's freeblock list.  Note
that the available blocks in a pool are *not* linked all together when a pool
is initialized.  Instead only "the first two" (lowest addresses) blocks are
set up, returning the first such block, and setting pool->freeblock to a
one-block list holding the second such block.  This is consistent with that
pymalloc strives at all levels (arena, pool, and block) never to touch a piece
of memory until it's actually needed.

So long as a pool is in the used state, we're certain there *is* a block
available for allocating, and pool->freeblock is not NULL.  If pool->freeblock
points to the end of the free list before we've carved the entire pool into
blocks, that means we simply haven't yet gotten to one of the higher-address
blocks.  The offset from the pool_header to the start of "the next" virgin
block is stored in the pool_header nextoffset member, and the largest value
of nextoffset that makes sense is stored in the maxnextoffset member when a
pool is initialized.  All the blocks in a pool have been passed out at least
once when and only when nextoffset > maxnextoffset.
```

大概就是说，`freeblock`字段指向了一个单项链表，这个链表连接了该池中的一部分可用的块。之所以说是‘一部分’是因为在初始化池的时候系统只会给前两给内存块分配内存，这样使得只有当需要分配新内存的时候才会让池占用新的块空间，节省了内存的消耗。初始化池的时会进行的另一个操作是设置`maxnextoffset`字段，即内存指针最大偏移量。当需要拓展新的块空间时，通过`szidx`及`nextoffset`字段计算出新块所占用的内存地址区域并分配内存。最后，当`nextoffset`大于`maxnextoffset`时，整个池的就满了。

为了更有效地进行池的管理，python引入了`usedpools`数组来储存各个**size class**的块：

<img src="https://motor-taxi-master-rider.github.io/assets/img/usedpools.svg"  title="usedpools示例"/>

值得注意的是，块和池并不是直接分配内存，它们所分配的内存来自于其所在的Arena（内存空间）。

## Arena
Arena（内存空间）是由64个池组成的在堆上的256k的空间，同样也是双向链表。它的结构如下：

```code
struct arena_object {
    uintptr_t address;
    block* pool_address;
    uint nfreepools;
    uint ntotalpools;
    struct pool_header* freepools;
    struct arena_object* nextarena;
    struct arena_object* prevarena;
};
```

其中`ntotalpools`和`nfreepools`储存了内存空间上可用池的信息。`freepools`指向一个可用池的链表。

# python中的垃圾处理
python中的垃圾处理机制由两部分组成：

1. 引用计数（*reference counting*）
2. 分代垃圾收集器（*generational garbage collector*）

引用计数是我们无法染指只能了解的一部分，但它的机制也很简单，就是为每个对象维护一个引用计数，当这个引用计数落为0的时候立刻释放对象所占内存。它无法处理循环引用的情况，分代垃圾收集器即`gc`模块则是为了应对这种情况而产生。这两种技术相辅相成组成了python中的垃圾处理机制。

基于引用计数的垃圾收集机制是一种相对简单的机制。在一些其他语言中，有一些更现代的机制，如java中的可达性算法。这个算法的基本思路就是通过一系列的称为`GC Roots`的对象作为起始点，从这些节点开始向下搜索所有走过的路径作为引用链，当一个对象到`GC Roots`没有任何引用链相连时候，则证明此对象不可用。这一种算法也能够避免循环引用的产生。

<img src="https://motor-taxi-master-rider.github.io/assets/img/reachability_analysis_algorithm.png"  title="可达性算法示例"/>

## 引用计数
在python的[c api文档中](https://docs.python.org/3.6/c-api/intro.html#objects-types-and-reference-counts)描述了cpython中引用计数的底层实现。

cpython中通过[Py_INCREF](https://docs.python.org/3.6/c-api/refcounting.html#c.Py_INCREF)和[Py_DECREF](https://docs.python.org/3.6/c-api/refcounting.html#c.Py_DECREF)两个宏来控制引用计数的增加和减少。对象析构器会触发`Py_DECREF`宏，该宏会检查对象的引用计数是否会被降为0————为0时则立刻释放该对象的内存，这就使得引用计数释放内存具有即时性。

你可以使用`sys.getrefcount`方法来取得某个对象的引用计数：

```python
import sys


foo = []

# 2 references, 1 from the foo var and 1 from getrefcount
print(sys.getrefcount(foo))

def bar(a):
    # 4 references
    # from the foo var, function argument, getrefcount and Python's function stack
    print(sys.getrefcount(a))

bar(foo)
# 2 references, the function scope is destroyed
print(sys.getrefcount(foo))
```

## 分代垃圾收集器
引用计数这个简单的机制会带来许多问题，如无法解决循环引用、需要线程锁及效率低下。为了解决循环引用的问题，[gc模块](https://docs.python.org/3.6/library/gc.html)在python 1.5版本中被加入。

由于循环引用只会在container容器类型中发生，所以`gc`模块并不会追踪python中所有的对象。我们可以使用`gc.is_tracked`函数来判断某个对象是否被追踪：

```python
>>> gc.is_tracked(0)
False
>>> gc.is_tracked("a")
False
>>> gc.is_tracked([])
True
>>> gc.is_tracked({})  #这个字典为空，因此未被追踪
False
>>> gc.is_tracked({"a": 1})  #这个字典所有元素都为原子类型，因此未被追踪
False
>>> gc.is_tracked({"a": []})
True
```

与引用计数机制的即时触发不同的是，为了保证性能`gc`并不是实时触发的。

首先要提到的是`gc`的 **分代机制**。作为一个分代垃圾收集器，所有被`gc`追踪的对象被分为三代：新生代、中年代和老年代，较新代的对象将会被更频繁的处理。所有新对象会被界定为新生代，只有当某个对象在一次`gc`中存活下来时它才会作为一个年迈的对象被标记为更老的一代。分代机制在一定程度上优化了`gc`的性能。

当某一代加入的对象数量超过一个阈值时，就会触发`gc`处理这一代及更新代的对象。这一阈值可以使用`gc.get_threshold`方法获得，如标准的阈值为(700,10,10)分别对应新中老三代的阈值。值得一提的是，为了提升性能，对第三代的‘长寿’对象的收集（即全局垃圾收集）需要达到[一个特性的标准](https://github.com/python/cpython/blob/051295a8c57cc649fa5eaa43526143984a147411/Modules/gcmodule.c#L94)————`long_lived_pending / long_lived_total`的比例大于25%。`long_lived_total`为在最近一次全局`gc`中存活下来的对象的数量，`long_lived_pending`为在所有非全局`gc`中存活下来的，现在处在老年代的对象的数量。

其次我们要探讨的是python中 **找出引用循环的算法**。我们经常看到对该算法的描述为：找到系统的 *根* 对象，从该对象开始遍历所有被追踪的容器对象，这些可到达的对象是活着的；释放所有其他对象。然而因为我们无法完全找到拓展模块的 *根* 对象，这种传统的方式已经不能再当今版本的python中使用了，因此我们得采取一种新的处理引用循环的算法。我们只需要处理被追踪的容器对象，得益于这点，我们可以以较小的代价将所有被追踪的对象用双向链表串联起来（减少在任意位置插入或删除节点的代价），并做如下处理：

1. 对链表中的每个对象，设置一个`gc_ref`s字段使其等于该对象的引用计数值；
2. 对于链表中的每个对象，找到它所引用的目标对象并减1该容器的`gc_refs`值；
3. 所有`gc_refs`值大于1的对象是有被立案表外对象引用的对象，因此我们不能释放它们的内存，将它们移至另一个集合中去（更年迈的代）；
4. 所有被这些转移的容器对象引用的链表中对象也不能够被释放，也将它们移到另一个集合中，对被它们引用的对象做相同的操作；
5. 现在我们的链表里剩下对象就是被循环引用的的对象，将它们释放；

# 总结
尽管有分代垃圾收集器帮助我们处理循环引用的问题，但在我们的代码中我们还是要注意避免出现循环引用。因为如果出现大量循环引用的话，启动`gc`机制依然要耗费大量的资源。在这里原作者给大家的建议是使用python中的`weakref`模块，弱引用并不会增加引用计数，当它引用的对象不存在时它会返回None给调用方。

另外，引用计数是一个我们不能控制的机制，但分代垃圾收集机制确是可以用`gc`模块hack的。我们可以使用`gc.disable()`来关闭分代垃圾收集器，并且使用`gc.collect()`函数来手动触发垃圾收集。但很多从业人员并不提倡这一点。

# Additional
参考：
1. [Things you need to know about garbage collection in Python](https://rushter.com/blog/python-garbage-collector/)
2. [Python internals: Memory management](https://rushter.com/blog/python-memory-managment/)
3. [Objects, Types and Reference Counts](https://docs.python.org/3.6/c-api/intro.html#objects-types-and-reference-counts)
4. [Garbage Collector interface](https://docs.python.org/3.6/library/gc.html)
5. [Garbage Collection for Python](http://arctrix.com/nas/python/gc/)
