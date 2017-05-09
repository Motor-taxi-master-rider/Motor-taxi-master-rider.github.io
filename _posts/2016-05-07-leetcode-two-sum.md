---
layout: post
title: LeetCode - Two Sum
tags:
- Python
- LeetCode
- Algorithms
- Array
categories: Python
description: Jacman 是一款扁平化，有着响应式设计的 Jekyll 主题。本站正式使用了 Jacman 主题。Jacman 基于 Jacman 的 Hexo 主题修改而来。你可以前往本站和 Demo 预览更多关于本主题的更多效果。如果你有任何问题或意见欢迎到 GitHub 发表 issue。
---

> Description

Given an array of integers, return **indices** of the two numbers such that they add up to a specific target.

You may assume that each input would have **exactly** one solution, and you may not use the same element twice.

Example:
```
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

<!-- more -->
Subscribe to see which companies asked this question.

[Source page](https://leetcode.com/problems/two-sum/#/description)

<!-- more -->
> Most popular solution

```
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if len(nums) <= 1:
            return False
        dict = {}
        for i in range(len(nums)):
            if nums[i] in dict:
                return [dict[nums[i]], i]
            else:
                dict[target - nums[i]] = i
```

**Mark:** 84%


> My solution

```
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        length = len(nums)
        num_temp = sorted(range(length), key=lambda k: nums[k])     #排序前的数组序号
        nums.sort()
        i = 0
        j = length - 1
        while 1:
            sumed = nums[i] + nums[j]
            if sumed > target:
                j -= 1
            elif sumed < target:
                i += 1
            else:
                return [num_temp[i], num_temp[j]]
```

**Mark:** 86%
