---
layout: post
title: LeetCode - Add One Row to Tree
tags: LeetCode,Tree,Recursion
category: C,Python
---


### Description
Given the root of a binary tree, then value `v` and depth `d`, you need to add a row of nodes with value `v` at the given depth `d`. The root node is at depth 1.
The adding rule is: given a positive integer depth `d`, for each NOT null tree nodes `N` in depth `d-1`, create two tree nodes with value `v` as `N's` left subtree root and right subtree root. And `N's` **original left subtree** should be the left subtree of the new left subtree root, its **original right subtree** should be the right subtree of the new right subtree root. If depth `d` is 1 that means there is no depth `d-1` at all, then create a tree node with value `v `as the new root of the whole original tree, and the original tree is the new root's left subtree.

**Example 1:**
```
Input:
A binary tree as following:
       4
     /   \
    2     6
   / \   /
  3   1 5   

v = 1

d = 2

Output:
       4
      / \
     1   1
    /     \
   2       6
  / \     /
 3   1   5   
```

**Example 2:**
```
Input:
A binary tree as following:
      4
     /   
    2    
   / \   
  3   1    

v = 1

d = 3

Output:
      4
     /   
    2
   / \    
  1   1
 /     \  
3       1
```
**Note:**
1. The given d is in range [1, maximum depth of the given tree + 1].
2. The given binary tree has at least one tree node.

[Source link](https://leetcode.com/problems/add-one-row-to-tree/#/description)


### Best practice

>题目中d=1时实为一种特殊情况————整颗树变为左子树。相似的当d=0时整棵树相应会变成右子树嘛。以此推理可以得以下终极解决方法。将d=0和d=1作为递归终止条件从而将d=1的特殊情况概化，又省去了helper函数。

C++ version

```c++
class Solution {
public:
    TreeNode* addOneRow(TreeNode* root, int v, int d) {
        if (d == 0 || d == 1) {
            TreeNode* newroot = new TreeNode(v);
            (d ? newroot->left : newroot->right) = root;
            return newroot;
        }
        if (root && d >= 2) {
            root->left  = addOneRow(root->left,  v, d > 2 ? d - 1 : 1);
            root->right = addOneRow(root->right, v, d > 2 ? d - 1 : 0);
        }
        return root;
    }
};
```

**Mark:** 16ms

----
>这个python版本显得非常不pythonic。helper函数增加了一个长度参数记录了递归树深度，其实可以用使参数d递减的方式来传递深度。

python version

```python
### Definition for a binary tree node.
### class TreeNode(object):
###     def __init__(self, x):
###         self.val = x
###         self.left = None
###         self.right = None

class Solution:
    def addOneRow(self, root, v, d):
        """
        :type root: TreeNode
        :type v: int
        :type d: int
        :rtype: TreeNode
        """
        if d == 1:
            a = TreeNode(v)
            a.left = root
            return a
        return self.helper(root, v, d, 1)

    def helper(self, node, v, d, dep):
        if not node:
            return
        if dep == d - 1:
            a = TreeNode(v)
            b = TreeNode(v)
            a.left = node.left
            b.right = node.right
            node.left = a
            node.right = b
        self.helper(node.left, v, d, dep + 1)
        self.helper(node.right, v, d, dep + 1)
        return node
```

**Mark:** 82ms

### Additional
