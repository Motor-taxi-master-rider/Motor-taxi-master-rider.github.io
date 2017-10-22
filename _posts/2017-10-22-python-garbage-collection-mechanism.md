---
layout: post
title: Python
tags:
- Gc
- Memory_management
categories:
- Python
description: note of python garbage collections documents.
---


# Description
本文环境为python3.6。

与c中拥有的malloc和free不同，python中的内存是编译器自动完成，因此我们并不需要时刻关心内存的使用情况。在[Things you need to know about garbage collection in Python](https://rushter.com/blog/python-garbage-collector/)一文中给我们详细介绍了python gc的具体实现及细节，本文主要参考该博客来对python垃圾处理机制做一些总结。

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

python中较大的对象会被分配到标准的c内存分配器，小对象分配器则由三个级别的抽象构成`Arena`、`Pool`、`Block`。

## Block
Block（块）是固定大小（8-512k）的内存块。为了方便起见，这些块被分为64类：

<table><thead><tr><th>Request in bytes</th><th>Size of allocated block</th><th>size class idx</th></tr></thead><tbody><tr><td>1-8</td><td>8</td><td>0</td></tr><tr><td>9-16</td><td>16</td><td>1</td></tr><tr><td>17-24</td><td>24</td><td>2</td></tr><tr><td>25-32</td><td>32</td><td>3</td></tr><tr><td>33-40</td><td>40</td><td>4</td></tr><tr><td>41-48</td><td>48</td><td>5</td></tr><tr><td>...</td><td>...</td><td>...</td></tr><tr><td>505-512</td><td>512</td><td>63</td></tr></tbody></table>

## Pool
Pool（池）是相同大小Block（块）的集合。通常来说，池的大小等于内存页的大小。固定块的大小能减少内存碎片的产生————当一个对象被销毁的时候，内存管理器能轻松地将相同大小的对象装载入块中。

在cpython中，池被定义为如下结构：

```code
/* Pool for small blocks. */
struct pool_header {
    union { block *_padding;
            uint count; } ref;          /* number of allocated blocks    */
    block * freeblock;                   /* pool's free list head         */
    struct pool_header * nextpool;       /* next pool of this size class  */
    struct pool_header *prevpool;       /* previous pool       ""        */
    uint arenaindex;                    /* index into arenas of base adr */
    uint szidx;                         /* block size class index        */
    uint nextoffset;                    /* bytes to virgin block         */
    uint maxnextoffset;                 /* largest valid nextoffset      */
};
```

池使用的是双向链表的结构，`nextpool`和`prevpool`字段指向链表节点。对于`freeblock`则是这么解释的：

```
pool->freeblock points to the start of a singly-linked list of free blocks within the pool.  When a
block is freed, it's inserted at the front of its pool's freeblock list.  Note
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
1. 引用计数
2. 分代垃圾收集器

引用计数是我们无法染指只能了解的一部分，

# Additional
参考：
1. [Things you need to know about garbage collection in Python](https://rushter.com/blog/python-garbage-collector/)
2. [Python internals: Memory management](https://rushter.com/blog/python-memory-managment/)
3. [gevnet_server.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/gevnet_server.py)
4. [benchmark.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/benchmark.py)
