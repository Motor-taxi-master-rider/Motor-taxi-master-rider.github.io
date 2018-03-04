---
layout: post
title: LeetCode - Most Frequent Subtree Sum
tags: Tree,Array
category: Python,C
---


### Description
Given the root of a tree, you are asked to find the most frequent subtree sum. The subtree sum of a node is defined as the sum of all the node values formed by the subtree rooted at that node (including the node itself). So what is the most frequent subtree sum value? If there is a tie, return all the values with the highest frequency in any order.

**Examples 1**

```
Input:

  5
 /  \
2   -3
```

return [2, -3, 4], since all the values happen only once, return all of them in any order.

**Examples 2**

```
Input:

  5
 /  \
2   -5
```

return [2], since 2 happens twice, however -5 only occur once.

**Note:** You may assume the sum of values in any subtree is in the range of 32-bit signed integer.

[Source link](https://leetcode.com/problems/most-frequent-subtree-sum/#/description)

__________

### Best practice

>C++的reg有点慢啊!

C++ reg verison

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
private:
    unordered_map<int, int> mp;
    int max = 0;
public:
    vector<int> findFrequentTreeSum(TreeNode* root) {
        vector<pair<int, int>> v;
        vector<int> res;

        calSum(root);
        for (auto& it : mp)
            if (it.second == max)
                res.push_back(it.first);

        return res;
    }

    int calSum(TreeNode* root) {
        if (root == NULL)   return 0;
        int k;

        k = root->val + calSum(root->left) + calSum(root->right);
        mp[k]++;
        max = max < mp[k] ? mp[k] : max;
        return k;
    }
};
```

**Mark:** 12ms

****


>普通的dfs遍历,遍历的同时保存最大值出现次数。

Python version - dfs

```python
class Solution(object):
    count = 0

    def findFrequentTreeSum(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        dic = {}
        self.helper(root, dic)
        return [item for item in dic.keys() if dic[item]==self.count]

    def helper(self, node, dic):
        if not node:
            return 0
        sums = node.val + self.helper(node.left, dic) + self.helper(node.right, dic)
        dic[sums] = dic.get(sums, 0) + 1
        self.count = max(self.count, dic[sums])
        return sums
```

**Mark:** 78ms

__________
### Additional
