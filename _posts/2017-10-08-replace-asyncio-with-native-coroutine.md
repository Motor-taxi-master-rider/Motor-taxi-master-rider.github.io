---
layout: post
title: Replace asyncio with native coroutine
tags:
- Asyncio
- Coroutine
categories:
- Python
description: note of David Beazley's lecture Topics of Interest(Python Asyncio).
---


# Description
在David Beazley的`Topics of Interest(Python Asyncio)`[演讲](http://pyvideo.org/python-brasil-2015/keynote-david-beazley-topics-of-interest-python-asyncio.html)中，他介绍了由于async在python中的种种历史遗留，asyncio库在`aync/await`语句加入之后已经不是一种最直接有效的python async实现。在写了一个简单程序替代asyncio库并与其及gevent库的效率做比较之后，我们发现了python3.5版本中引入的原声协程在处理异步方面具有非常高的效率。在演讲的最后他提出，可能我们需要的async并不是一个库而更像是一些api来供我们更有效地做底层的使用。

这次的演讲启迪了我许多，但碍于并没有相关的ppt和材料提供下载（有部分是David在台上光速Live coding的原因），我只能将其代码誊写下来，以供检验及研究，作为个人的读书笔记。

# Core programing of async server

## 准备工作
本文测试环境为python3.6版本，Intel Core i5-6500,8G RAM，win10。

David用了以下程序来做async服务器的测试。该程序会发送10000个请求并计算服务器处理请求的速率：

```python
#benchmark.py

import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

def benchmark(addr,nmessages):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.connect(addr)
    start=time.time()
    for n in range(nmessages):
        sock.send(b'x')
        resp=sock.recv(10000)
    end=time.time()
    print(nmessages/(end-start),'message/sec')

benchmark(('localhost',25000),100000)
```

## asyncio服务器
首先我们用asyncio来搭建一个异步服务器，代码如下：

```python
#asyncio_server.py

import asyncio
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

loop = asyncio.get_event_loop()


async def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(echo_handler(client))


async def echo_handler(client):
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            await loop.sock_sendall(client, b'Got:' + data)
    print('Connection closed')


loop.create_task(echo_server(('', 25000)))
loop.run_forever()
```

让我们启动服务并运行`benchmark.py`做测试，得到的结果为`9660.489944352334 message/sec`。

## 原生协程实现eventloop
观察以上asyncio服务器的代码，不难发现其中不仅有asyncio的eventloop（底层用生成器协程和`yield from`实现）还有新引入的`aync/await`原生协程，是一种跨界组合的状态。那么能不能将eventloop也用原生协程也实现呢？David给出了一个简单的方案：

```python
#native_coroutine_asyncio.py

from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


@coroutine
def read_wait(sock):
    yield 'read_wait', sock


@coroutine
def write_wait(sock):
    yield 'write_wait', sock


class Loop:
    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()

    async def sock_recv(self, sock, maxbytes):
        await read_wait(sock)
        return sock.recv(maxbytes)

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        while data:
            try:
                nsent = sock.send(data)
                data = data[nsent:]
            except BlockingIOError:
                await write_wait(sock)


    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        while True:
            while not self.ready:
                events = self.selector.select()
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)

            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    op, *args = self.current_task.send(None)  # run to the yield
                    getattr(self,op)(*args)  # sneaky method call
                except StopIteration:
                    pass

    def read_wait(self, sock):
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)
```

这段代码里有些比较不规范的做法，比如getattr(self,op)(* args)语句用字符串来运行函数，但无伤大雅，我们的目的是检验将eventloop换成原生协程实现的话会怎样。

我们将asyncioo_server中的eventloop换成刚刚实现的版本,其他代码保持不变：

```python
import native_coroutine_asyncio as native

loop=native.Loop()
```

运行`benchmark.py`发现每秒请求处理数变为了`19515.515222278125 message/sec`，效率提升了超过了100%。

## gevent服务器
为了做平行测试，David又用了gevent这个底层由c实现的库来检测原生协程的效率究竟如何，代码如下：

```python
#gevent_server.py

from gevent.server import StreamServer


# this handler will be run for each incoming connection in a deficated greenlet

def echo(socket, address):
    print('New connection from {}'.format(address))
    while True:
        data = socket.recv(100000)
        if not data:
            break
        socket.sendall(b'Got:' + data)
    socket.close()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 25000), echo)
    server.serve_forever()
```

在python3.6下它的每秒处理的请求数为`16807.0229190064 message/sec`，原生协程甚至比它还高一点。在David的线程测试的时候，他调用了python2.7的环境，使它和原生协程的效率是差不多。

# 结语
asyncio库其实有很大的历史包袱。python中的协程从单纯的yield生成器开始，经历了一个一个版本的变迁，生成器得到可以用`send`、`yield`，`throw`与外界通信的功能成为了意义上的协程；之后python3.3版本中加入的`yield from`给予了生成器协程更多的便利与可能；为期三年的郁金香项目逐渐孵化出asyncio又结合了以上的这些协程生成器组件及futures、callback、polling在3.4版本给我们带来了新的async模块。但要演化出这么一个模块所经历的一切实在是太久太长，我们面临的问题是：经过了这么多版本和这么久的时间变迁后是否它是最好的呢？有没有一个一步到位的协程来让我们使用呢？

在3.5版本中原生协程出现了，经过上面的实验我们可以初步判断它是一个更具效率的协程实现方案。这也让python有了新的优良特性，也让python在aync方向前进了一大步。

>在[How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)一文中详细的介绍了python async的历史：
受到[Icon语言](https://www2.cs.arizona.edu/icon/)的启发，python2.2中生成器首次被[PEP255 - simple generators](https://www.python.org/dev/peps/pep-0255/)引入。
而python2.5中yield语法的加入使得这一使用更少内存来迭代序列的想法更加实用。在这一版本中，[PEP342 - coroutine via enhanced generators](https://www.python.org/dev/peps/pep-0342/)使得python中的生成器不再试一点单纯的迭代器，被暂停的生成器也拥有了可以被send信息，与外界交互的能力。
生成器协程在相安无事了数个版本之后，终于在python3.3版本中[PEP380 - syntax for delegating to a subgenerator](https://www.python.org/dev/peps/pep-0380/)增加了新的语法yield from简化了协程之间的管道式调用。同一个版本中Guido主导的asyncio库作为实验性发布，并且在python3.4中正式成为标准库的一员。
python3.5中协程迎来了新的纪元，加入async def、async with、async for、await语法及相对应的底层协议。为了以示区分，用这些语法构成的协程称之为原生协程。原生协程不可以await一个非协程生成器，彻底讲生成器与协程的界限划分开来。

# Additional
源代码：
1. [asyncio_server.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/asyncio_server.py)
2. [native_coroutine_asyncio.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/native_coroutine_asyncio.py)
3. [gevnet_server.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/gevnet_server.py)
4. [benchmark.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/benchmark.py)
