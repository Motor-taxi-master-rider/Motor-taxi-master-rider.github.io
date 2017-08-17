---
layout: post
title: Python装饰器的正确打开方式
tags:
- Decorator
- Wrapt
- Descriptor
categories:
- Python
description: give a speech to tell you how to implement your python decorators in a right way.
---


# Description
装饰器是python语言的一个非常常用及pythonic的特性，但往往由于忽视python中的内省，我们会写出一些不是特别完美的自定义装饰器。Graham Dumpleton写了一系列[博客](https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/README.md)，深入剖析了如何实现行为良好的装饰器。此外他还是[wrapt模块](http://wrapt.readthedocs.org/en/latest/)的作者,他将他对装饰器的深厚知识充分应用到这个模块之中。这个模块的作用是简化装饰器和动态函数包装起的实现，使得多层装饰也支持内省且行为正确，既可以应用到方法上，也可以作为描述符使用。

本文拾取了Graham Dumpleton在wrapt模块中附带的一系列博文的牙慧，旨在带来对python装饰器更深的理解和更好的设计。

# 两类装饰器及内省缺陷
装饰器符`@`是一种语法糖，深究原理的话使用装饰器实际上是一种猴子补丁的实现方式。以下的两种方式是等价的：

```python
@function_wrapper
def function():
    pass
```

>等价于

```python
#在python2.4版本你会这么做
def function():
    pass

function = function_wrapper(function)
```

而对于装饰器的实现，我们有以下两种方式：

>1.定义类

```python
class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

@function_wrapper
def function():
    pass
#通过魔术方法__call__来运行被包裹的方法
```

>2.使用闭包函数

```python
def function_wrapper(wrapped):
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

@function_wrapper
def function():
    pass
```







# Additional
参考文献:
1. [Less Copies in Python with the Buffer Protocol and memoryviews](http://eli.thegreenplace.net/2011/11/28/less-copies-in-python-with-the-buffer-protocol-and-memoryviews/)
2. [Memoryview Q&A](https://stackoverflow.com/questions/3038033/what-are-good-uses-for-python3s-function-annotations)
