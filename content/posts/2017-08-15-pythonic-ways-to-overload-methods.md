---
layout: post
title: Pythonic的泛函数
tags: Singledispatch,Multidispatch,Overload
category: Python
---


### Description
因为python不支持重载方法或函数，所以我们无法像java那样用不同的签名定义某个方法的变体来实现用不同的方式处理不同的数据类型，导致这个区别的根本原因是python语言的动态性。但也正因得益于此，利用动态参数类型以及字典参数列表，在python中我们常常可以把方法变成一个分派函数，使用一串if/elif/else调用专门的函数来实现类java重载的功能。然而这样并不便于模块的用户拓展，还显得很愚蠢：实现一长，分派函数会变得很大，而且它与各个专门函数之间的耦合也很紧密。

我们这里的泛型函数是指由一组为不同类型参数执行相似操作的函数组成的函数，具体调用哪一个函数的实现取决于分发算法和参数类型（也即是python中的参数列表类型重载）。在这里我们例举了`Fluent Python`里的singledispath和`Python Cookbook`里的利用函数注解实现方法重载的例子。来展现函数重载这一静态类型特性在python这个动态类型语言中的实现以及局限。对于这个特性实现牵扯到了python的多种元特性让它成为了一个实在有趣的话题。

Python单分发器（Singledispatch）是实现泛型函数的一种形式，由一个单一参数来决定选择和调用哪个函数。在Python3.4中，singledispath方法第一出现在functools模块中，你可以在[PEP 443 — Single-dispatch generic function](https://www.python.org/dev/peps/pep-0443/)找到关于它更多特性的介绍。

在`Python Cookbook`中介绍了一个不完美但可行的利用函数注解方式实现方法重载的方法，分别用元函数和与singledispath类似的装饰器实现。这是一个比较深入的关于函数注解的应用。你也可以在之前的博文中找到一些比较不深入的对于函数注解的[应用](https://motor-taxi-master-rider.github.io/python/2017/08/10/python-memoryview-and-annotation-ideas#description)。

### 代码示例

## Singledispatch
>Python 3.4 新增的 functools.singledispatch 装饰器可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。使用 @singledispatch 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。以下是fluent python中关于singledispatch的示例。

```python
from functools import singledispatch
from collections import abc
import numbers
import html

@singledispatch  # @singledispatch 标记处理 object 类型的基函数。
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlize.register(str)  # 各个专门函数使用 @«base_function».register(«type») 装饰。
def _(text):            # 专门函数的名称无关紧要；_ 是个不错的选择，简单明了。
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlize.register(numbers.Integral)  # 为每个需要特殊处理的类型注册一个函数。numbers.Integral 是 int 的虚拟超类。
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple)  # 可以叠放多个 register 装饰器，让同一个函数支持不同类型。
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'
```
>singledispatch 机制的一个显著特征是，你可以在系统的任何地方和任何模块中注册专门函数。如果后来在新的模块中定义了新的类型，可以轻松地添加一个新的专门函数来处理那个类型。此外，你还可以为不是自己编写的或者不能修改的类添加自定义函数。

## Multidispatch
>这是两个python cookbook中利用annotation对多参数方法的重载的示例。在第一个示例中我们利用元类来生成支持参数重载的类。在__prepare__方法中将类的字典变成自定义的MultiDict字典。

### 使用元类实现

```python
import inspect
import types

class MultiMethod:
    '''
    Represents a single multimethod.
    '''
    def __init__(self, name):
        self._methods = {}
        self.__name__ = name

    def register(self, meth):
        '''
        Register a new method as a multimethod
        '''
        sig = inspect.signature(meth)   #利用inpsect模块来获取函数签名

        # Build a type signature from the method's annotations
        types = []
        for name, parm in sig.parameters.items():
            if name == 'self':
                continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError(
                    'Argument {} must be annotated with a type'.format(name)
                )
            if not isinstance(parm.annotation, type):
                raise TypeError(
                    'Argument {} annotation must be a type'.format(name)
                )
            if parm.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth
            types.append(parm.annotation)

        self._methods[tuple(types)] = meth

    def __call__(self, *args):
        '''
        Call a method based on type signature of the arguments
        '''
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            raise TypeError('No matching method for types {}'.format(types))

    def __get__(self, instance, cls):
        '''
        Descriptor method needed to make calls work in a class
        '''
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

class MultiDict(dict):
    '''
    Special dictionary to build multimethods in a metaclass
    '''
    def __setitem__(self, key, value):
        if key in self:
            # If key already exists, it must be a multimethod or callable
            current_value = self[key]
            if isinstance(current_value, MultiMethod):
                current_value.register(value)
            else:
                mvalue = MultiMethod(key)   #装饰符来控制mvalue行为
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key, mvalue)
        else:
            super().__setitem__(key, value)

class MultipleMeta(type):
    '''
    Metaclass that allows multiple dispatch of methods
    '''
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, dict(clsdict))

    @classmethod
    def __prepare__(cls, clsname, bases):
        return MultiDict()
```

>为了使用这个类，你可以像下面这样写：

```python
class Spam(metaclass=MultipleMeta):
    def bar(self, x:int, y:int):
        print('Bar 1:', x, y)

    def bar(self, s:str, n:int = 0):
        print('Bar 2:', s, n)
### Example: overloaded __init__
import time

class Date(metaclass=MultipleMeta):
    def __init__(self, year: int, month:int, day:int):
        self.year = year
        self.month = month
        self.day = day

    def __init__(self):
        t = time.localtime()
        self.__init__(t.tm_year, t.tm_mon, t.tm_mday)
```

>测试结果

```python
>>> s = Spam()
>>> s.bar(2, 3)
Bar 1: 2 3
>>> s.bar('hello')
Bar 2: hello 0
>>> s.bar('hello', 5)
Bar 2: hello 5
>>> s.bar(2, 'hello')
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "multiple.py", line 42, in __call__
        raise TypeError('No matching method for types {}'.format(types))
TypeError: No matching method for types (<class 'int'>, <class 'str'>)
>>> # Overloaded __init__
>>> d = Date(2012, 12, 21)
>>> # Get today's date
>>> e = Date()
>>> e.year
2012
>>> e.month
12
>>> e.day
3
```

### 装饰器实现
>作为使用元类和注解的一种替代方案，可以通过描述器来实现类似的效果。

```python
import types

class multimethod:
    def __init__(self, func):
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults+1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self
```

>为了使用描述器版本，你需要像下面这样写：

```python
class Spam:
    @multimethod
    def bar(self, *args):
        # Default method called if no match
        raise TypeError('No matching method for bar')

    @bar.match(int, int)
    def bar(self, x, y):
        print('Bar 1:', x, y)

    @bar.match(str, int)
    def bar(self, s, n = 0):
        print('Bar 2:', s, n)
```

### 缺陷
本节的实现中的主要思路其实是很简单的。`MutipleMeta` 元类使用它的 `__prepare__()` 方法 来提供一个作为 `MultiDict` 实例的自定义字典。这个跟普通字典不一样的是， `MultiDict` 会在元素被设置的时候检查是否已经存在，如果存在的话，重复的元素会在 `MultiMethod` 实例中合并。

`MultiMethod` 实例通过构建从类型签名到函数的映射来收集方法。 在这个构建过程中，函数注解被用来收集这些签名然后构建这个映射。 这个过程在 `MultiMethod.register()` 方法中实现。 这种映射的一个关键特点是对于多个方法，所有参数类型都必须要指定，否则就会报错。
`
为了让 `MultiMethod` 实例模拟一个调用，它的 `__call__()` 方法被实现了。 这个方法从所有排除 `self` 的参数中构建一个类型元组，在内部map中查找这个方法， 然后调用相应的方法。为了能让 `MultiMethod` 实例在类定义时正确操作，`__get__()` 是必须得实现的。 它被用来构建正确的绑定方法。

不过本节的实现还有一些限制，其中一个是它不能使用关键字参数。

同样对于继承也是有限制的，例如，类似下面这种代码就不能正常工作：

```python
class A:
    pass

class B(A):
    pass

class C:
    pass

class Spam(metaclass=MultipleMeta):
    def foo(self, x:A):
        print('Foo 1:', x)

    def foo(self, x:C):
        print('Foo 2:', x)
```

原因是因为 x:A 注解不能成功匹配子类实例（比如B的实例），如下：

```python
>>> s = Spam()
>>> a = A()
>>> s.foo(a)
Foo 1: <__main__.A object at 0x1006a5310>
>>> c = C()
>>> s.foo(c)
Foo 2: <__main__.C object at 0x1007a1910>
>>> b = B()
>>> s.foo(b)
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "multiple.py", line 44, in __call__
        raise TypeError('No matching method for types {}'.format(types))
TypeError: No matching method for types (<class '__main__.B'>,)
```

### Additional
