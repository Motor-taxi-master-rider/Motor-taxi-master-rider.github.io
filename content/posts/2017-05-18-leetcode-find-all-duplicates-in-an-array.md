---
layout: post
title: LeetCode - Find All Duplicates in an Array
tags: LeetCode,Consecutive
category: Python,C
---


### Description
Given an array of integers, 1 ≤ a[i] ≤ n (n = size of array), some elements appear **twice** and others appear **once**.

Find all the elements that appear **twice** in this array.

Could you do it without extra space and in O(n) runtime?

**Example:**

```
Input:
[4,3,2,7,8,2,3,1]

Output:
[2,3]
```

[Source link](https://leetcode.com/problems/find-all-duplicates-in-an-array/#/description)

__________

### Best practice

> 数列有两个特征：一是长度为n的数列只会由1到n的数字组成，二是重复数量不超过两次。对于任意一个数列元素i，序号i-1必定存在且唯一，因此我们可以用数列的序号使数列本身成为一个存放已匹配到数字的哈希表——当匹配元素值时，将其对应的序号的元素值设为负数。

C++ version

```c++
class Solution {
public:
	vector<int> findDuplicates(vector<int>& nums) {
		vector<int> res;
		for (int i = 0; i < nums.size(); i++) {
			int index = abs(nums[i]) - 1;
			if (nums[index] < 0) {
				res.push_back(abs(nums[i]));
			}
			else {
				nums[index] = -nums[index];
			}
		}
		return res;
	}
};
```

**Mark:** 139ms

****

Python version

```python
class Solution(object):
    def findDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        res = []
        for x in nums:
            if nums[abs(x)-1] < 0:
                res.append(abs(x))
            else:
                nums[abs(x)-1] *= -1
            print(nums)
        return res
```

**Mark:** 365ms

__________
### Additional

[Find duplicates in O(n) time and O(1) extra space](http://www.geeksforgeeks.org/find-duplicates-in-on-time-and-constant-extra-space/)
