---
layout: post
title: LeetCode - Total Hamming Distance
tags: Leetcode,Hamming_distance,Bit_manipulaion
category: Python
---


### Description
The Hamming distance between two integers is the number of positions at which the corresponding bits are different.
Now your job is to find the total Hamming distance between all pairs of the given numbers.

**Example:**

```
Input: 4, 14, 2

Output: 6

Explanation: In binary representation, the 4 is 0100, 14 is 1110, and 2 is 0010 (just
showing the four bits relevant in this case). So the answer will be:
HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2) = 2 + 2 + 2 = 6.
```

**Note:**
1. Elements of the given array are in the range of `0` to `10^9`
2. Length of the array will not exceed `10^4`.

[Source link](https://leetcode.com/problems/total-hamming-distance/description/)


### Best practice

>经过观察可以发现，所有列表中元素的汉明距离也可以用他们各个位中的0和1的分布情况来得出。例如共有八个元素，所有元素的2^0位有三个1五个0，则该位对整体汉明距离的贡献为3*5。本题中所描述的total hamming distance可以由所有位产生的汉明距离的和表示。这样的平均时间复杂度位O(n*m),m为元素二进制位平均长度。


python version

```python
from collections import defaultdict


class Solution(object):
    def totalHammingDistance(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result = 0
        for i in range(32):
            count = 0  # 列表中所有元素第i位中的1的数量
            bit = (1 << i)  # 参照二进制数
            for item in nums:
                if item & bit:
                    count += 1
            result += count * (len(nums) - count)
        return result
```

**Mark:** 268 ms


### Additional
