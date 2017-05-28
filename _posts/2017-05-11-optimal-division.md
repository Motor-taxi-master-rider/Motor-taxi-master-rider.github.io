---
layout: post
title: LeetCode - Optimal Division
tags:
- Python
- LeetCode
- String
categories: Python
description: Given a list of positive integers, the adjacent integers will perform the float division. For example, [2,3,4] -> 2 / 3 / 4.
---


# Description
Given a list of **positive integers**, the adjacent integers will perform the float division. For example, [2,3,4] -> 2 / 3 / 4.

However, you can add any number of parenthesis at any position to change the priority of operations. You should find out how to add parenthesis to get the **maximum** result, and return the corresponding expression in string format. **Your expression should NOT contain redundant parenthesis**.

**Example:**

```
**Input**: [1000,100,10,2]
**Output**: "1000/(100/10/2)"
**Explanation**:
1000/(100/10/2) = 1000/((100/10)/2) = 200
However, the bold parenthesis in "1000/((100/10)/2)" are redundant,
since they don't influence the operation priority. So you should return "1000/(100/10/2)".

Other cases:
1000/(100/10)/2 = 50
1000/(100/(10/2)) = 50
1000/100/10/2 = 0.5
1000/100/(10/2) = 2
```

**Note:**
1. The length of the input array is [1, 10].
2. Elements in the given array will be in range [2, 1000].
3. There is only one optimal division for each test case.

[Source link](https://leetcode.com/problems/optimal-division/#/description)

__________

# Most popular

Regardless of parentheses, every element is either in the numerator or denominator of the final fraction. The expression A[0] / ( A[1] / A[2] / ... / A[N-1] ) has every element in the numerator except A[1], and it is impossible for A[1] to be in the numerator, so it is the largest. We must also be careful with corner cases.

```python
class Solution(object):
    def optimalDivision(self, A):
        A = map(str, A)
        if len(A) <= 2: return '/'.join(A)
        return '{}/({})'.format(A[0], '/'.join(A[1:]))
```

__________


# My solution

```python
class Solution(object):
    def optimalDivision(self, nums):
        """
        :type nums: List[int]
        :rtype: str
        """
        length=len(nums)
        if length == 1:
            return str(nums[0])
        elif length == 2:
            return str(nums[0]) + "/" + str(nums[1])
        return str(nums[0]) + "/(" + "/".join(map(str, nums[1:])) + ")"
```

__________
# Additional
