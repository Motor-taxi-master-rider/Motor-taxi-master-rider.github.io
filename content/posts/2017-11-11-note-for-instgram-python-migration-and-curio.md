---
layout: post
title: Instagram python migration笔记
tags: Async
category: Python
---


### Description
Lisa Guo和Hui Ding在 **Pycon2017** 的[keynote](https://www.youtube.com/watch?v=66XoCk79kjM)分享了Instagram成功从python2.7、Django1.3升级到python3.6、Django1.8的经历。

在Talk Python fm之前的episode中，我惊喜地发现了有一期Michael Kennedy邀请到了[David Beazley](https://talkpython.fm/episodes/transcript/107/python-concurrency-with-curio)。在哪一期节目中他们畅谈了python concurrency相关及David在Github上的async项目[Curio](https://github.com/dabeaz/curio)。


### Instagram
很难想象Instagram能在保持产品功能高速迭代的同时完成从python2.7版本到3.5版本的跨越。他们在版本更新途中在代码层面遇到的主要有以下几类问题。

#### Unicode
Python3最显著的改动就是严格化了UNICODE/STR/BYTE的转换。Instagram编写了一些功能函数（`ensure_binary`,`ensure_str`,`ensure_text`）来确保之前代码里的输入和输出符合python3的标准。

#### Data format incompatible
在Instagram中经常用到了`pickle`模块。该模块在python2和3中的区别是：python3的pickle的协议最高版本提升到了4。他们发现即使将协议版本hardcode到python2里的2，由于版本2和3的同时存在，他们之间的相互序列化的转化也会存在问题。因此他们将不同版本的pickle结果隔离，做到自取自拿。

#### Iterator
Python3中的许多函数的返回值被修改成了迭代器（`map`,`filter`,`dict.item`），迭代器使得Instagram中那些会遍历两遍这些函数返回结果的代码全部失效。这其实非常难以调试，因此他们首先将所有该类函数的返回值用`list`方法还原成列表，然后将优化只迭代一遍的实例。

#### Dictionary ordering
[之前的一篇note](https://motor-taxi-master-rider.github.io/python/2017/11/05/note-for-async-dictionary-machine-learing)也讲过，由于python字典的版本改动，字典中的返回值将大大不同。

```python
testdict = {'a':1, 'b':2, 'c':3}
json.dumps(testdict)
```

各版本的返回结果大致为：

```
python2: {'a':1, 'c':2, 'b':3} (hardcode hashcode)

python3.5.1: (random)

python3.6：{'a':1, 'b':2, 'c':3} (keep order)
```

为了追求兼容性，他们对`json.dumps`函数加了参数：

```python
json.dumps(testdict, sort_keys=True)
```

另外他们也提到了以下的一个小的Unicode的改动将Instagram的性能提升了12%：

```python
if uwsgi.opt.get('optimize_men', None) == 'True'
    optimize_men()
```

to

```python
if uwsgi.opt.get('optimize_men', None) == b'True'
    optimize_men()
```

未来他们计划使用了python3完善好的特性type hints和mypy来提高他们codebase的健壮性，使用asyncio库用异步来处理之前的一些线程操作。

### Curio
David Beazley一直是一位我非常喜欢的python授业者，同时也是python cookbook的作者。他在这次访谈中提到了在python中实现async的另一种思路，也就是他写`Curio`库的目的。

在以教授python为业之前，他是教计算机科学系操作系统课程的教授。在课上他会告诉学生们如何用C语言来写操作系统的内核，内核做的事情主要就是多任务管理和IO，这和`asyncio`库所做的非常相似。既然`asyncio`库能将`callback`,`futures`,`coroutine`神奇地组合成一个奇妙的任务管理系统，为什么我们不能模仿系统内核也去实现一个任务管理系统呢？本身async编程也是一个焕发第二春的旧想法。

David也提到，由于python3.5中`async/await`关键字的加入，他之前的许多演讲和教程都有些过时了。这使他觉得，我们或许不该关注aync底层到底是如何实现的：无论是用`callback`还是用其他技术，而是关注我们该如何利用async编程或者说是async应该在的的领域。

可能现在async最大的问题就是它的传染性，一旦你代码中的一部分变成async，拿它所对应的整个代码生态链也必须是async的，否则小小的一段同步代码就会阻塞整个程序。虽然没有特别夸张，但是对于线程编程来说，这一点确实是值得考虑的。虽然asyncio库提供了一个函数作为对async中线程的支持，但是并没有将线程纳入`eventloop`处理的范畴之中，`coroutine`也不是线程安全的。David的设想就是在不远的将来能将线程和async统一结合起来，使得`eventloop`能同时兼任地处理协程和线程，这样对async的未来定是大有裨益。事实上David在`Curio`中已经完成了一个统一队列的组件（universal queue object）作为线程和协程的交流媒介。


### Additional
