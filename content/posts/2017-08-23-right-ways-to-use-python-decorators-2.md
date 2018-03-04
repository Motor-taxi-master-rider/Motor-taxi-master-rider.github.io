---
layout: post
title: Python装饰器的正确打开方式(2)
tags: Decorator,Wrapt,Descriptor
category: Python
---


### Description
装饰器是python语言的一个非常常用及pythonic的特性，但往往由于忽视python中的内省，我们会写出一些不是特别完美的自定义装饰器。Graham Dumpleton写了一系列[博客](https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/README.md)，深入剖析了如何实现行为良好的装饰器。此外他还是[wrapt模块](http://wrapt.readthedocs.org/en/latest/)的作者,他将他对装饰器的深厚知识充分应用到这个模块之中。这个模块的作用是简化装饰器和动态函数包装起的实现，使得多层装饰也支持内省且行为正确，既可以应用到方法上，也可以作为描述符使用。

本文拾取了Graham Dumpleton在wrapt模块中附带的一系列博文的牙慧，旨在带来对python装饰器更深的理解和更好的设计。
[上一篇文章](https://motor-taxi-master-rider.github.io/python/2017/08/18/right-ways-to-use-python-decorators-1)论述了普通装饰器可能带来的一些内省缺陷，并提出了一些解决方案。本文接上文更深入地介绍python装饰器的高级用法以便之后继续探讨关于内省缺陷的解决方案。

### 带参数的装饰器

接上文，我们至今为止的所创建的所有装饰器都不能传入任何参数，但要知道通过传入参数来改变装饰器的部分装饰行为是一种很常见并且强大的特性。通常我们只要用一个接受参数的函数闭包就能构成一个带参数的装饰器。

```python
def with_arguments(arg):
    @decorator
    def _wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

@with_arguments(arg=1)
def function():
    pass
```

如果给装饰器参数arg一个默认值的话，就能以`@with_arguments()`的方式调用它了。但这种调用方式会和我们之前使用装饰器的方式不一致。但是我们可以用参数默认值和`partial`函数结合的方法来实现这一前后的统一：

```python
def optional_arguments(wrapped=None, *, arg=1):
    if wrapped is None:
        return functools.partial(optional_arguments, arg=arg)

    @decorator
    def _wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return _wrapper(wrapped)

@optional_arguments(arg=2)
def function1():
    pass

@optional_arguments
def function2():
    pass
```

当wrapped参数为空时，则返回一个已经具有默认参数`arg`的装饰器`functools.partial(optional_arguments, arg=arg)`来装饰函数。

### 给被装饰的函数添加缓存功能

很多时候，当我们多遍调用某个函数的时候就会希望该函数能够“记录”下来它之前所运行的结果，并且在下次传入相同参数的时候不再去做它内部那些复杂的运算而是直接返回缓存的值。这听起来是一个有些麻烦的需求。幸运的是，通过在装饰器中定义一个缓存结构，能让我们方便地让任意一个函数拥有这一神奇的功能。

这里我们也用到了上一节所提到的默认参数和`partial`函数结合的装饰器设计：

```python
def cache(wrapped=None, d=None):
    if wrapped is None:
        return functools.partial(cache, d=d)

    if d is None:
        d = {}

    @decorator
    def _wrapper(wrapped, instance, args, kwargs):
        try:
            key = (args, frozenset(kwargs.items()))   #此次传入的参数集合
            return d[key]   #当参数集合已缓存时直接返回之前的结果
        except KeyError:
            result = d[key] = wrapped(*args, **kwargs)    #当为新参数的缓存到装饰器的字典中
            return result

    return _wrapper(wrapped)

@cache
def function1():
    return time.time()

_d = {}    #当传入同一个字典的时候，被装饰的不同函数会拥有相同的缓存。

@cache(d=_d)
def function2():
    return time.time()

@cache(d=_d)
def function3():
    return time.time()
```

与之前相同，我们也可以将这一缓存装饰器写成类的版本：

```python
class cache(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.d = {}

    def __call__(self, *args, **kwargs):
        try:
            key = (args, frozenset(kwargs.items()))
            return self.d[key]
        except KeyError:
            result = self.d[key] = self.wrapped(*args, **kwargs)
            return result

@cache
def function():
    return time.time()
```

### python中的同步装饰器

在Java中，如果我们希望一个方法是同步`(synchronized)`的，有两种方式给我们的代码增加同步特性：

```java
//第一是使用synchronized关键字的方式使整个方法具有同步特性
public class SynchronizedCounter {
    private int c = 0;
    public synchronized void increment() {
        c++;
    }
    public synchronized void decrement() {
        c--;
    }
    public synchronized int value() {
        return c;
    }
}

//第二是使用synchronized语句使得被包裹的代码块具有同步特性
//与第一个方法不同的是，我们必须制定一个提供内在锁的对象(这
//里是this)
public void addName(String name) {
    synchronized(this) {
        lastName = name;
        nameCount++;
    }
    nameList.add(name);
}
```

简单的来说，同步特性即是让每个类的实例都拥有一个内在的锁，当一个方法或一段代码被触发的时候就取得锁，当该方法返回时随后该锁就被释放。这种锁被称为 **重入锁** 。当一个线程获取对象锁之后，这个线程可以不用阻塞地再次获取本对象上的锁，而其他的线程是不可以的。这就使得从一个同步的方法运行在同一对象中的另一个同步方法成为了可能。

## 初探同步装饰器

在python中，我们可以利用上下文管理器和threading模块的锁方法来确保被我们装饰的函数具有同步特性。

```python
import threading

def synchronized(wrapped):
    lock = threading.RLock()
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrapper

@synchronized
def function():
    pass
```

当然我们也可以用上之前提到的带参装饰器技术使我们的同步锁装饰器更加灵活,再加上`decorator`装饰器来获取之前的自省特性。

```python
def synchronized(wrapped=None, lock=None):
    if wrapped is None:
        return functools.partial(synchronized, lock=lock)

    if lock is None:
        lock = threading.RLock()

    @decorator
    def _wrapper(wrapped, instance, args, kwargs):
        with lock:
            return wrapped(*args, **kwargs)

    return _wrapper(wrapped)

@synchronized
def function1():
    pass

lock = threading.Lock()

@synchronized(lock=lock)
def function2():
    pass
```

这使得我们的装饰器能够适用在实例、类和静态方法。但仔细想想以上代码的话会发现这一简单的实现其实并不实用。因为同步锁只对不同线程访问被装饰的方法时才起作用并且他会作用于着个类的所有实例，这和我们希望在java中看到的表现不尽相同。

我们想要的行为是：对于某个类的一个实例的所有被synchronized装饰过的实例方法，它们会同步关联一个类实例的单锁对象。

同时，我们要考虑一个额外的问题，发生竞争创建锁关系时我们该如何保证我们的线程安全性。

## 在对象中储存同步锁

让我们重新考虑一下问题，除了传入锁或者在函数闭包中创建它，我们可不可以让被装饰对象自己储存锁并通过包装函数来管理？

答案是肯定的。让我们来看以下代码：

```python
@decorator
def synchronized(wrapped, instance, args, kwargs):
    if instance is None:
        owner = wrapped   #当被装饰的位普通函数或静态方法时将同步锁绑在函数或方法上
    else:
        owner = instance    #当被装饰的为实例方法或类方法时将同步锁绑在实例或类上

    lock = vars(owner).get('_synchronized_lock', None)

    if lock is None:
      #使用metalock来确保创建同步锁时不会出现竞争关系
       meta_lock = vars(synchronized).setdefault(
               '_synchronized_meta_lock', threading.Lock())

       with meta_lock:
         #再次确认锁的存在状态，防止在生成meta_lock时同步锁已经被其他线程生成
           lock = vars(owner).get('_synchronized_lock', None)
           if lock is None:
               lock = threading.RLock()
               setattr(owner, '_synchronized_lock', lock)

    with lock:
        return wrapped(*args, **kwargs)

#对应的绑定关系如下
@synchronized # lock bound to function1
def function1():
    pass

@synchronized # lock bound to function2
def function2():
    pass

@synchronized # lock bound to Class
class Class(object):

    @synchronized # lock bound to instance of Class
    def function_im(self):
        pass

    @synchronized # lock bound to Class
    @classmethod
    def function_cm(cls):
        pass

    @synchronized # lock bound to function_sm
    @staticmethod
    def function_sm():
        pass
```

在实现我们的设计的时候一个关键的事情就是在第一次创建同步锁的时候我们需要判断锁是否存在，如果存在的话就返回原有的锁。我们通过`lock = vars(wrapped).get('_synchronized_lock', None)`获取锁。

当我们遇到多个线程竞争创建锁时，可以使用`lock = vars(wrapped).setdefault('_synchronized_lock', threading.RLock())`默认字典的形式来防止任一线程创建的锁被另一个线程覆盖。但如果我们使用这一方法的话，我们会在装饰类方法上遇到问题。因为类的字典`dictproxy`并没有setdefault方法，因此我们只能使用`setattr(Object, '_synchronized_lock', threading.RLock())`来为类设置同步锁

## 让同步锁装饰器具有上下文管理器的功能

 至此为止，我们已经实现了java的同步的第一个功能了。对于第二个功能，在python中是一个和上下文管理器相似的行为。我们想让我们的synchronized装饰器能够这样使用来同步方法或函数中的部分代码：

 ```python
 class Object(object):  

    @synchronized
    def function_im_1(self):
        pass  

    def function_im_2(self):
        with synchronized(self):
            pass
 ```

 为了拥有上下文管理器的功能，我们必须让装饰器函数返回一个具有`__enter__` and `__exit__`方法的对象。但我们的`synchronized(None)`实际返回的是一个`<__main__.function_wrapper object at 0x107b7ea10>`对象，再该类里我们还没有着两个方法的定义。因此我们已经不能使用原来的装饰器工厂函数`@decorator`了，作为替代我们首先要直接使用之前定义的`function_wrapper`类装饰器来获得内省功能：

 ```python
 def synchronized(wrapped):
    def _synchronized_lock(owner):
        lock = vars(owner).get('_synchronized_lock', None)

        if lock is None:
            meta_lock = vars(synchronized).setdefault(
                    '_synchronized_meta_lock', threading.Lock())

            with meta_lock:
                lock = vars(owner).get('_synchronized_lock', None)
                if lock is None:
                    lock = threading.RLock()
                    setattr(owner, '_synchronized_lock', lock)

        return lock

    #使用_synchronized_lock同步锁的自定义装饰器
    def _synchronized_wrapper(wrapped, instance, args, kwargs):
        with _synchronized_lock(instance or wrapped):
            return wrapped(*args, **kwargs)

    #直接使用function_wrapper自定义同步锁装饰器装饰到被装饰函数warpped上
    return function_wrapper(wrapped, _synchronized_wrapper)
 ```

 现在我们已经完成装饰工程函数的替换工作了，接下来的功能就是在`function_wrapper`类装饰器中加入
`__enter__` and `__exit__`魔术方法来实现上下文管理器，这里我们继承了`function_wrapper`类:

```python
def synchronized(wrapped):
    def _synchronized_lock(owner):
        lock = vars(owner).get('_synchronized_lock', None)

        if lock is None:
            meta_lock = vars(synchronized).setdefault(
                    '_synchronized_meta_lock', threading.Lock())

            with meta_lock:
                lock = vars(owner).get('_synchronized_lock', None)
                if lock is None:
                    lock = threading.RLock()
                    setattr(owner, '_synchronized_lock', lock)    #为被装饰器装饰的方法加锁

        return lock

    def _synchronized_wrapper(wrapped, instance, args, kwargs):
        with _synchronized_lock(instance or wrapped):
            return wrapped(*args, **kwargs)

    class _synchronized_function_wrapper(function_wrapper):

        def __enter__(self):
            self._lock = _synchronized_lock(self.wrapped)   #为上下文管理器枷锁
            self._lock.acquire()
            return self._lock

        def __exit__(self, *args):
            self._lock.release()

    return _synchronized_function_wrapper(wrapped, _synchronized_wrapper)
```

至此为止，我们对java的`synchronized`的移植就全部完成了。

### Additional
参考文献:
1. [Wrapt blog](https://github.com/GrahamDumpleton/wrapt/tree/develop/blog)
