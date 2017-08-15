---
layout: post
title: LeetCode - Linked List Random Node
tags:
- LeetCode
- Reservoir_sampling
categories:
- Python
- R
description: Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.
---


# Description
Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.

Follow up:
What if the linked list is extremely large and its length is unknown to you? Could you solve this efficiently without using extra space?

**Example:**

```
// Init a singly linked list [1,2,3].
ListNode head = new ListNode(1);
head.next = new ListNode(2);
head.next.next = new ListNode(3);
Solution solution = new Solution(head);

// getRandom() should return either 1, 2, or 3 randomly. Each element should have equal probability of returning.
solution.getRandom();
```

[Source link](https://leetcode.com/problems/linked-list-random-node/description/)

# Analytics

当数据流长度已知或不大的时候可以简单的解决这个问题：遍历链表之后得到长度n，以`$$ \frac{1}{n} $$`的概率选取元素。

但当给出数据流的长度很大或者未知时，我们将无法做遍历链表得到长度的操作。此时因为数据流很大，为了追求效率，该数据流中数据只能访问一次。有没有这么一个随机选择算法，使得该数据流中的所有数据被选中的概率相等呢？

这个无边界的问题确实很让人头疼啊，但幸运的是，这我们可以用为蓄水池抽样（Reservoir Sampling）的方法来解决该类问题。

## 蓄水池抽样介绍

蓄水池抽样是一种从一个包含`n`个元素的列表`S`中随机抽取`k`个样本的随机算法，这里的`n`是一个非常大或者未知的值。

这个算法的基本思想就是先选中`1`到`k`个元素，作为被选中的元素。然后依次对第`k+1`至第`n`个元素做以下操作：
每个元素都有`$$ \frac{k}{i} $$`的概率被选中，然后以等概率`$$ \frac{1}{k} $$`替换掉被选中的元素。其中`i`是元素的序号。

## 算法证明

算法的成立是用数学归纳法证明的:

```
设每次都是以k/i的概率来选择

假设当前是i+1, 按照我们的规定，i+1这个元素被选中的概率是k/i+1，也即第 i+1 这个元素在蓄水池中出现的概率是k/i+1
此时考虑前i个元素，如果前i个元素出现在蓄水池中的概率都是k/i+1的话，说明我们的算法是没有问题的。

对这个问题可以用归纳法来证明：k < i <=N
1.当i=k+1的时候，蓄水池的容量为k，第k+1个元素被选择的概率明显为k/(k+1), 此时前k个元素出现在蓄水池的概率为 k/(k+1), 很明显结论成立。
2.假设当 j=i 的时候结论成立，此时以 k/i 的概率来选择第i个元素，前i-1个元素出现在蓄水池的概率都为k/i。
证明当j=i+1的情况：
即需要证明当以 k/i+1 的概率来选择第i+1个元素的时候，此时任一前i个元素出现在蓄水池的概率都为k/(i+1).
前i个元素出现在蓄水池的概率有2部分组成, ①在第i+1次选择前得出现在蓄水池中，②得保证第i+1次选择的时候不被替换掉
①.由2知道在第i+1次选择前，任一前i个元素出现在蓄水池的概率都为k/i
②.考虑被替换的概率：
首先要被替换得第 i+1 个元素被选中(不然不用替换了)概率为 k/i+1，其次是因为随机替换的池子中k个元素中任意一个，所以不幸被替换的概率是 1/k，故
前i个元素(池中元素)中任一被替换的概率 = k/(i+1) * 1/k = 1/i+1
则(池中元素中)没有被替换的概率为: 1 - 1/(i+1) = i/i+1
综合① ②,通过乘法规则
得到前i个元素出现在蓄水池的概率为 k/i * i/(i+1) = k/i+1
故证明成立
```

## 伪代码
```
Init : a reservoir with the size： k  
        for    i= k+1 to N  
            M=random(1, i);  
            if( M < k)  
                 SWAP the Mth value and ith value  
       end for
```

## 加权分布式蓄水池抽样

有时候我们的蓄水池中的数据是有权重，算法希望数据被抽样选中的概率和该数据的权重成正比。2005年Pavlos S. Efraimidis和Paul G. Spirakis的论文[Weighted random sampling with a reservoir](http://dl.acm.org/citation.cfm?id=1138834)提供了对于加权状态下这一问题的解决方案。们的解法既简单又优雅，基本思想和上面的分布式蓄水池抽样一致：对于每个数据计算一个0-1的值R，并求r的n次方根作为该数据的新的R值。这里的n就是该数据的权重。最终算法返回前k个R值最高的数据然后返回。根据计算规则，权重越大的数据计算所得的R值越接近1，所以越有可能被返回。

# Best practice

>python实现的普通蓄水池算法。

python version

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None
import random


class Solution(object):

    def __init__(self, head):
        """
        @param head The linked list's head.
        Note that the head is guaranteed to be not null, so it contains at least one node.
        :type head: ListNode
        """
        self.head = head
        self.k = 1 #随机选出的数量

    def getRandom(self):
        """
        Returns a random node's value.
        :rtype: int
        """
        count = 0
        node = self.head
        for _ in range(k):
            result.append(node.val)
            node = node.next
        while node:
            count += 1  #为linklist数量计数，视为i
            r = random.randint(1, count)
            if r <= self.k:  #以k/i的概率来选择
                result[r] = node.val  #这里没有用交换操作，会有数据丢失
            node = node.next
        return self.result


# Your Solution object will be instantiated and called as such:
# obj = Solution(head)
# param_1 = obj.getRandom()
```

**Mark:** 362 ms

-----

>这是维基百科上关于加权蓄水池算法的R语言实现。

In many applications sampling is required to be according to the weights that are assigned to each items available in set. For example, it might be required to sample queries in a search engine with weight as number of times they were performed so that the sample can be analyzed for overall impact on user experience. There are two ways to interpret weights assigned to each item in the set:
1. Let the weight of each item be $$ {\displaystyle w_{i}} w_{i} $$ and sum of all weights be W. We can convert weight to probability of item getting selected in sample as $${\displaystyle P_{i}=w_{i}/W} P_{i}=w_{i}/W$$.
2. Let the weight of two items i and j be $$ {\displaystyle w_{i}} w_{i} and {\displaystyle w_{j}} w_{j} $$. Let the probability of item i getting selected in sample be $$ {\displaystyle p_{i}} p_{i }$$, then we give$$ {\displaystyle p_{j}=\min(1,p_{i}{\frac {w_{j}}{w_{i}}})} {\displaystyle p_{j}=\min(1,p_{i}{\frac {w_{j}}{w_{i}}})} $$.

**Algorithm A-Res**
```r
(*
  S is a stream of items to sample, R will contain the result
  S.Current returns current item in stream
  S.Weight  returns weight of current item in stream
  S.Next advances stream to next position
  The power operator is represented by ^
  min-priority-queue supports:
    Count -> number of items in priority queue
    Minimum() -> returns minimum key value of all items
    Extract-Min() -> Remove the item with minimum key
    Insert(key, Item) -> Adds item with specified key
 *)
ReservoirSample(S[1..?], R[1..k])
  H = new min-priority-queue
  while S has data
    r = Random(0,1) ^ (1/S.Weight)  // important: inclusive range
    if H.Count < k
      H.Insert(r, S.Current)
    else
      if H.Minimum < r
        H.Extract-Min()
        H.Insert(r, S.Current)
    S.Next
```

# Additional
参考文献：
1. [Reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling)
2. [蓄水池抽样及实现](http://www.cnblogs.com/hrlnw/archive/2012/11/27/2777337.html)
3. [数据工程师必知算法：蓄水池抽样](http://blog.jobbole.com/42550/)
