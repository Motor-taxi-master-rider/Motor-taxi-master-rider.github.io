---
layout: post
title: LeetCode - Single Number
tags: LeetCode,Bit_manipulation
category: Python,C
---


### Description
Given an array of integers, every element appears **twice** except for one. Find that **single** one.

**Note:**
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

[Source link](https://leetcode.com/problems/single-number/#/description)

__________

### Best practice

>利用异或位运算消除成对出现的元素只留下那个单身元素。

C++ version

```c++
class Solution {
public:
	int singleNumber(vector<int>& nums) {
		int result = 0;
		int n = nums.size();
		for (int i = 0; i < n; ++i) {
			result = result^nums[i];
		}
		return result;
	}
};
```

**Mark:** 16ms

****



Python version

```python
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result=0
        for item in nums:
            result^=item

        return result

```

**Mark:** 45ms

__________
### Additional

[来谈谈C++ 位运算](http://www.linuxidc.com/Linux/2014-03/98362.html)
