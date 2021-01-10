---
layout: post
title: [Translate] Python中如何将多个参数传入map函数
tags: Translate,Python
---

> 来源：[How to Pass Multiple Arguments to a map Function in Python](https://miguendes.me/how-to-pass-multiple-arguments-to-a-map-function-in-python)
> 作者：Miguel Brito

在这篇文章中，我会给大家展示当有多个参数需要传入`map`函数时我的处理方式。这个方法不仅适用于普通的`map`方法，同时你也能以同样的技巧给`concurrent.futures.Executor.map`和`multiprocessing.Pool`传入复数个参数。



## 问题

假设我们有一个叫做`sum_four`的函数，它接收四个参数并且返回它们的总和。

```python
>>> def sum_four(a, b, c, d):
        return a + b + c + d
```

同时我们假设你在解决一个非常特殊的问题，该问题要求固定以上函数前三个参数。在仅改变最后一个参数的条件下，试图比较该函数的不同行为。

```python
>>> a, b, c = 1, 2, 3

>>> sum_four(a=a, b=b, c=c, d=1)
 7

>>> sum_four(a=a, b=b, c=c, d=2)
 8

>>> sum_four(a=a, b=b, c=c, d=3)
 9

>>> sum_four(a=a, b=b, c=c, d=4)
 10
```

如果说因为你喜欢函数式编程或者你来自一门鼓励这一范式的语言（*说的就是你，Haskell），所以你渴望使用`map`函数来解决这个问题，不难想到，既然只有`d`在变化，我们就可以将要测试的所有可能值存在列表里`ds = [1, 2, 3, 4]`。那么问题来了，给定一个函数和一个包含多个元素的列表，如果你想将这个列表传入一个只接受单个元素的`map`方法，该怎么做？



### 方案 1

第一个方案是用`itertools.starmap`来替代`map`函数。该函数接受一个函数及一个由元组组成的可迭代(_iterable_)对象作为参数。`startmap`会遍历各个元组`t`，之后将它们解包并作为参数执行函数，类似于`for t in tuples: function(*t)`。

为了让事情更加直观，给以下示例供思考：

```python
>>> import itertools

>>> ds = [1, 2, 3, 4]

>>> items = ((a, b, c, d) for d in ds)

>>> list(items)
 [(1, 2, 3, 1), (1, 2, 3, 2), (1, 2, 3, 3), (1, 2, 3, 4)]

>>> list(itertools.starmap(sum_four, items))
 [7, 8, 9, 10]
```

如你所见，列表中有很多重复的元素，当列表过长时它们会不可避免地消耗许多内存。作为改进，我将`items`设计成生成器，这样我们就可以只将正在处理的元素加载至内存中了。



### 方案 2

第二个方案是通过**柯里化**并创建一个新的偏函数。根据文档，[`partial()`](https://docs.python.org/2/library/functools.html#functools.partial)会“冻结”函数的某部分参数和(或)关键字，从而生成一个具有简化签名的新函数。

```python
In [29]: import functools

In [30]: partial_sum_four = functools.partial(sum_four, a, b, c)

In [31]: partial_sum_four(3)
Out[31]: 9

In [32]: list(map(partial_sum_four, ds))
Out[32]: [7, 8, 9, 10]
```



### 方案 3

第三个选择是使用[`itertools.repeat`](https://docs.python.org/3/library/itertools.html#itertools.repeat)。这个函数产生一个迭代器，该迭代器会一遍又一遍的返回对象。如果你没有指定_times_这一参数的话，就可以无限次地遍历它。接下来让我们仔细看一下`map()`的[签名](https://docs.python.org/3/library/functions.html#map)，它接收一个函数及多个可迭代对象作为参数，`map(function, iterable, ...)`。

根据文档中的描述，

> 如果传递了额外的*iterable*作为参数，则*function*必须能够接收和所有可迭代对象数量相同的参数，并且所有可迭代对象的元素将会同时并行地作用于该函数。当有复数个可迭代对象时，最短的可迭代对象耗尽则整个迭代就将结束。

_Bingo_！我们可以使用`itertools.repeat()`来制作`a` ，`b`， `c`的无穷迭代器。当最短的可迭代对象——`ds`被耗尽时，`map`就会停止。

```python
>>> import itertools
>>> list(map(sum_four, itertools.repeat(a), itertools.repeat(b), itertools.repeat(c), ds))
 [7, 8, 9, 10]
```

换一种方式的话，使用`repeat()`大致等效于：

```python
>>> list(map(sum_four, [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], ds))
 [7, 8, 9, 10]
```

你无需太担心内存的问题，因为元素只有在被使用时才会被生成。事实上，`repeat`返回一个`repeatobject`对象，而不是`list`[[ref](https://github.com/python/cpython/blob/3.9/Modules/itertoolsmodule.c#L4226)]。



## 问题 2：如何传递多个参数`multiprocessing.Pool.map`?

这是一个和普通`map()`函数与多个参数交互类似的问题。假设我们的要提高代码性能，将`sum_four`并行运行在不同进程中。好消息是上述的大部分方案可以适用于这一新的场景中，除了一个例外：`Pool.map`只接收单一的可迭代对象。这意味着我们不再能够使用`repeat()`，那让我们看看其他方案吧。

### 使用 `starmap`

```python
>>> from multiprocessing import Pool

>>> import itertools

>>> def sum_four(a, b, c, d):
                return a + b + c + d

>>> a, b, c = 1, 2, 3

>>> ds = [1, 2, 3, 4]

>>> items = [(a, b, c, d) for d in ds]

>>> items
 [(1, 2, 3, 1), (1, 2, 3, 2), (1, 2, 3, 3), (1, 2, 3, 4)]

>>> with Pool(processes=4) as pool:
         res = pool.starmap(sum_four, items)

>>> res
 [7, 8, 9, 10]
```



### 使用 `partial()`

```python
>>> import functools

>>> partial_sum_four = functools.partial(sum_four, a, b, c)

>>> with Pool(processes=4) as pool:
         res = pool.map(partial_sum_four, ds)

>>> res
 [7, 8, 9, 10]
```



## 问题 3： 如何传递多个参数给`concurrent.futures.Executor.map`?

 [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) 模块提供了一种叫 `Executor`的高层接口来运行异步运行可调用对象(_callable_)。

当前的版本中这一接口存在两种不同的实现方式，即 `ThreadPoolExecutor` 和 `ProcessPoolExecutor`。与 `multiprocessing.Pool`相反的是，  `Executor` 没有 `startmap()`方法，但是它的`map()` 实现支持多个可迭代对象。这允许我们使用 `repeat()`函数。另外一个区别是 `Executor.map` 返回的是生成器而非列表。



### 使用 `partial()`

```python
>>> from concurrent.futures import ProcessPoolExecutor

>>> import functools

>>> def sum_four(a, b, c, d):
                return a + b + c + d

>>> a, b, c = 1, 2, 3

>>> ds = [1, 2, 3, 4]

>>> partial_sum_four = functools.partial(sum_four, a, b, c)

>>> with ProcessPoolExecutor(max_workers=4) as pool:
              res = list(pool.map(partial_sum_four, ds))

>>> res
 [7, 8, 9, 10]
```



### 使用 `repeat()`

```python
>>> from concurrent.futures import ProcessPoolExecutor

>>> from itertools import repeat

>>> def sum_four(a, b, c, d):
                return a + b + c + d

>>> a, b, c = 1, 2, 3

>>> ds = [1, 2, 3, 4]

>>> with ProcessPoolExecutor(max_workers=4) as pool:
              res = list(pool.map(sum_four, repeat(a), repeat(b), repeat(c), ds))

>>> res
 [7, 8, 9, 10]
```



## 结论

伙计们！这就是今天的全部内容了。希望你能学到一些有用和特别的东西。 `map()`函数使得Python有个函数式编程语言的感觉。 `map()`不仅是一个置函数，还可以作为 `multiprocessing` 和 `concurrent.futures` 模块的方法使用。在本文中，我展示了如何在`map`函数里处理多个参数。如果你喜欢这篇文章，请考虑与你的朋友们分享！ 另外，请随时关注我： [miguendes.me](http://miguendes.me/)。

你可能会喜欢我的其他文章：

- [How to Use datetime.timedelta in Python With Examples](https://miguendes.me/how-to-use-datetimetimedelta-in-python-with-examples)
- [73 Examples to Help You Master Python's f-strings](https://miguendes.me/73-examples-to-help-you-master-pythons-f-strings)
- [How to Check if an Exception Is Raised (or Not) With pytest](https://miguendes.me/how-to-check-if-an-exception-is-raised-or-not-with-pytest)
- [3 Ways to Test API Client Applications in Python](https://miguendes.me/3-ways-to-test-api-client-applications-in-python)
- [Everything You Need to Know About Python's Namedtuples](https://miguendes.me/everything-you-need-to-know-about-pythons-namedtuples)
- [The Best Way to Compare Two Dictionaries in Python](https://miguendes.me/the-best-way-to-compare-two-dictionaries-in-python)
- [5 Hidden Python Features You Probably Never Heard Of