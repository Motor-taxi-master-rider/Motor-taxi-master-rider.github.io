---
layout: post
title: 简单的文本解析计算器 v2
tags: Algorithms,Python,Stack
---

很久之前基于生成器写过[一个简单的文本解析计算器](https://motor-taxi-master-rider.github.io/yi-ge-jian-dan-de-wen-ben-jie-xi-ji-suan-qi.html)。这个计算器集中了很多面向对象的思想，但却不是很多有用。虽然它支持求幂`^`操作，但却无法处理括号，并没有那么有用。

学习栈的时候有了解过如何用后缀表达式求表达式的值，一直没有动手去亲自实现这一算法。最近有被问到和这个算法相类似的题，动手尝试下加深了印象。

# 中缀表达式转化后缀表达式

中缀转化后缀的规则如下，来自王道学堂：

![后缀表达式的计算步骤](https://motor-taxi-master-rider.github.io/assets/img/postfix_expression.png)

按照这一逻辑，实现的算法如下：

```python
def postfix_expression(string: str) -> List[Union[int, str]]:
    if not string:
        return []
    priority_map = {'+': 0, '-': 0, '*': 1, '/': 1}
    i = 0
    operator_stack = []
    postfix_expression = []
    while i < len(string):
        if string[i] == ' ':
            i += 1
            continue

        if string[i].isdigit():
            # 数字直接加入后缀表达式
            summary = 0
            while i < len(string) and string[i].isdigit():
                summary = summary * 10 + int(string[i])
                i += 1
            postfix_expression.append(summary)
        else:
            if string[i] == '(':
                # 若为左括号，入栈
                operator_stack.append(string[i])
            elif string[i] == ')':
                # 若为右括号，则把栈中运算符加入后缀表达式，直到遇到左括号
                operator = operator_stack.pop()
                while operator != '(':
                    postfix_expression.append(operator)
                    operator = operator_stack.pop()
            else:
                operator = string[i]
                if not operator_stack or operator_stack[-1] == '(' or priority_map[operator] > priority_map[
                    operator_stack[-1]]:
                    # 若1.栈空 2.栈顶元素为左括号 3.高于栈顶元素优先级，则入栈
                    operator_stack.append(operator)
                else:
                    # 若低于栈顶元素优先级，弹出栈顶加入后缀直到1.栈空 2.遇到左括号 3.遇到优先级比它低的运算符(乘和除，加和减之间的前后顺序)
                    while operator_stack and operator_stack[-1] != '(' and priority_map[operator] <= priority_map[
                        operator_stack[-1]]:
                        item = operator_stack.pop()
                        postfix_expression.append(item)
                    operator_stack.append(operator)

            i += 1

    while operator_stack:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression
```

我们要维护的运算符栈`operator_stack`的一个性质：栈上方运算符会比下方运算符更优先执行。

其中，之前困惑我比较多的点是c中的第四点：依次弹出栈顶运算符，直到一个优先级比它低的运算符或左括号。在38行有三个循环先决条件：

1. 运算符栈不能为空。适用于`1+2-3`这种情况，第二个加号pop出第一个加号后，栈中没有元素就需要停止循环
2. 运算符栈顶不能为左括号。只有右括号才能pop出左括号。停止循环时栈顶元素为左括号，之后将现在处理的运算符入栈。适用于`1+(2+3+4)`这种情况
3. 栈顶元素的运算符大于或等于正在处理的运算符，即只有遇到优先级比它低的运算符才会停止弹出操作。有这么两种情况：
   1. `1+2*3/4`，栈中已有`+,*`，`\`想入栈时发现栈顶元素等于它的优先级。此时先入栈的同级元素在表达式更靠前处，理应优先计算。最终操作是出栈`*`入栈`\`。而对于`+`，除法还是得优先于加法运行。
   2. `1+2*3-3`，栈中已有`+,*`，`-`想入栈时发现栈顶元素大于它的优先级，并且不会有元素小于它的优先级。因此会不断退栈直至抵达1或者2的条件。



来一个测试用例：

```python
assert postfix_expression('11 + 22*( 33*44/55-66)-77/88') == [11, 22, 33, 44, '*', 55, '/', 66, '-', '*', '+', 77, 88,
                                                              '/', '-']
```



# 计算后缀表达式

有了后缀表达式，接下来一部就是计算后缀表达式了。这步相对而言逻辑没有那么复杂。基本操作就是遍历后缀表达式入栈；遇到操作符退栈两个元素计算，将结果再次入栈。实现代码如下：

```python
def simple_calculator(string: str) -> float:
    postfix_list = postfix_expression(string)
    stack = []
    for item in postfix_list:
        if isinstance(item, int):
            stack.append(item)
        else:
            # 栈最上方的为第二位元素
            second = stack.pop()
            first = stack.pop()
            if item == '+':
                stack.append(first + second)
            elif item == '-':
                stack.append(first - second)
            elif item == '*':
                stack.append(first * second)
            elif item == '/':
                stack.append(first / second)

    return stack[-1]
```

有一个需要注意的点。退栈两个元素时，先被弹出的元素是计算表达式的第二位。

跑两个测试用例：

```python
assert simple_calculator('(10-(15+6/2)/3)*(6+8)') == 56
assert simple_calculator('11 + 22*( 33*44/55-66)-77/88') == -861.075
```



# 总结

以上就是用后缀表达式实现简单计算器的全部内容了。总的来说，逻辑复杂度集中在中缀转后缀的部分。

完整代码[链接](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/simple_calculator.py)。



