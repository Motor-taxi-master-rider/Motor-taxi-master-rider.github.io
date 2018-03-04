---
layout: post
title: LeetCode - Invert binary tree
tags: Tree,Google
category: C
---


### Description
Invert a binary tree.

```
     4
   /   \
  2     7
 / \   / \
1   3 6   9
```

to
```
     4
   /   \
  7     2
 / \   / \
9   6 3   1
```

**Trivia:**
This problem was inspired by this original tweet by Max Howell:
>**Google: 90% of our engineers use the software you wrote (Homebrew), but you can’t invert a binary tree on a whiteboard so fuck off.**

[Source link](https://leetcode.com/problems/invert-binary-tree/#/description)

__________

### Best practice

>很容易就能想到用递归的方式，实际一做非常简单。被这个老哥怼的谷歌内心一定感到很委屈吧。

C++ -- recursion

```c++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (root!=NULL) {
            invertTree(root->left);
            invertTree(root->right);
            swap(root->left, root->right);
        }
        return root;
    }
};
```

**Mark:** 3ms

****

>这是一个用队列储存二叉树节点的非递归算法，可能会比较快一点吧。

C++ -- queue

```c++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        queue<TreeNode*> record;
        record.push(root);
        while(!record.empty()){
            TreeNode* node = record.front();
            record.pop();
            if(node != NULL){
                record.push(node->left);
                record.push(node->right);
                swap(node->left,node->right);
            }

        }
        return root;
    }
};
```

**Mark:** 0ms

__________
### Additional
