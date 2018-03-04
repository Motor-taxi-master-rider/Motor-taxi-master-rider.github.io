---
layout: post
title: LeetCode - Find Largest Value in Each Tree Row
tags: LeetCode,Tree
category: Python,C
---


### Description
You need to find the largest value in each row of a binary tree.

**Example:**

```
Input:

          1
         / \
        3   2
       / \   \  
      5   3   9

Output: [1, 3, 9]
```

[Source link](https://leetcode.com/problems/find-largest-value-in-each-tree-row/#/description)

__________

### Best practice

>设树根为第0层，则第i层的最大值等于结果集result[i]。遍历每一层比较相同序号的根值的最大值。

C++ version

```c++
#include <iostream>
#include <vector>
#include <algorithm>
class Solution {
	vector<int> result;
public:
	vector<int> largestValues(TreeNode* root) {
		helper(root, 0);
		return result;
	}

	void helper(TreeNode* node, int level) {
		if (!node) return;
		if (result.size() <= level ) {
			result.push_back(node->val);
		}
		else {
			result[level] = max(result[level],node->val);
		}
		helper(node->left, level + 1);
		helper(node->right, level + 1);
	}
};
```

**Mark:** 12ms

****

> 本题先生成一行中的所有元素，之后再比较出最大值。

Python version

```python
class Solution(object):
    def largestValues(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        lst = []
        child = [root]
        while any(child):
            lst.append(max([item.val for item in child]))
            child=[item for node in child for item in filter(None,(node.left,node.right))]
        return lst
```

**Mark:** 96ms

__________
### Additional

[C++指针详解](http://www.cnblogs.com/ggjucheng/archive/2011/12/13/2286391.html)
