---
layout: post
title: LeetCode - Find Bottom Left Tree Value
tags:
- Python
- LeetCode
- Tree
categories: Python
description: Given a binary tree, find the leftmost value in the last row of the tree.
---


# Description

Given a binary tree, find the leftmost value in the last row of the tree.

**Example 1:**

```
Input:

    2
   / \
  1   3

Output:
1
```

**Example 2:**

```
Input:

        1
       / \
      2   3
     /   / \
    4   5   6
       /
      7

Output:
7
```

**Note:** You may assume the tree (i.e., the given root node) is not NULL.

[Source link](https://leetcode.com/problems/find-bottom-left-tree-value/#/description)

__________
# Most popular solution

```python
class Solution(object):
  def findLeftMostNode(self, root):
    queue = [root]
    for node in queue:
        queue += filter(None, (node.right, node.left))
    return node.val
```

__________
# My solution



__________
# Additional

**It's leftmost in last row not left left node**
