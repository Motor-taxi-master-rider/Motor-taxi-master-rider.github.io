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

然而由于描述符的原因，使用类作为装饰器是一个更好地选择。

对于直接定义的装饰器，被装饰的方法的 __name__ 和 __doc__ 属性将会丢失，因此标准库functools提供了`warps`和`update_wrapper`装饰器来将被装饰方法的自省属性传递给装饰器：

```python
import functools

def function_wrapper(wrapped):
    #对闭包使用functools.wraps装饰
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        #对于类使用functools.update_wrapper装饰
        functools.update_wrapper(self, wrapped)
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

@function_wrapper
def function():
    pass
```

>事实上warps()重用了update_wrapper()的代码，为了更好地理解装饰器的运作，不妨让我们来看一下它的源码。

```python
"""
python 3.3版本的update_wrapper()的源码,在这里将被装饰的方法保存在__wrapped__属性中。这是一个bug，3.4中将这一步放在了函数体的最后。
这个函数又将WRAPPER_ASSIGNMENTS中的属性从被装饰函数wrapped中复制到装饰器wrapper中。
最后将被装饰函数__dict__中的内容复制到装饰器中。
"""
WRAPPER_ASSIGNMENTS = ('__module__',
       '__name__', '__qualname__', '__doc__',
       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper, wrapped,
        assigned = WRAPPER_ASSIGNMENTS,
        updated = WRAPPER_UPDATES):
    wrapper.__wrapped__ = wrapped
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(
                getattr(wrapped, attr, {}))
```

然而，即便使用了functools的修正方法保存了原函数的 __name__ 和 __doc__ 方法，但还是会在以下几个方面存在缺陷：
* 保存函数参数规范（`inspect.getargspec()`）
* 保存函数获取源码的能力（`inspect.getsource()`）
* 叠加附加在描述符上的能力

# 解决方案
## 描述符装饰器
解决问题的一个办法是为普通函数和类中函数分配各自的装饰方法，这样形成的装饰器也会是一种描述符。

```python
class bound_function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)
    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__( instance, owner)
        return bound_function_wrapper(wrapped)
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)
```

>如果装饰器附加在一个普通函数上，会使用function_wrapper的__call__方法返回的函数。而如果是附加在类方法上的话，则会调用__get__方法返回一个绑定instance的wrapper，然后它的__call__方法则会被触发。这使得该装饰器能传递描述符协议。

值得一提的是，每次当这个wrapper附加在类方法上被调用的时候，一个新的辅助wrapper将会被创建。这点无疑影响了效率。我们可能需要一个更加高效的方法来实现这种装饰器了。

## 透明对象代理
对于以上问题的解决方案被称为对象代理。以下是一个与被它包装的对象看上去很相似的wrapper：

```python
#这个对象代理的例子只代理了一些基本的方法。
class object_proxy(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__= wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __getattr__(self, name):
        return getattr(self.wrapped, name)
```

有了这个wrapper类我们就可以跟`update_wrapper()`说拜拜了。可以对我们的装饰器做以下修改：

```python
class bound_function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super(bound_function_wrapper, self).__init__(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)  

class function_wrapper(object_proxy):

    def __init__(self, wrapped):
       super(function_wrapper, self).__init__(wrapped)

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__( instance, owner)
        return bound_function_wrapper(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)
```

>这时，__name__ 和 __doc__ 之类的属性将会从代理对象中获取，inspect.getargspec()和inspect.getsource()也能够顺利工作。

这个方案还存在的一个明显缺陷就是：每次我们要定义一个新装饰器便要继承object_proxy代理函数并写两个类的代码。为了让我们的装饰器更好用不妨用工厂函数来帮我们完成这项重复工作。


# Additional
参考文献:
1. [Wrapt blog](https://github.com/GrahamDumpleton/wrapt/tree/develop/blog)
