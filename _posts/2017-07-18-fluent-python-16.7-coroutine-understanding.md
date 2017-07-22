---
layout: post
title: Flunet Python 16.7 coroutine understading
tags:
- Fluent_Python
- Coroutine
categories:
- Python
description: Flunet Python 16.7 coroutine understading.
---


# Description
援引自《Fluent Python》16.7节中关于调用方通过yield from委派生成器调用子生成器的例子。因为一个代码细节造成了对于委派生成器理解上的困难，因此基于个人的理解做出相应地修改来优化该段代码。


# 原例

```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# the subgenerator
def averager():  # <1>
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # <2>
        if term is None:  # <3>
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # <4>


# the delegating generator
def grouper(results, key):  # <5># <6>
  while True:
        results[key] = yield from averager()  # <7>



# the client code, a.k.a. the caller
def main(data):  # <8>
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # <9>
        next(group)  # <10>
        for value in values:
            group.send(value)  # <11>
        group.send(None)  # important! <12>

    #print(results)  # uncomment to debug
    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
              result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
```

1. 与示例 16-13 中的 averager 协程一样。这里作为子生成器使用。

2. main 函数中的客户代码发送的各个值绑定到这里的 term 变量上。

3. 至关重要的终止条件。如果不这么做，使用 yield from 调用这个协程的生成器会永远阻塞。

4. 返回的 Result 会成为 grouper 函数中 yield from 表达式的值。

5. grouper 是委派生成器。

6. 这个循环每次迭代时会新建一个 averager 实例；每个实例都是作为协程使用的生成器对象。

7. grouper 发送的每个值都会经由 yield from 处理，通过管道传给 averager 实例。grouper 会在 yield from 表达式处暂停，等待 averager 实例处理客户端发来的值。averager 实例运行完毕后，返回的值绑定到 results[key] 上。while 循环会不断创建 averager 实例，处理更多的值。

8. main 函数是客户端代码，用 PEP 380 定义的术语来说，是“调用方”。这是驱动一切的函数。

9. group 是调用 grouper 函数得到的生成器对象，传给 grouper 函数的第一个参数是 results，用于收集结果；第二个参数是某个键。group 作为协程使用。

10. 预激 group 协程。

11. 把各个 value 传给 grouper。传入的值最终到达 averager 函数中 term = yield 那一行；grouper 永远不知道传入的值是什么。

12. 把 None 传入 grouper，导致当前的 averager 实例终止，也让 grouper 继续运行，再创建一个 averager 实例，处理下一组值。

>示例 16-17 中最后一个标号前面有个注释——“重要！”，强调这行代码（group.send(None)）至关重要：终止当前的 averager 实例，开始执行下一个。如果注释掉那一行，这个脚本不会输出任何报告。此时，把 main 函数靠近末尾的 print(results) 那行的注释去掉，你会发现，results 字典是空的。

[源码](https://github.com/fluentpython/example-code/blob/master/16-coroutine/coroaverager3.py)

# 理解与勘误

注解 **6** 表示在委派生成器中将会循环创建averager迭代器。这一点让我在理解起来产生了极大的困惑。因为以我之见对应每个key，委托迭代器只会在一个子迭代器中遍历并计算平均值。
遂我们将while True语句去掉，当main函数的for循环内给委托迭代器send None的时候便会抛出StopIteration异常。
之后将grouper生成器改写成如下便可成功运行。

```python
def grouper(results, key):
    results[key] = yield from averager()
    yield
```
在这里接受到None之后子迭代器averager迭代器也能成功返值Result，委托迭代器在第二个yield处阻塞所以不会抛出StopIteration异常。
当然也可以将while语句去掉后在main函数加入异常处理来捕获StopIteration异常，这样还能知道每个子迭代器停止的时间。

```python
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        try:
            group.send(None)
        except StopIteration as ex:
            print('end of child iterater')
```

假如使用源程序的while true这段代码的话，对于每个key子迭代器会生成两遍，当然第二遍的子迭代器是不会使用的。

下面简要说明示例的运作方式，还会说明把 main 函数中调用 group.send(None) 那一行代码（带有“重要！”注释的那一行）去掉会发生什么事。

* 外层 for 循环每次迭代会新建一个 grouper 实例，赋值给 group 变量；group 是委派生成器。

* 调用 next(group)，预激委派生成器 grouper，此时进入 while True 循环，调用子生成器 averager 后，在 yield from 表达式处暂停。

* 内层 for 循环调用 group.send(value)，直接把值传给子生成器 averager。同时，当前的 grouper 实例（group）在 yield from 表达式处暂停。

* 内层循环结束后，group 实例依旧在 yield from 表达式处暂停，因此，grouper 函数定义体中为 results[key] 赋值的语句还没有执行。

* 如果外层 for 循环的末尾没有 group.send(None)，那么 averager 子生成器永远不会终止，委派生成器 group 永远不会再次激活，因此永远不会为 results[key] 赋值。

* 外层 for 循环重新迭代时会新建一个 grouper 实例，然后绑定到 group 变量上。前一个 grouper 实例（以及它创建的尚未终止的 averager 子生成器实例）被垃圾回收程序回收。

# Additional
参考文献:
1. [流畅的python](http://www.ituring.com.cn/book/1564)
