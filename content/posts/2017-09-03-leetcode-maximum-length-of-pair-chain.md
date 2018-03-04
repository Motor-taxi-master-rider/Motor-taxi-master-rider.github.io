---
layout: post
title: LeetCode - Maximum Length of Pair Chain
tags: LeetCode,Math
category: Python
---


### Description
You are given `n` pairs of numbers. In every pair, the first number is always smaller than the second number.

Now, we define a pair `(c, d)` can follow another pair `(a, b)` if and only if `b < c`. Chain of pairs can be formed in this fashion.

Given a set of pairs, find the length longest chain which can be formed. You needn't use up all the given pairs. You can select pairs in any order.

**Example 1:**
```
Input: [[1,2], [2,3], [3,4]]
Output: 2
Explanation: The longest chain is [1,2] -> [3,4]
```

**Note:**
1. The number of given pairs will be in the range [1, 1000].

[Source link](https://leetcode.com/problems/maximum-length-of-pair-chain/description/)


### Best practice

>本题的关键在于减少时间复杂度。尝试了排序后发现，将列表元组按第二个元素排序是一个时间复杂度为o（n）的解决方案。举例来说，[5,6]前所能接的元素链长度总大于等于[4,6]，因此按此排序后从第一个元素开始遍历筛选就可以了。这里我们没有在遇到拥有相同第二个元素的元组时使用取最大值的方法，因为普通的顺序遍历就能得到o（n）复杂度的算法了。


python version

```python
from operator import itemgetter


class Solution(object):
    def findLongestChain(self, pairs):
        """
        :type pairs: List[List[int]]
        :rtype: int
        """
        last, n = None, 0
        for item in sorted(pairs, key=itemgetter(1)):
            if last is None:
                last, n = item, 1
            elif item[0] > last[1]:
                last, n = item, n + 1
        return n
```

**Mark:** 75 ms


### Additional
