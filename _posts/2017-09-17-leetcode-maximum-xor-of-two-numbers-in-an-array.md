---
layout: post
title: LeetCode - Maximum XOR of Two Numbers in an Array
tags:
- Leetcode
- Bit_manipulaion
categories:
- Python
description: Find the maximum result of ai XOR aj, where 0 ≤ i, j < n.
---


# Description
Given a **non-empty** array of numbers,$$ a_0, a_1, a_2, … , a_{n-1}, where 0 ≤ a_i < 2^{31} $$.

Find the maximum result of a_i `XOR` a_j, where `0 ≤ i, j < n`.

Could you do this in `O(n)` runtime?

**Example:**

```
Input: [3, 10, 5, 25, 2, 8]

Output: 28

Explanation: The maximum result is 5 ^ 25 = 28.
```

[Source link](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/description/)


# Best practice

>我们从左至右对每一位进行判断，在这个过程中逐渐缩小被我们选中的元素范围。假设输入列表包含26个整数（在这里我们以a,b,c,d至z来表示）。向右遍历时，当某几个数a,d,e,h,u在最大二进制位上不同时，就可以确定该位为我们最终答案的最大二进制位了。因为该位为1的情况大于该位右侧所有位为1的情况。在下次遍历时我们就可以检查这几个数中的次大二进制位是否不同，也就可以确定次大二进制位的值，我们的候选组也会从a,d,e,h,u缩小至a,e,h的情况。这个问题的特性是，每次我们缩小候选元素范围时，我们不需要关心哪些元素留下来了，只需要知道我们的最终答案是多少。


python version

```python
class Solution(object):
    def findMaximumXOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max, mask = 0, 0
        for i in reversed(range(32)):
            mask = mask | (1 << i)
            #prefix set
            prefixes = {num & mask for num in nums}
            temp = max | (1 << i)
            for prefix in prefixes:
                # 因为1^0=1,1^1=0,0^0=0,所以当a^b=c时，a^c=b
                # item1^item2=temp,item1^temp=item2
                if prefix ^ temp in prefixes:
                    max = temp
                    break
        return max
```

**Mark:** 129 ms


# Additional
