---
layout: post
title: 一个简单的文本解析计算器
tags:
- Coroutine
- Singledispatch
- Tree
- Stackless
categories:
- Python
description: the target of this tutorial is to implement visiter parttern with stackless python.
---


# Description
之前在《python cookbook》上8.22节看到了用非递归的方式实现访问者模式的[方法](http://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p22_implementing_visitor_pattern_without_recursion.html)，通过巧妙地使用生成器的方式在树遍历或者搜索算法中中消除递归。从而避免了在使用访问者模式遍历深层嵌套树形数据结构时，因为超过嵌套层级限制而失败的情况。

原文是David Dabeaz基于python3.3版本构建的，很不凑巧的是，在python3.4版本又推出了一个非常强大的协程和生成器的新特性：`yield from`，这无疑为我们增添了新的玩具。

2014年，Dabeaz的[Final generator](http://www.dabeaz.com/finalgenerator)讲座全面地介绍了许多协程编写的诀窍并且炸毁了许多听众的大脑（包括笔者的），在课程的最后一部分他又从头用协程代替了经典的访问者模式，用于计算算术表达式。受他的课程的引导和启发便有了本文。

# 代码实现

从逻辑上来说，这个文本计算器会为我们分三步做事情：

1. 解析传入文本，将文本转换成可识别单元。很容易想到的是使用正则表达式来解析文本。
2. 确定运算的先后顺序，如乘除优先于加减。在这里我们将识别好的单元构造成树来体现运算的优先级。
3. 深度遍历生成树，计算并输出结果。

接下来我们就来一步一步实现这一简易编译器。

## 准备工作

首先定义好此次所需的数据结构和计算器类：

```python
import re
import types
from collections import namedtuple
from functools import singledispatch


class Node:
    """简易数据结构构造父类"""
    _fields = []

    def __init__(self, *args):
        for name, value in zip(self._fields, args):
            setattr(self, name, value)


class Number(Node):
    """数字型"""
    _fields = ['value']


class BinOp(Node):
    """操作符号型"""
    _fields = ['op', 'left', 'right']

class Calculator:
    # 可以被tokenize函数解析的字符
    TOKENS = [
        r'(?P<NUM>\d+)',
        r'(?P<PLUS>\+)',
        r'(?P<MINUS>-)',
        r'(?P<TIMES>\*)',
        r'(?P<DIVIDE>/)',
        r'(?P<POWER>\^)',
        r'(?P<WS>\s+)',
    ]

    # 储存字符类型和值的元组
    Token = namedtuple('Token', ['type', 'value'])

    def __init__(self, token=None):
        if token:
            self.TOKENS = token
        # 预编译正则表达式
        self.MASTER_RE = re.compile('|'.join(self.TOKENS))

    def caculate(self, text):
        """解析并计算表达式"""
        self.text = text
        try:
            token = self._tokenize(text)
            tree = self._parse(token)
            result = self._evaluate(tree)
        except Exception as e:
            raise e
        return result

    def _tokenize(self, text):
        """从字符串开始扫描所有匹配字符,输出所有非空元素"""
        pass

    def _parse(self, toks):
        """将tokenize后的元素parse成树结构"""
        pass

    def _evaluate(self, node):
       """遍历生成树计算结果"""
      pass
```

对于数据结构类我们使用了一种简单粗暴的构造方法：直接设置成类的属性。其实这也是一种蛮常用的方法，适合构造大量简单数据结构类。

对于计算器类，我们开放了caculate api接受传入的字符串，并经过上文论述的三个步骤来输出结果。当然我们也可以直接调用这三个步骤的方法来进行调试和维护，我们接下来的任务就是分别实现这三个方法。

## Tokenize

```python
def _tokenize(self, text):
      """从字符串开始扫描所有匹配字符,输出所有非空元素"""
      try:
          scan = self.MASTER_RE.scanner(text)
      except Exception as  e:
          raise e
      return (self.Token(m.lastgroup, m.group())
              for m in iter(scan.match, None)
              if m.lastgroup != 'WS')
```

`Tokenize`方法根据类变量`TOKENS`里的正则表达式捕获匹配字符组并且将它们命名，之后返回所有非空格的字符元素。

这里值得一提的是`re`模块的`scanner`方法。不知道是不是刻意而为之，它没有任何官方的文档。在我们这个简单编译器的情景下，它逐个扫描传入字符串里的所有符合正则表达式的元素并输出。

## Parse

```python
def _parse(self, toks):
        """将tokenize后的元素parse成树结构"""
        lookahead, current = next(toks, None), None

        def accept(*toktypes):
            """判断生成器toks的下个元素是否为传入类型"""
            nonlocal lookahead, current
            if lookahead and lookahead.type in toktypes:
                current, lookahead = lookahead, next(toks, None)
                return True

        # 表达式结构：
        # expr ::= term { +|- term }*
        # term ::= pow { *|/ pow}*
        # pow  ::= factor { ^ factor}*
        # factor ::= NUM
        def expr():
            left = term()
            while accept('PLUS', 'MINUS'):
                left = BinOp(current.value, left)
                left.right = term()
            return left

        def term():
            left = pow()
            while accept('TIMES', 'DIVIDE'):
                left = BinOp(current.value, left)
                left.right = pow()
            return left

        def pow():
            left = factor()
            while accept('POWER'):
                left = BinOp(current.value, left)
                left.right = factor()
            return left

        def factor():
            if accept('NUM'):
                return Number(int(current.value))
            else:
                raise SyntaxError()

        return expr()
```

`Parse`方法通过`accept`函数来遍历`tokenize`返回的字符元素迭代器，并通过树状的函数结构来生成一棵真正的树。非常欣赏它的模仿能力。

它将表达式在语意上分为三种类型：term，pow，factor (实际上这些名字没什么特别的意意义)。例如`1+2*4-5^2`这个表达式，factor为最小单元即数字，factor组成pow即` 1 2 4 5^2`为次小单元，pow组成term`1 2*4 5^2`,term组成表达式来体现运算符的优先级。

## Evaluate

```python
def _evaluate(self, node):
    """遍历生成树计算结果"""
    @singledispatch
    def visit(obj):
        raise NotImplemented

    @visit.register(BinOp)
    def _(node):
        """
        协程。
        visit method for BinOp
        """
        left = yield node.left
        right = yield node.right
        # TODO: could be more dynamic
        switch = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y,
        }
        try:
            return switch.get(node.op, None)(left, right)  # 产生StopIteration并返回结果
        except TypeError as e:
            pass

    @visit.register(Number)
    def _(node):
        """visit method for number"""
        return node.value

    def gen_visit(node):
        """
        委派生成器。
        返回输入数值及中间值。
        """
        result = visit(node)
        return (yield from result) if isinstance(result, types.GeneratorType) else result

    stack = [gen_visit(node)]  # 将根节点的协程放入栈
    result = None
    while stack:
        try:
            node = stack[-1].send(result)  # send(None)预激协程，send（result）将计算好的值存入协程
            stack.append(gen_visit(node))  # 深度遍历添加协程，等待处理
            result = None
        except StopIteration as e:
            stack.pop()
            result = e.value  # 取得number的值或表达式计算值
    return result
```

`Evalute`函数遍历`parse`所生成的树并计算结果。在这里我们用3.4新加入的`singledispatch`来替代原先Dabeaz使用的方式：

```python
methname = 'visit_' + type(node).__name__
meth = getattr(self, methname, None)
```

比较容易让人炸脑的是用list来管理栈的过程。以`1+2*4-5`这个表达式举例，传入`evaluate`方法的生成树是这样的。

```
第一层:
              BinOp             "-"            Number
第二层：
      Number   "+"      BinOp                    5
第三层：
        1        Number  "*"  Number
第四层：            2             4
```

如果你发现自己无法理解我的绘画作品的话不妨跑下`parse`方法。

1. 我们先将初始化根节点的委派生成器入栈，记该委派生成器`gen_visit`为`A`，传入None预激`A`,`visit(BinOp('-',x,y))`返回协程`a`，由于该协程为生成器子类，进入`return`语句中的`yield from result`子句代理的协程`a`，`yield`出`BinOp('-',x,y)`的左节点`BinOp('+',x,y)`。将其传入委派生成器`B`并入栈。此时协程`a`走至`left = yield node.left`语句的等号右边。
2. 传入None预激委派生成器`B`,`visit(BinOp('+',x,y))`返回协程`b`，进入`yield from result`代理的协程`b`中`yield`出`BinOp('+',x,y)`的左节点`Number(1)`。将其传入委派生成器`C`并入栈。此时协程`b`走至`left = yield node.left`语句的等号右边。
3. 传入None预激委派生成器`C`,`visit(Number(1))`返回整形`1`，
此时`return`将返回`result`，抛出`StopIteration`异常。我们捕获异常获得`result`的值`1`并将`C`出栈。
4. 将`1`传入委派生成器`B`代理的协程`b`，此时`left = yield node.left`中变量`left`获得传入值并继续`yield`出右节点`BinOp('*',x,y)`
5. 中间重复过程不再累述，当协程走至`return switch.get(node.op, None)(left, right)`则会抛出`StopIteration`异常和该表达式的运算结果，以此层层回溯得到最终的结果。

# 总结

至此，我们已经完成对`Calculator`类的编写，可以通过以下方式进行测试：

```python
cal = Calculator()
cal.caculate('1+2*4-5^2')
```

其实我们完全可以用python自带的`eval`方法来执行任意字符串代码。但之所以我们要大费周章地用协程实现这一文本计算器，是为了在python中实践`stackless`的思想。

比如要计算`cal.caculate('+'.join(str(i) for i in range(2017)))`,我们的`parse`函数会生成一棵超过两千深度的树，这时候就无法用递归的方式来遍历树了。

另外，如cookbook里说的，如果我们想用另一种没有`yield`语句的方案，我们不得不处理很多棘手的问题。例如，为了消除递归，我们必须要维护一个栈结构。如果不使用生成器，代码就会变得很臃肿，到处都是栈操作语句、会掉函数等。因此使用`yield`可以让你写出非常漂流的代码，它消除了递归但看上去又很像是递归实现，代码很简洁。


# Additional
代码源文件:
1. [text_calculator.py](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/text_calculator.py)
