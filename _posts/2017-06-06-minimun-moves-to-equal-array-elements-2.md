---
layout: post
title: LeetCode - Minimum Moves to Equal Array Elements II
tags:
- C++
- Math
- Vector
categories:
- C++
description: Given a non-empty integer array, find the minimum number of moves required to make all array elements equal, where a move is incrementing a selected element by 1 or decrementing a selected element by 1.
---


# Description
Given a **non-empty** integer array, find the minimum number of moves required to make all array elements equal, where a move is incrementing a selected element by 1 or decrementing a selected element by 1.

You may assume the array's length is at most *10,000*.

**Example:**

```
**Input:**
[1,2,3]

**Output:**
2

**Explanation:**
Only two moves are needed (remember each move increments or decrements one element):

[1,2,3]  =>  [2,2,3]  =>  [2,2,2]
```

[Source link](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/#/description)

__________

# Best practice

>我咋觉得昨天的比较复杂。
需要用到algorithms库的sort函数。中间序号的数的值为数列的目标变化值。Minimum moves等于所有元素与该目标变化值的差值之和。

C++

```c++
class Solution {
public:
	int minMoves2(vector<int>& nums) {
		sort(nums.begin(),nums.end());
		int mid = nums[floor(nums.size()/2)];
		int result = 0;
		for (auto i:nums) {
			result += abs(i-mid);
		}
		return result;
	}
};
```

**Mark:** 19ms
__________
# Additional
