---
layout: post
title: LeetCode - Convert BST to Greater Tree
tags:
- LeetCode
- BST
categories:
- Python
- C
description: Given a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus sum of all keys greater than the original key in BST.
---


# Description
Given a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus sum of all keys greater than the original key in BST.

**Example:**

```
Input: The root of a Binary Search Tree like this:
              5
            /   \
           2     13

Output: The root of a Greater Tree like this:
             18
            /   \
          20     13
```

[Source link](https://leetcode.com/problems/convert-bst-to-greater-tree/#/description)

__________

# Best practice

>利用二叉搜索树的特性，以右中左的方式遍历全树。python版本先完成，使用了全局变量记录累计值来辅助递归。C++版本则将变量加入递归,不使用全局变量。

C++ version

```c++
class Solution {
public:
	int helper(TreeNode* root, int cum) {
		if (root->right) cum = helper(root->right, cum);
		root->val = root->val + cum;
		return (root->left) ? helper(root->left, root->val) : root->val;
	}
	TreeNode* convertBST(TreeNode* root) {
		if (!root) return NULL;
		helper(root, 0);
		return root;
	}
};
```

**Mark:** 35ms

****



Python version

```python
class Solution(object):
    cum = 0
    def convertBST(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        self.helper(root)
        return root

    def helper(self, node):
        if not node:
            return
        self.helper(node.right)
        self.cum += node.val
        node.val = self.cum
        self.helper(node.left)
```

**Mark:** 178ms

__________
# Additional
