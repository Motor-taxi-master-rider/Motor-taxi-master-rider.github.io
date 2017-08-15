---
layout: post
title: Python Memoryview and Annotation Ideas
tags:
- Memoryview
- Annotation
categories:
- Python
description: some brief ideas and preliminary cognition of python memoryview and annotation.
---


# Description
**Memoryview** (内存视图)是一个内置类，它能让用户在不复制内容的情况下操作同一个数组的不同切片。memoryview 的概念受到了 NumPy 的启发（参见 2.9.3 节）。Travis Oliphant 是 NumPy 的主要作者，他在回答“ When should a memoryview be used?” [link](http://stackoverflow.com/questions/4845418/when-should-a-memoryview-be-used/）这个问题时是这样说的：

内存视图其实是泛化和去数学化的 NumPy 数组。它让你在不需要复制内容的前提下，在数据结构之间共享内存。其中数据结构可以是任何形式，比如 PIL 图片、SQLite 数据库和 NumPy 的数组，等等。这个功能在处理大型数据集合的时候非常重要。

memoryview.cast 的概念跟数组模块类似，能用不同的方式读写同一块内存数据，而且内容字节不会随意移动。这听上去又跟 C 语言中类型转换的概念差不多。memoryview.cast 会把同一块内存里的内容打包成一个全新的 memoryview 对象给你。

****

Python 3 提供了一种句法，用于为函数声明中的参数和返回值附加元数据。**参考文献2** 中描述了python引入annotations的一种解释。

Python 对注解所做的唯一的事情是，把它们存储在函数的 __annotations__ 属性里。仅此而已，Python 不做检查、不做强制、不做验证，什么操作都不做。换句话说，注解对 Python 解释器没有任何意义。注解只是元数据，可以供 IDE、框架和装饰器等工具使用。即便没有强制语义，我们依然可以利用注解来规范函数输入。

# 使用Memoryview导入文件字符流
在这里我们比较了三种读取字节流的方式。后两种方法能减少一次数据的拷贝，但令人惊讶的是，使用memoryview并没有提高读取程序的效率和速度。
如果要进行本地测试的话，请将FILENAME改为你本地环境中的大文件的路径。

**代码：**
```python
import os
from time import time

# 大文件路径
FILENAME = r'C:\Users\chu060\Downloads\ubuntu-16.04.2-desktop-i386.iso'


def test_load_file_copy():
    """使用普通的读取字节流的方式，该方式会进行一次拷贝"""
    f = open(FILENAME, 'rb')
    buf = bytearray(f.read())
    f.close()
    return buf[:100]


def test_load_file_mv():
    """memoryview测试"""
    f = open(FILENAME, 'rb')
    buf = bytearray(os.path.getsize(FILENAME))
    mv = memoryview(buf)
    f.readinto(mv)
    f.close()
    return buf[:100]


def test_load_file_ba():
    """无memoryview，使用bytearray"""
    f = open(FILENAME, 'rb')
    buf = bytearray(os.path.getsize(FILENAME))
    f.readinto(buf)
    f.close()
    return buf[:100]


def load_tester(func, n=3):
    """进行测试并输出结果"""
    print('=' * 50)
    start = time()
    for i in range(n):
        result = func()
        if i == 0:
            print(result)
    print('try {test_times} times, {name} avg running time: {avg_time}'.format(
        test_times=n,
        name=func.__name__,
        avg_time=str((time() - start) / n)))


# 获取所有待测函数
test_funcs = [globals()[name] for name in globals() if name.startswith('test')]
# 进行测试,此处取十次测试的平均值
for func in test_funcs:
    load_tester(func, 10)

```
[source file](https://github.com/Motor-taxi-master-rider/Python/tree/master/Script/load_file_with_memoryview.py)

**运行结果为：**
```
==================================================
bytearray(b'3\xed\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x9
0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x903\xed\xfa\x8e\xd5\xbc\x
00|\xfb\xfcf1\xdbf1\xc9fSfQ\x06W\x8e\xdd\x8e\xc5R\xbe\x00|\xbf\x00\x06\xb9\x00\x
01\xf3\xa5\xeaK\x06\x00\x00R\xb4A\xbb\xaaU1\xc90\xf6\xf9\xcd\x13r\x16\x81\xfbU\x
aau\x10\x83\xe1\x01t')
try 10 times, test_load_file_ba avg running time: 0.9056999921798706
==================================================
bytearray(b'3\xed\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x9
0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x903\xed\xfa\x8e\xd5\xbc\x
00|\xfb\xfcf1\xdbf1\xc9fSfQ\x06W\x8e\xdd\x8e\xc5R\xbe\x00|\xbf\x00\x06\xb9\x00\x
01\xf3\xa5\xeaK\x06\x00\x00R\xb4A\xbb\xaaU1\xc90\xf6\xf9\xcd\x13r\x16\x81\xfbU\x
aau\x10\x83\xe1\x01t')
try 10 times, test_load_file_copy avg running time: 1.3784000158309937
==================================================
bytearray(b'3\xed\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x9
0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x903\xed\xfa\x8e\xd5\xbc\x
00|\xfb\xfcf1\xdbf1\xc9fSfQ\x06W\x8e\xdd\x8e\xc5R\xbe\x00|\xbf\x00\x06\xb9\x00\x
01\xf3\xa5\xeaK\x06\x00\x00R\xb4A\xbb\xaaU1\xc90\xf6\xf9\xcd\x13r\x16\x81\xfbU\x
aau\x10\x83\xe1\x01t')
try 10 times, test_load_file_mv avg running time: 0.9180000066757202
```

# 使用annotations进行参数检查
我们可以简单将annotations(注解)当成函数参数说明文档。注解会被储存在函数的__annotations__属性中，因此我们也可以利用这个字典来做更多的事情：比如参数类型、有效性的检验。

**代码：**
```python
def validate(func, locals):
    for var, test in func.__annotations__.items():
        value = locals[var]
        msg = 'Var: {0}\tValue: {1}\tTest: {2.__name__}'.format(var, value, test)
        assert test(value), msg


def is_int(x):
    return isinstance(x, int)

def between(lo, hi):
    def _between(x):
            return lo <= x <= hi
    return _between

def f(x: between(3, 10), y: is_int):
    validate(f, locals())
    print(x, y)
```

**结果：**
```
>>> f(0, 31.1)
Traceback (most recent call last):
   ...
AssertionError: Var: y  Value: 31.1 Test: is_int
```

# Additional
参考文献:
1. [Less Copies in Python with the Buffer Protocol and memoryviews](http://eli.thegreenplace.net/2011/11/28/less-copies-in-python-with-the-buffer-protocol-and-memoryviews/)
2. [Memoryview Q&A](https://stackoverflow.com/questions/3038033/what-are-good-uses-for-python3s-function-annotations)
