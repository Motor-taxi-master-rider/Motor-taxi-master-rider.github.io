---
layout: post
title: Linklist Problems Summary
tags:
- Linklist
- Data_Structure
categories:
- Python
description: Analysis and solution of some linklist problems.
---


# Description
链表问题是经常会遇到的数据结构问题。该类问题的难点主要集中再单向遍历以及链表有环的情况下。很多链表问题只要利用两个速度不一的指针来完成单向遍历就可以简化问题、减少复杂度。本文基于一些常见的链表问题来分析比较良好的方案以及python实现。


# 准备工作
在解决问题之前，我们先要定义这次使用的链表的数据结构。
在此我们定义了一个普通的value和next指针的链表结构，并重写了__len__魔术方法来计算无环链表自身的长度，添加了traversal方法来帮助我们遍历链表验证结论。
在SampleLinklist类中我们定义了一些链表示例来辅助我们验证结论。

```python
# -*- coding: utf-8 -*-


class Linklist(object):
    def __init__(self, value, next):
        self.value = value
        self.next = next

    def traversal(self):
        """
        遍历该节点开始的链表
        :return:
        """
        print(self.value)
        if self.next:
            self.next.traversal()

    def __bool__(self):
        """
        用于之后的if Linklist判断
        :return:
        """
        return True

    def __len__(self):
        """
        :return: 无环链表的长度
        """
        count = 0
        node = self
        while node is not None:
            node = node.next
            count += 1
        return count


class SampleLinklist(object):
    def __init__(self):
        # 创建一个值为0-19的链表数组
        nodelist = [Linklist(i, None) for i in range(20)]
        # 0-6为无环单链表；7-11为有环单链表（入口为8）；
        # 12-14交于无环单链表(入口为5)；15-19交于有环链表（入口为9）；
        for key, value in enumerate(nodelist):
            if key != 6 and key != 11 and key != 14 and key != 19:
                value.next = nodelist[key + 1]
            elif key == 11:
                value.next = nodelist[8]
            elif key == 14:
                value.next = nodelist[5]
            elif key == 19:
                value.next = nodelist[9]

        #无环单链表
        self.normal_linklist = nodelist[0]
        #有环单链表（入口为8）
        self.loop_linklist = nodelist[7]
        #与normal_linklist交于5
        self.intersect_normal_linklist = (nodelist[0], nodelist[12])
        # 与nloop_linklist交于9
        self.intersect_loop_linklist = (nodelist[7], nodelist[15])
```

# 解决问题

## 在O(1)时间删除链表节点

**题目描述：** 给定链表的头指针和一个节点指针，在O(1)时间删除该节点。

**分析：** 本题与《编程之美》上的「从无头单链表中删除节点」类似。主要思想都是「狸猫换太子」，即用下一个节点数据覆盖要删除的节点，然后删除下一个节点。但是如果节点是尾节点时，python无法直接在内存中删除传入函数的对象，暂时还没找到办法解决。

```python
# -*- coding: utf-8 -*-

from linklist import SampleLinklist


def delete_specified_node(node):
    assert(node != None)
    if node.next != None:
        storeNode = node.next
        node.value = node.next.value
        node.next = node.next.next
```

## 反转单链表
**题目描述：** 输入一个单向链表，输出逆序反转后的链表。

**分析：** 链表的转置是一个很常见、很基础的数据结构题了。我们在这里运用了递归算法，将尾节点冒泡返回，然后对每个节点的指针反置。

```python
# -*- coding: utf-8 -*-

from linklist import SampleLinklist


def revert_linklist(node):
    if not node or not node.next:
        # 返回链表尾节点为，既反转后链表头结点
        return node
    # 暂存头结点
    header = revert_linklist(node.next)
    node.next.next = node
    node.next = None
    return header
```

## 找到单链表倒数第k个节点
**题目描述：** 输入一个单向链表，输出该链表中倒数第k个节点，链表的倒数第0个节点为链表的尾指针。

**分析：** 设置两个指针 p1、p2，首先 p1 和 p2 都指向 head，然后 p2 向前走 k 步，这样 p1 和 p2 之间就间隔 k 个节点，最后 p1 和 p2 同时向前移动，直至 p2 走到链表末尾。

```python
# -*- coding: utf-8 -*-


from linklist import SampleLinklist


def find_last_nth(header, n):
    if not header or n < 0:
        return None
    # 将fast和slow指针设至链表起点
    fast = slow = header
    # 将fast走n个节点
    while fast.next and n > 0:
        fast = fast.next
        n -= 1
    # n大于链表长度的情况
    if n > 0:
        return None
    while fast.next:
        fast = fast.next
        slow = slow.next
    return slow
```

## 找到单链表中间节点
**题目描述：** 求链表的中间节点，如果链表的长度为偶数，返回中间两个节点的任意一个，若为奇数，则返回中间节点。

