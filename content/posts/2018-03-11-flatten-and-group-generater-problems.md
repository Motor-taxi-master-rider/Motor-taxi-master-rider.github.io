---
layout: post
title: StackOverflow list generator algorithms
tags: Algorithm,Generator
---


### Faltten nested lists with indices
这个问题来自[StackOverflow](http://adventofcode.com/2017/day/16)。

对于一个嵌套的列表L:

```python
L = [[[1, 2, 3], [4, 5]], [6], [7,[8,9]], 10]
```

希望有一个函数能够yield出每个元素的嵌套位置元组：

```python
(1, (0, 0, 0))
(2, (0, 0, 1))
(3, (0, 0, 2))
(4, (0, 1, 0))
(5, (0, 1, 1))
(6, (1, 0))
(7, (2, 0))
(8, (2, 1, 0))
(9, (2, 1, 1))
(10, (3,))
```
以`4`为例，元组`(0,1,0)`代表它处于第一层的 **首个列表** 中的 **第二个列表** 的 **第一个元素** 的的位置上。

之前我也遇到过一个`yield from`的示例，在此不得不提一下

```python
def flatten(iter):
    for item in iter:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
```

这个函数用递归的方式讲嵌套列表里的元素取出，`yield`出一个 *flatten* 版本的列表：`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`。

回归到这个问题，提问者给出了一个基于递归和生成器的解决方案：

```python
def flatten(l):
    for i, e in enumerate(l):
        try:
            for x, y in flatten(e):
                yield x, (i,) + y
        except:
            yield e, (i,)
```

这个函数的关键在于利用了元组加法的性质`(1, 2) + (3,) = (1, 2, 3)`来返回出嵌套位置的信息，而元组本身则是由变量`e`和`x`传递。

而底下的答案则提供了一个非递归的方案：

```python
def flatten(l):
    stack = [enumerate(l)]
    path = [None]
    while stack:
        for path[-1], x in stack[-1]:
            if isinstance(x, list):
                stack.append(enumerate(x))
                path.append(None)
            else:
                yield x, tuple(path)
            break
        else:
            stack.pop()
            path.pop()
```

这个算法定义了两个栈`stack`和`path`。`path`用来存储当前追踪元素的嵌套位置信息，而`stack`则是以外层至内层的顺序将列表的`enumerate`迭代器入栈。并按层次遍历。算法本身巧妙的一点是将入栈的初始位置置为`None`，之后再通过对`enumerate`的拆包用元素的位置信息替换`path`栈的最后一个元素。这个方法没有使用递归。

### Iterate through array while finding the mean of the top k elements
来源于Stack Overflow的问题: [Python iterate through array while finding the mean of the top k elements](https://stackoverflow.com/questions/49000803/python-iterate-through-array-while-finding-the-mean-of-the-top-k-elements/49001728#49001728)。

问题的描述是这样的：对于一个列表`a = [3, 5, 2, 7, 5, 3, 6, 8, 4]`, 我们希望找到所有连续三个元素中最大两个元素的均值。对于举例的列表`a`将生成列表`[4, 6, 6, 6, 5.5, 7, 7]`。首个连续三元素组合`[3, 5, 2]`的计算结果为`4`。

我们可把整个问题分解成三个部分：`1.` 获得每个连续三元组 `2.` 取出前两大的元素 `3.` 计算平均值。对于所有问题，我比较喜欢这个解答：

```python
# Sliding window
def windowed_iterator(iterable, n=2):
    iterators = itertools.tee(iterable, n)
    iterators = (itertools.islice(it, i, None) for i, it in enumerate(iterators))
    yield from zip(*iterators)

windows = windowed_iterator(iterable=a, n=3)

# Top 2 elements
from heapq import nlargest
top_n = map(lambda x: nlargest(2, x), windows)

# Mean
from statistics import mean
means = map(mean, top_n)
```

比较有趣的是`Sliding window`的部分，这里我们用`itertools.tee`生成三个独立的迭代器。并且用`islice`和`zip`进行错位和组合，最终生成连续三元组序列。

### Additional
