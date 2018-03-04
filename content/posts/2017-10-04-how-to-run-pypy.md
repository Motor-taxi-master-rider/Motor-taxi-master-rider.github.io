---
layout: post
title: How to run PyPy
tags: PyPy
category: Python
---


### Description
`PyPy`是目前速度最快的python解释器。先不说它惊人的用python来编写python解释器的理念，之前在planet python里看到一篇`PyPy`计划移除GIL的[文章](https://morepypy.blogspot.com/2017/08/lets-remove-global-interpreter-lock.html)就已经让我惊为天人了。
听了David Beazley在2012年关于`PyPy`和`Rpython`的几个演讲之后([Additional](#additional) 1,2,3)，就对这个项目起了浓厚的兴趣。

### Download and install
可以在<https://pypy.org/download.html>下载到`PyPy`的最新版本。`PyPy`已经支持python2.7和3.5.3了，但基于python3的`PyPy`依旧是一个beta版本，并且声称比`PyPy`2的速度慢很多。因为我们选择安装了基于Ubuntu的64位`PyPy`。解压后，为了日后使用我们使用以下命令在`/usr/local/bin`下创建一个软连接,其中第一个目录为`PyPy`的安装目录：

```
ln -s ~/Program/pypy2-v5.8.0-linux64/bin/pypy /usr/local/bin
```

现在我们可以用`pypy`命令进入`PyPy`的shell了。

### Performance test
David给了一段斐波那契数列的测试代码,其中`PyPy`是将`target`函数为入口函数的。经过测试，这个`PyPy`版本已经不需要这个入口函数了，也不需要向David在`Pycon`的分享中那样用`translate.py`先进行编译再执行c源码。（当然也可能是只有`Rpython`需要这么做。）本文所用的斐波那契数列的源码如下：

```python
#fib.py

import sys
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


def main(argv):
    print(fib(int(argv[1])))
    return 0


if __name__ == '__main__':
        main(sys.argv)
```

我们用python2.7，python3.6，pypy5.8这三个环境做性能测试：

* python2.7

```
>>time python fib.py 41

165580141

real	0m47.026s
user	0m46.564s
sys	0m0.024s
```

* python3.6

```
>>time python fib.py 41

165580141

real	1m9.771s
user	1m8.992s
sys	0m0.004s
```

* pypy5.8

```
>>time pypy fib.py 41

165580141

real	0m4.208s
user	0m3.392s
sys	0m0.736s
```

以上结果是在虚拟机里测试的，仅供参考。可以发现`PyPy`的运算速度比`Cpython`快了非常多，但python3比python2还慢蛮多的确实让我很气啊。当然，这只是一个纯cpu密集型程序的运算结果，根据`PyPy`的网站所说，得益于JIT以及Stackless，`PyPy`的平均速度应该是`Cpython`的四倍左右。
值得一提的是，David在`Pycon`演示的那个先编译再运行的`PyPy`版本，运行的斐波那契数列的速度甚至超过了未优化的c，一秒钟就你完成该运算，但在这个版本的pypy中没有编译的过程并且似乎没有了Daivd提到的`Restrict`数据类型的限制。

### Type restrict feature
为了说明`PyPy`的缺乏动态类型的支持，Daivd举了以下的例子：

```python
lst = [1, 2, 3, 'Hello']
for item in lst：
  print(lst)
```

```python
class A(object):
  def __int__(self, x, y):
    self.x = x
    self.y = y

a = A(1, 2)
b = B('Hello', 'world')
```

这些代码是通不过当时版本`PyPy`的编译的，然而在现在版本中可以正常运行，这点着实让我惊讶。David提到的一个`PyPy`的独特处理方式，就是讲纯python代码和rpython代码分开编译，我想这大概是其中原因。

<img src="https://motor-taxi-master-rider.github.io/assets/img/pypy_compile_1.png"  title="PyPy处理方式"/>



### Additional
1. [Understanding RPython](https://www.youtube.com/watch?v=GjnRLG8ATn4)
2. [Low Level RPython](https://www.youtube.com/watch?v=kkt_BtR9Kzk)
3. [Let's Talk About PyPy](https://www.youtube.com/watch?v=kkt_BtR9Kzk)
4. [PyPy documentation](http://doc.pypy.org/en/latest/release-1.2.0.html)