**分析：** 此题的解决思路和第3题「求链表的倒数第 k 个节点」很相似。可以先求链表的长度， 然后计算出中间节点所在链表顺序的位置。但是如果要求只能扫描一遍链表，如何解决呢？ 最高效的解法和第3题一样，通过两个指针来完成。用两个指针从链表头节点开始，一个指针每次向后移动两步，一个每次移动一步，直到快指针移到到尾节点，那么慢指针即是所求。

```python
# -*- coding: utf-8 -*-


from linklist import SampleLinklist


def find_mid(header):
    if not header:
        return None
    # 将fast和slow指针设至链表起点
    fast = slow = header
    while  fast and fast.next:
        #fast速度为slow两倍
        fast=fast.next.next
        slow=slow.next
    return slow
```

## 判断单链表是否有环
**题目描述：** 输入一个单向链表，判断链表是否有环。如果链表存在环，如何找到环的入口点？

**分析：** 通过两个指针，分别从链表的头节点出发，一个每次向后移动一步，另一个移动两步，两个指针移动速度不一样，如果存在环，那么两个指针一定会在环里相遇。按照 p2 每次两步，p1 每次一步的方式走，发现 p2 和 p1 重合，确定了单向链表有环路了。接下来，让p2回到链表的头部，重新走，每次步长不是走2了，而是走1，那么当 p1 和 p2 再次相遇的时候，就是环路的入口了。为什么？：假定起点到环入口点的距离为 a，p1 和 p2 的相交点M与环入口点的距离为b，环路的周长为L，当 p1 和 p2 第一次相遇的时候，假定 p1 走了 n 步。那么有：p1走的路径： a+b ＝ n；p2走的路径： a+b+k*L = 2*n； p2 比 p1 多走了k圈环路，总路程是p1的2倍根据上述公式可以得到 k*L=a+b=n显然，如果从相遇点M开始，p1 再走 n 步的话，还可以再回到相遇点，同时p2从头开始走的话，经过n步，也会达到相遇点M。显然在这个步骤当中 p1 和 p2只有前 a 步走的路径不同，所以当 p1 和 p2 再次重合的时候，必然是在链表的环路入口点上。

```python
# -*- coding: utf-8 -*-


from linklist import SampleLinklist


def is_loop(header):
    if not header:
        return False
    fast = slow = header
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
        # 找到两步长交汇点
        if fast == slow:
            break
    if fast != slow:
        return None

    # 将fast发配回起点
    fast = header
    #当两节点再次相遇的时候则为环入口
    while not fast == slow:
        fast = fast.next
        slow = slow.next
    return fast
```

## 判断两个单链表是否相交
**题目描述：** 给出两个链表的头指针，判断其是否相交。

**分析：** 如果两个无环链表相交，则其尾指针一定相同；如果两个有环链表相交，则两个链表都有共同一个环，即环上的任意一个节点都存在于两个链表上。因此，就可以判断一链表上俩指针相遇的那个节点，在不在另一条链表上。

```python
# -*- coding: utf-8 -*-


from linklist import SampleLinklist
from whether_linklist_has_loop import is_loop


def is_intersect(header1, header2):
    if not header1 or not header2:
        return False
    if not is_loop(header1) and not is_loop(header2):
        # 两个无环链表的尾节点是否相等决定了它们是否相交
        while header1:
            header1 = header1.next
        while header2:
            header2 = header2.next
        return True if header1 == header2 else False
    elif not is_loop(header1) or not is_loop(header2):
        return False
    else:
        # 两个带环链表的入口必然在它们的环内
        intersect1 = is_loop(header1)
        intersect2 = is_loop(header2)
        node = intersect2.next
        # 如果任意链表环中有另一列表的节点则相交
        while node != intersect2:
            if node == intersect1:
                return True
            node = node.next
        return False
```

## 找到链表相交点
**题目描述：** 如果两个单链表相交，怎么求出他们相交的第一个节点呢？

**分析：** 当两链表无环时，则可采用对齐的思想。计算两个链表的长度 L1 , L2，分别用两个指针 p1 , p2 指向两个链表的头，然后将较长链表的 p1（假设为 p1）向后移动L2 - L1个节点，然后再同时向后移动p1 , p2，直到 p1 = p2。相遇的点就是相交的第一个节点。当两链表有环时，如果个环入口相等，则可看成以环入口为尾节点的无环情况。如果不等，则首公共节点为两个入口较近的那个。

```python
# -*- coding: utf-8 -*-


from linklist import SampleLinklist


def find_intersect_first_common(header1, header2):
    len1 = len(header1)
    len2 = len(header2)
    if len1 > len2:
        for i in range(len1 - len2):
            header1 = header1.next
    else:
        for i in range(len2 - len1):
            header2 = header2.next
    while header1:
        if header1 == header2:
            return header1
        header1 = header1.next
        header2 = header2.next
    return None
```

[源码下载](https://github.com/Motor-taxi-master-rider/data_structure_and_algorithm/tree/master/linklist_problems)

# Additional
参考文献:
1. [面试精选：链表问题集锦](http://wuchong.me/blog/2014/03/25/interview-link-questions/)
2. [流畅的python](http://www.ituring.com.cn/book/1564)
