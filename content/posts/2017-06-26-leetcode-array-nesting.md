---
layout: post
title: LeetCode - Array Nesting
tags: LeetCode,List
category: Python
---


### Description
A zero-indexed array A consisting of N different integers is given. The array contains all integers in the range [0, N - 1].
Sets S[K] for 0 <= K < N are defined as follows:
S[K] = { A[K], A[A[K]], A[A[A[K]]], ... }.
Sets S[K] are finite for each K and should NOT contain duplicates.
Write a function that given an array A consisting of N integers, return the size of the largest set S[K] for this array.

**Example 1:**
```
Input: A = [5,4,0,3,1,6,2]
Output: 4
Explanation:
A[0] = 5, A[1] = 4, A[2] = 0, A[3] = 3, A[4] = 1, A[5] = 6, A[6] = 2.

One of the longest S[K]:
S[0] = {A[0], A[5], A[6], A[2]} = {5, 6, 2, 0}
```

**Note:**
1. N is an integer within the range [1, 20,000].
2. The elements of A are all distinct.
3. Each element of array A is an integer within the range [0, N-1].


[Source link](https://leetcode.com/problems/array-nesting/#/description)


### Best practice

>这里用到了一个之前用过的入栈遍历方式，取max时候的运算还可以进行优化。

Python version 1

```python
class Solution(object):
    def arrayNesting(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        length=len(nums)
        def helper(stack):
            for item in stack:
                #忽略被标记的元素
                if nums[item] < length:
                    stack.append(nums[item])
                    #将所有遍历过的元素的序号+length做唯一标记
                    nums[item] += length
            return len(stack) - 1
        #遍历所有未被标记的元素
        return max([helper([item]) for item in nums if item <length])
```

**Mark:** 85ms

----
>这是一个比较普适性的方法，创建一个记录列表。

python version 2

```python
class Solution(object):
    def arrayNesting(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        ans, step, n = 0, 0, len(nums)
        seen = [False] * n
        for i in range(n):
            while not seen[i]:
                seen[i] = True
                i, step = nums[i], step + 1
            ans = max(ans, step)
            step = 0
        return ans
```

**Mark:** 85ms

### Additional
