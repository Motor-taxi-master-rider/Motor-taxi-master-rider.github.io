---
layout: post
title: LeetCode - Merge Two Binary Trees
tags:
- LeetCode
- Tree
- Recursion
categories:
- C++
description: Given two binary trees and imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not.
---


# Description
Given two binary trees and imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not.

You need to merge them into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of new tree.

**Example 1:**

```
Input:
	Tree 1                     Tree 2                  
          1                         2                             
         / \                       / \                            
        3   2                     1   3                        
       /                           \   \                      
      5                             4   7    

Output:
Merged tree:
	     3
	    / \
	   4   5
	  / \   \
	 5   4   7
```

**Note:** The merging process must start from the root nodes of both trees.
[Source link](https://leetcode.com/problems/merge-two-binary-trees/#/description)


# Best practice

>用递归的方法来合并两树：如果一树任意节点不存在则返回另一个树的节点（如果都为空则返回一个空节点，很合理）。如果都存在则生成新节点其值为两树节点值得和。
TreeNode \*node =new TreeNode(t1->val + t2->val); 返回一个TreeNode指针。

C++ version

```c++
class Solution {
public:
	TreeNode* mergeTrees(TreeNode* t1, TreeNode* t2) {
		if (!t1) return t2;
		if (!t2) return t1;
		TreeNode *node =new TreeNode(t1->val + t2->val);
		node->left = mergeTrees(t1->left,t2->left);
		node->right= mergeTrees(t1->right, t2->right);
		return node;
	}
};
```

**Mark:** 10ms

# Additional
