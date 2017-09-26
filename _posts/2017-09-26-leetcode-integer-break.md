---
layout: post
title: LeetCode - Integer Break
tags:
- Leetcode
- Math
categories:
- Python
description: Given a positive integer n, break it into the sum of at least two positive integers and maximize the product of those integers. Return the maximum product you can get.
---


# Description
Given a positive integer n, break it into the sum of **at least** two positive integers and maximize the product of those integers. Return the maximum product you can get.

For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).

**Note:** You may assume that n is not less than 2 and not larger than 58.

[Source link](https://leetcode.com/problems/integer-break/description/)


# Best practice

>经过枚举可以发现，输入元素最终的不可分单位为2和3（所给例子中的10最小可被分为3+3+2+2）。由此可见我们只需要在只产生这两种不可分元素的情况下尽可能贪婪的获取更多3就能使被break的元素积最大了。更深入发现，若欲使元素积最大，只会出现一个2和两个2元素的情况，因此我们设计的代码如下。


python version 1

```python
class Solution(object):
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n < 4:
            return n - 1
        if n % 3 == 0:
            return 3 ** (n // 3)
        if (n - 2) % 3 == 0:
            return 3 ** ((n - 2) // 3) * 2
        if (n - 4) % 3 == 0:
            return 3 ** ((n - 4) // 3) * 2 ** 2
```

**Mark:** 32 ms

----

>这是leetcode上的pop的答案，偏计算机思维。用比目标元素小的元素的生成结果来计算之后的结果，其实多了很多循环，但不知道为什么leetcode声称运行起来更快。

python version 2

```python
class Solution(object):
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n < 4:
            return n - 1

        res = [0, 1, 2, 3]
        for i in xrange(4, n + 1):
            res[i % 4] = max(res[(i - 2) % 4] * 2, res[(i - 3) % 4] * 3)
        return res[n % 4]
```

**Mark:** 28 ms


# Additional
