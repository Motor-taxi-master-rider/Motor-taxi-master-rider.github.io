---
layout: post
title: LeetCode - Max Consecutive Ones
tags:
- Python
- C++
- LeetCode
- Consecutive
categories:
- Python
- C++
description: Given a binary array, find the maximum number of consecutive 1s in this array.
---


# Description
Given a binary array, find the maximum number of consecutive 1s in this array.

**Example 1:**

```
Input: [1,1,0,1,1,1]
Output: 3
Explanation: The first two digits or the last three digits are consecutive 1s.
    The maximum number of consecutive 1s is 3.
```

**Note:**

1. The input array will only contain 0 and 1.
2. The length of input array is a positive integer and will not exceed 10,000

[Source link](https://leetcode.com/problems/max-consecutive-ones/#/description)

__________

# Most popular



__________


# My solution

C++ version

```c++
class Solution {
public:
	int findMaxConsecutiveOnes(vector<int>& nums) {
		int cnt = 0;
		int ans = 0;
		for (int i = 0; i < nums.size(); ++i) {
			if (nums[i] == 1) {
				ans = ans > ++cnt ? ans : cnt;
			}
			else
			{
				cnt = 0;
			}
		}
		return ans;
	}
};
```

**Mark:** 2ms

****

Python version

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        lst = [-1]
        length = len(nums)
        for i in range(length):
            if nums[i] == 0:
                lst.append(i)
        lst.append(length)
        return max(map(lambda x: x[1] - x[0] - 1, zip(lst[:-1], lst[1:])))
```

**Mark:** 105ms

__________
# Additional
