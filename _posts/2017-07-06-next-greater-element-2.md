---
layout: post
title: LeetCode - Construct the Rectangle
tags:
- LeetCode
- Stack
- Circular_array
categories:
- Python
description: Given a circular array (the next element of the last element is the first element of the array), print the Next Greater Number for every element. The Next Greater Number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, output -1 for this number.
---


# Description
Given a circular array (the next element of the last element is the first element of the array), print the Next Greater Number for every element. The Next Greater Number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, output -1 for this number.

**Example 1:**
```
Input: [1,2,1]
Output: [2,-1,2]
Explanation: The first 1's next greater number is 2;
The number 2 can't find next greater number;
The second 1's next greater number needs to search circularly, which is also 2.
```

**Note:** The length of given array won't exceed 10000.

[Source link](https://leetcode.com/problems/next-greater-element-ii/#/description)


# Best practice

>TBD

C++ version -- TBD

```c++

```

**Mark:** 0ms

----

>使用栈来判断各个元素next greater的元素。用1至2n序号以及取余的方法来遍历两遍列表，模拟循环数组的情况

python version

```python
class Solution(object):
    def nextGreaterElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
				length = len(nums)
			    stack, res = [], [-1] * length
			    for i in range(length * 2):
			        #如果出现大于栈顶序号得元素值的元素时，
			        #就可以疯狂出掉所有小于该元素的所有元素序号
			        while stack and (nums[stack[-1]] < nums[i % length]):
			            res[stack.pop()] = nums[i % length]
			        #仅仅将每个元素的序号入栈一次
			        if i < length:
			            stack.append(i)
			    return res
```

**Mark:** 275ms

# Additional
