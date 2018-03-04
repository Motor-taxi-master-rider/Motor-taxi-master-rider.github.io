---
layout: post
title: Pyjion、python debug、pandas优化笔记
tags: JIT,Debug,Pandas
category: Python
---


### Description
Brett Cannon和Dino Viehland在 **Pycon2016** 的[Pyjion: who doesn’t want faster for free?](https://www.youtube.com/watch?v=1DAIzO3QXcA)演讲中介绍了Microsoft为cpython提供JIT的c++项目`Pyjion`。之后我也在talkpython的往期访谈中找到与Brett Cannon的`Pyjion`相关的访谈，其中的很多看法让我大受脾益。

Elizaveta Shashkova在 **Pycon2017** 的[Debugging in Python 3 6 Better, Faster, Stronger](https://www.youtube.com/watch?v=NdObDUbLjdg&feature=youtu.be)演讲非常令人印象深刻。她在开发pycharm的JetBrains公司工作，而pycharm因为它优秀的debug功能成为了我最喜欢的IDE，没有之一。虽然俄罗斯老姐有一点口音，但并不影响这是一次让人感到Bingo的演讲。

同样在 **Pycon2017** 上，美丽的Sofia Heisler告诉了我们[No More Sad Pandas Optimizing Pandas Code for Speed and Efficiency](https://www.youtube.com/watch?v=HN5d490_KKk&feature=youtu.be)。这同样也是一次既实用而又让人能学到很多新知的讲解，非常高兴能有很多优秀的女性开发者参与到pycon中来。


### Pyjion
Brett Cannon介绍了各种python实现。`IronPython`和`Jython`分别是python基于C#和Java的实现，这样它们就可以兼容.Net和Java的应用了。

`PyPy`是我之前比较关注的一个实现。它主要有两部分组成，一是它有一组为编程语言定制JIT的工具，你不仅可以为python来实现JIT，也可以用Rpython为其他语言写一个JIT的实现。二是刚刚提到的Rpython，虽然`PyPy`是由python编写的，但这里的python实际上是python的超集Rpython。Rpython是静态类型版的python，因此能编译成c代码提高运行的效率。

`IronPython`、`Jython`和`PyPy`有一个共同的问题就是无法有效的兼容python的c api，致使使用者无法利用很多优秀的c库。`IronPython`和`Jython`由于它们并非是c语言实现具有如上兼容性问题非常容易理解，`PyPy`则是由于使用CFFI模块的原因对c api只有部分的支持。像`NumPy`这种模块`PyPy`只能开个新的项目重写，这也是`PyPy`作为最快的Python实现而得不到科学计算社区广泛应用的原因所在。

`Pyston`是Dropbox赞助的项目，它的目标是用JIT（LLVM JIT）提高python运行速度的同时尽可能地兼容python的c extension，因此它冲用了大部分`CPython`的代码。但比较遗憾的是`Pyston`现在只支持python2.7版本。

而`Pyjion`存在的意义则是直接为`Cpython`提供JIT的同时兼容更多的c extension。它由Dino发起，使用c++编写，单向支持python3版本。现在JIT是基于coreclr实现的，但在演讲中他们也提到这种实现也是可以作为一个后台系统更换的。

Brett Cannon也提到，python社区推广python3的关键是提高python3的速度，因此有很多核心开发者在从事这方面的工作，`Pyjion`也是其中之一。社区在建立一个对象的缓存系统：通过判断对象的版本来自省对象是否被改变，当未改变对象在缓存中时我们就不用对命名空间进行层层筛选来获取对象了。

另一个至关重要的优化就是之前一篇笔记中提到的可能会在python3.7中实装的调用函数速度的优化。调用函数瓶颈的产生是由于python的多种入参形式（位置参数，关键字参数，* args，** kwargs，python3中新添加的只允许关键字的参数，函数闭包）。这些入参形式是的了python在具备动态性的同时不丧失太多功能，但在构建参数列表时则会对系统产生极大地符合。Yuri针对这种情况开开发了新的加载实例方法和调用函数的字节码。

### Debug
Pycharm中的debug功能是基于`sys.settrace`函数完成的。而设置断点的功能则是在断点前插入一个字节码级别的监听用户输入的死循环。在加入新的字节码之后，还需要更新原有的变量和字节码的偏移量。当我们`dis`如下函数时：

```python
def maximun(a, b):
    if a > b:
        return a
    else:
        return b
```

将得到这些字节码：

```
2           0 LOAD_FAST                0 (a)
            2 LOAD_FAST                1 (b)
            4 COMPARE_OP               4 (>)
            6 POP_JUMP_IF_FALSE       12

3           8 LOAD_FAST                0 (a)
           10 RETURN_VALUE

5     >>   12 LOAD_FAST                1 (b)
           14 RETURN_VALUE
           16 LOAD_CONST               0 (None)
           18 RETURN_VALUE
```

我们想要在`return a`语句这一行打上断点时，插入了类似这样的函数：

```python
def _stop_at_break():
  # a lot of code here

def breakpoint():
  _stop_at_break()
```

字节码为：

```
0 LOAD_GLOBAL              0 (_stop_at_break)
2 CALL_FUNCTION            0
4 POP_TOP
6 LOAD_CONST               0 (None)
8 RETURN_VALUE
```

在python3.6之前，由于Pycharm使用的是`sys.settrace`，运行程序时每一行都会触发一次trace函数，因此调试时的运行时间将会增加25倍。Debug使得时间敏感的程序失去准确性。好在python3.6中部署了PEP523中的frame evaluation api。PEP523中有两个主要的内容:

1. Handle evaluation of frames
2. Add a new field to code objects

为了更好的让我们理解，Elizaveta Shashkova给了我们c code的python版示例：

```python
def frame_eval(frame, exc):
    func_name = frame.f_code.co_name
    line_number = frame.f_lineno
    print(line_number, func_name)
    return _PyEval_EvalFrameDefault(frame, exc)

def set_frame_eval():
    state = PyThreadState_Get()
    state.interp.eval_frame = frame_eval
```

这样我们就可以调用`set_frame_eval`来最终frame了。它只在每次进入frame时候触发，能大大减少debug运行时候的效率。但是当出现频繁调用函数致使进入frame的次数过多的时候，我们的debug运行效率将会退化到`sys.settrace`的水平。

这时候PEP523中的第二点就可以为我们所用了。这个特性拓展了`PyCodeObject`的结构，增加了`co_extra`属性。利用这个属性我们可以以不插入`breakpoint`函数的方式来标记代码。示例代码如下：

```python
def frame_eval(frame, exc):
    flag = _PyCode_GetExtra(frame.f_code, index)
    if flag == NO_BREAKS_IN_FRAME:
        return _PyEval_EvalFrameDefault(frame, exc)
    # check for breakpoints
```

最终的效率提升情况大致如下：

<img src="https://motor-taxi-master-rider.github.io/assets/img/frame_evaluation.png"  title="Frame evaluation"/>

### Pandas
Sofia Heisler测试的函数如下,测试数据文件[在此](https://github.com/sversh/pycon2017-optimizing-pandas/blob/master/new_york_hotels.csv)：

```python
def haversine(lat1, lon1, lat2, lon2):
    miles_constant = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    mi = miles_constant * c
    return mi
```

我们利用利用Jupyter notebook的`%%timeit`魔术方法及`line_profiler`来跑分。首先我们用循环的方式来遍历整个df:

```python
%%timeit
### Haversine applied on rows via iteration
haversine_series = []
for index, row in df.iterrows():
    haversine_series.append(haversine(40.671, -73.985,\
                                      row['latitude'], row['longitude']))
df['distance'] = haversine_series
```

得到的结果是`197 ms ± 6.65 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)`。

之后是apply方法：

```python
%timeit df['distance'] =\
df.apply(lambda row: haversine(40.671, -73.985,\
                               row['latitude'], row['longitude']), axis=1)
```

得到的结果是`78.1 ms ± 6.65 ms per loop (mean ± std. dev. of 7 runs, 10 loop each)`。如果用`line_profiler`来进行分析，就会发现性能瓶颈来自于频繁调用函数的第三行和第六行。

接下来我们将数据向量化。在Pandas中的向量化是如此的简单：

```python
### Vectorized implementation of Haversine applied on Pandas series
%timeit df['distance'] = haversine(40.671, -73.985,\
                                   df['latitude'], df['longitude'])
```

跑分的结果是`2.21 ms ± 230 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)`。调用`line_profiler`后发现函数第三行的执行频率下降到了和其他语句同一数量级（529)，第六行也从一万六千多次下降到了三千五百多次。但这还不是最优的结果。

之后我们将输入由pd.Series变为np.ndarray，减少了Pandas Series索引及检查数据类型等开销:

```python
### Vectorized implementation of Haversine applied on NumPy arrays
%timeit df['distance'] = haversine(40.671, -73.985,\
                         df['latitude'].values, df['longitude'].values)
```

得到的结果是`370 µs ± 18 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)`。

Sofia Heisler最后的实验是用Cython来优化函数本身的运算速度。因为如果有些原因我们不能将数据向量化亦或者向量化无法表达出原有的业务逻辑，那么我们就必须迭代我们的数据集了。为了提高效率我们将原函数写成这样然后用`apply`迭代：

```python
%%cython -a
### Haversine cythonized
from libc.math cimport sin, cos, acos, asin, sqrt

cdef deg2rad_cy(float deg):
    cdef float rad
    rad = 0.01745329252*deg
    return rad

cpdef haversine_cy_dtyped(float lat1, float lon1, float lat2, float lon2):
    cdef:
        float dlon
        float dlat
        float a
        float c
        float mi

    lat1, lon1, lat2, lon2 = map(deg2rad_cy, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    mi = 3959 * c
    return mi
```
```python
%timeit df['distance'] =\
df.apply(lambda row: haversine_cy_dtyped(40.671, -73.985,\
                              row['latitude'], row['longitude']), axis=1)
```

尽管如此，跑分的结果还是不如我们的向量化`51.1 ms ± 2.74 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)`。

最终的实验结果如下：

<img src="https://motor-taxi-master-rider.github.io/assets/img/optimizing_pandas.png"  title="Optimize pandas"/>

### Additional
