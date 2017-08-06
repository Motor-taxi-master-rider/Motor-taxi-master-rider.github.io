---
layout: post
title: Python Descriptor
tags:
- Descriptor
categories:
- Python
description: 介绍了python中描述符（Descriptor）的种种。
---


# Description
描述符是对多个属性运用相同存取逻辑的一种方式。例如，Django ORM 和 SQL Alchemy 等 ORM 中的字段类型是描述符，把数据库记录中字段里的数据与 Python 对象的属性对应起来。

描述符是实现了特定协议的类，这个协议包括 __get__、__set__ 和 __delete__ 方法。property 类实现了完整的描述符协议。通常，可以只实现部分协议。其实，我们在真实的代码中见到的大多数描述符只实现了 __get__ 和 __set__ 方法，还有很多只实现了其中的一个。

描述符是 Python 的独有特征，不仅在应用层中使用，在语言的基础设施中也有用到。除了特性之外，使用描述符的 Python 功能还有方法及 classmethod 和 staticmethod 装饰器。理解描述符是精通 Python 的关键。

本文在简要介绍描述符的基础上探讨描述符在python中的显隐性。

# 描述符种类

在正式探讨描述符在python中的显隐性前，先了解下三种描述符。

## 覆盖型描述符

实现 __set__ 方法的描述符属于覆盖型描述符，因为虽然描述符是类属性，但是实现 __set__ 方法的话，会覆盖对实例属性的赋值操作。

## 没有 __get__ 方法的覆盖型描述符
通常，覆盖型描述符既会实现 __set__ 方法，也会实现 __get__ 方法，不过也可以只实现 __set__ 方法，此时，只有写操作由描述符处理。通过实例读取描述符会返回描述符对象本身，因为没有处理读操作的 __get__ 方法。如果直接通过实例的 __dict__ 属性创建同名实例属性，以后再设置那个属性时，仍会由 __set__ 方法插手接管，但是读取那个属性的话，就会直接从实例中返回新赋予的值，而不会返回描述符对象。也就是说，实例属性会遮盖描述符，不过只有读操作是如此。

## 非覆盖型描述符
没有实现 __set__ 方法的描述符是非覆盖型描述符。如果设置了同名的实例属性，描述符会被遮盖，致使描述符无法处理那个实例的那个属性。方法是以非覆盖型描述符实现的。

# Python属性查找策略


1. 优先找到Python自动产生的属性。
2. 查找obj.__class__.__dict__，如果attr存在并且是覆盖型描述符，返回覆盖型描述符的__get__方法的结果，如果没有继续在obj.__class__ 的父类以及祖先类中寻找覆盖型描述符。
3. 在obj.__dict__ 中查找，这一步分两种情况，第一种情况是obj是一个普通实例，找到就直接返回，找不到进行下一步。第二种情况是obj是一个类，依次在obj和它的父类、祖先类的__dict__中查找，如果找到一个描述符就返回描述符的__get__方法的结果，否则直接返回attr。如果没有找到，进行下一步。
4. 在obj.__class__.__dict__ 中查找，如果找到了一个描述符(这里的描述符一定是非覆盖型描述符)，返回描述符的__get__方法的结果。如果找到一个普通属性，直接返回属性值。如果没有继续在obj.__class__ 的父类以及祖先类中寻找非覆盖型描述符。
5. 很不幸，Python终于受不了。在这一步，它raise **AttributeError**。


# 代码验证

接下来我们编写示例代码来对以上策略进行验证。

