---
layout: post
title: LeetCode - Queue Reconstruction by Height
tags: Python,LeetCode,Stack
category: Python
---


### Description
Suppose you have a random list of people standing in a queue. Each person is described by a pair of integers `(h, k)`, where `h` is the height of the person and `k` is the number of people in front of this person who have a height greater than or equal to `h`. Write an algorithm to reconstruct the queue.

**Example:**

```
Input:
[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]

Output:
[[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]
```

**Note:**

The number of people is less than 1,100.

[Source link](https://leetcode.com/problems/queue-reconstruction-by-height/#/description)

__________

### Most popular



__________


### My solution

1. 先将列表以h DEC, k ASC排序

2. 将元素一一入栈, 若 k > 栈深, 则无解; 否则插入到列表的位置k

```python
class Solution(object):
    def reconstructQueue(self, people):
        """
        :type people: List[List[int]]
        :rtype: List[List[int]]
        """
        stack = []
        for item in sorted(people, key=lambda x: (-x[0], x[1])):
            if len(stack) < item[1]:
                return False
            stack.insert(item[1], item)
        return stack
```

__________
### Additional
