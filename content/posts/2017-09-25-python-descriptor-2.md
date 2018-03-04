---
layout: post
title: Python Descriptor Behavior II
tags: Descriptor
category: Python
---


### Description
在之前一篇[文章](https://motor-taxi-master-rider.github.io/python/2017/08/05/python-descriptor)中我们讨论了python描述符以及其行为，也做了一些总结。但个人能力有限，对描述符访问的优先规则解释的不是非常清楚。

近日看到一篇文章：[Python中的属性访问与描述符](http://fanchunke.me/Python/Python%E4%B8%AD%E7%9A%84%E5%B1%9E%E6%80%A7%E8%AE%BF%E9%97%AE%E4%B8%8E%E6%8F%8F%E8%BF%B0%E7%AC%A6/)中对于属性访问优先规则的部分解释的很清晰，遂记录下来学习。

### 属性访问的优先规则
属性访问的入口点是`__getattribute__`方法。它的实现中定义了Python中属性访问的优先规则。Python官方文档中对`__getattribute__`的底层实现有相关的介绍，本文暂时只是讨论属性查找的规则，相关规则可见下图：

<img src="https://motor-taxi-master-rider.github.io/assets/img/python_descriptor.png"  title="{{site.title }}"/>

上图是查找b.x这样一个属性的过程。在这里要对此图进行简单的介绍：

1. 查找属性的第一步是搜索基类列表，即type(b).__mro__，直到找到该属性的第一个定义，并将该属性的值赋值给`descr`

2. 判断descr的类型。它的类型可分为数据描述符、非数据描述符、普通属性、未找到等类型。若descr为数据描述符，则调用desc.__get__(b, type(b))，并将结果返回，结束执行。否则进行下一步

3. 如果`descr`为非数据描述符、普通属性、未找到等类型，则查找实例b的实例属性，即b.__dict__。如果找到，则将结果返回，结束执行。否则进行下一步；

4. 如果在b.__dict__ 未找到相关属性，则重新回到`descr`值的判断上。
  * 若`descr`为非数据描述符，则调用desc.__get__(b, type(b))，并将结果返回，结束执行
  * 若`descr`为普通属性，直接返回结果并结束执行；
  * 若`descr`为空（未找到），则最终抛出`AttributeError`异常，结束查找。



### Additional
