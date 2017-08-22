---
layout: post
title: LeetCode - Move Zeroes
tags:
- LeetCode
- List
categories:
- C
- Python
description: Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.
---


# Description
Given an array `nums`, write a function to move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

For example, given `nums = [0, 1, 0, 3, 12]`, after calling your function, `nums` should be `[1, 3, 12, 0, 0]`.

Note:
1. You must do this **in-place** without making a copy of the array.
2. Minimize the total number of operations.


[Source link](https://leetcode.com/problems/move-zeroes/#/description)


# Best practice

>每当遇到一个0位就将之后的数字向前移动x位（x为遇到的0的个数），最后将后x位置为0。

C++ version

```c++
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int count=0;
        for(int i=0;i<nums.size();++i){
            if(nums[i]==0){
                ++count;
            }else{
                nums[i-count]=nums[i];
            }
        }
        for(int i=0;i<count;++i){
            nums[nums.size()-1-i]=0;
        }
    }
};
```

**Mark:** 16ms

----
>用一个变量j来记录非0位应在的位置，最后处理末置0位。

python version

```python
class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        j = 0
        for item in nums:
            if item != 0:
                nums[j] = item
                j += 1
        for index in range(j, len(nums)):
            nums[index] = 0
```

**Mark:** 59ms

# Additional