```python
"""
覆盖型描述符:

    >>> obj = Model()
    >>> obj.__dict__['over'] = 'obj instance property over'
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> Model.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.Model'>
    >>> sub_obj = SubClass()
    >>> sub_obj.__dict__['over'] = 'sub_obj instance property over'
    >>> sub_obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.SubClass object at 0x...>
        owner    = <class 'descriptorkinds.SubClass'>
    >>> SubClass.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.SubClass'>

#行为完全符合策略2。额外的，这里测试了获取类属性时传入参数的值。

没有 __get__ 方法的覆盖型描述符:

    >>> obj.__dict__['over_no_get'] = 'obj instance property over_no_get'
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    'obj instance property over_no_get'
    >>> sub_obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> sub_obj.__dict__['over_no_get'] = 'sub_obj instance property over_no_get'
    >>> sub_obj.over_no_get  # doctest: +ELLIPSIS
    'sub_obj instance property over_no_get'

#行为符合策略4。其行为更像非覆盖型描述符。但无法直接使用obj.over_no_get的方式给实例属性赋值。

非覆盖型描述符：
    >>> obj.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> obj.non_over = 'obj instance property non_over'
    >>> obj.non_over  # doctest: +ELLIPSIS
    'obj instance property non_over'
    >>> sub_obj.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = <descriptorkinds.SubClass object at 0x...>
        owner    = <class 'descriptorkinds.SubClass'>
    >>> sub_obj.__dict__['non_over'] = 'sub_obj instance property non_over'
    >>> sub_obj.non_over  # doctest: +ELLIPSIS
    'sub_obj instance property non_over'

#行为符合策略4。
"""

# BEGIN DESCRIPTORKINDS
def print_args(name, *args):  # <1>
    cls_name = args[0].__class__.__name__
    arg_names = ['self', 'instance', 'owner']
    if name == 'set':
        arg_names[-1] = 'value'
    print('{}.__{}__() invoked with args:'.format(cls_name, name))
    for arg_name, value in zip(arg_names, args):
        print('    {:8} = {}'.format(arg_name, value))


class Overriding:  # <2>
    """a.k.a. data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # <3>

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # <4>
    """an overriding descriptor without ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # <5>
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Model:  # <6>
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # <7>
        print('Model.spam() invoked with arg:')
        print('    self =', self)

class SubClass(Model):
    def spam(self):
        print('SubClass.spam() invoked with arg:')
        print('    self =', self)
```

另外，在类中定义的函数属于绑定方法（bound method），因为用户定义的函数都有 __get__ 方法，所以依附到类上时，就相当于描述符。

```python
"""
# BEGIN FUNC_DESCRIPTOR_DEMO

    >>> word = Text('forward')
    >>> word  # <1>
    Text('forward')
    >>> word.reverse()  # <2>
    Text('drawrof')
    >>> Text.reverse(Text('backward'))  # <3>
    Text('drawkcab')
    >>> type(Text.reverse), type(word.reverse)  # <4>
    (<class 'function'>, <class 'method'>)
    >>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))  # <5>
    ['diaper', (30, 20, 10), Text('desserts')]
    >>> Text.reverse.__get__(word)  # <6>
    <bound method Text.reverse of Text('forward')>
    >>> Text.reverse.__get__(None, Text)  # <7>
    <function Text.reverse at 0x101244e18>
    >>> word.reverse  # <8>
    <bound method Text.reverse of Text('forward')>
    >>> word.reverse.__self__  # <9>
    Text('forward')
    >>> word.reverse.__func__ is Text.reverse  # <10>
    True

# END FUNC_DESCRIPTOR_DEMO
"""

# BEGIN FUNC_DESCRIPTOR_EX
import collections


class Text(collections.UserString):

    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]

# END FUNC_DESCRIPTOR_EX
```

# Additional
**描述符用法建议：**

1. 使用特性以保持简单

内置的 property 类创建的其实是覆盖型描述符，__set__ 方法和 __get__ 方法都实现了，即便不定义设值方法也是如此。特性的 __set__ 方法默认抛出 AttributeError: can't set attribute，因此创建只读属性最简单的方式是使用特性，这能避免下一条所述的问题。

2. 只读描述符必须有 __set__ 方法

如果使用描述符类实现只读属性，要记住，__get__ 和 __set__ 两个方法必须都定义，否则，实例的同名属性会遮盖描述符。只读属性的 __set__ 方法只需抛出 AttributeError 异常，并提供合适的错误消息。


3. 用于验证的描述符可以只有 __set__ 方法

对仅用于验证的描述符来说，__set__ 方法应该检查 value 参数获得的值，如果有效，使用描述符实例的名称为键，直接在实例的 __dict__ 属性中设置。这样，从实例中读取同名属性的速度很快，因为不用经过 __get__ 方法处理。

4. 仅有 __get__ 方法的描述符可以实现高效缓存

如果只编写了 __get__ 方法，那么创建的是非覆盖型描述符。这种描述符可用于执行某些耗费资源的计算，然后为实例设置同名属性，缓存结果。同名实例属性会遮盖描述符，因此后续访问会直接从实例的 __dict__ 属性中获取值，而不会再触发描述符的 __get__ 方法。

5. 非特殊的方法可以被实例属性遮盖

由于函数和方法只实现了 __get__ 方法，它们不会处理同名实例属性的赋值操作。因此，像 my_obj.the_method = 7 这样简单赋值之后，后续通过该实例访问 the_method 得到的是数字 7——但是不影响类或其他实例。然而，特殊方法不受这个问题的影响。解释器只会在类中寻找特殊的方法，也就是说，repr(x) 执行的其实是 x.__class__.__repr__(x)，因此 x 的 __repr__ 属性对 repr(x) 方法调用没有影响。出于同样的原因，实例的 __getattr__ 属性不会破坏常规的属性访问规则。
