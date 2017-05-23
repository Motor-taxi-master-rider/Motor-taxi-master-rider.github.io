---
layout: post
title: LeetCode - Detect Capital
tags:
- Python
- C++
- Re
- String
categories:
- Python
- C++
description: Given a word, you need to judge whether the usage of capitals in it is right or not.
---


# Description

Given a word, you need to judge whether the usage of capitals in it is right or not.

We define the usage of capitals in a word to be right when one of the following cases holds:

1. All letters in this word are capitals, like "USA".
2. All letters in this word are not capitals, like "leetcode".
3. Only the first letter in this word is capital if it has more than one letter, like "Google".

Otherwise, we define that this word doesn't use capitals in a right way.

**Example 1:**

```
Input: "USA"
Output: True
```

***Example 2:***

```
Input: "FlaG"
Output: False
```


**Note:** The input will be a **non-empty word** consisting of uppercase and lowercase latin letters.

[Source link](https://leetcode.com/problems/detect-capital/#/description)

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


>利用正则表达式写的标准匹配程序。

Python version v1 - Re solution

```python
class Solution(object):
    def detectCapitalUse(self, word):
        """
        :type word: str
        :rtype: bool
        """
        return True if re.match(r'[A-Z]+$|[a-z]+$|[A-Z][a-z]*$', word) else False
```

**Mark:** 45ms

***


>看了其他小伙子的代码之后发现python有自己定义的方法匹配题目所述的三钟string的情况，便有了以下代码。

Python version v2 - Bulit in solution

```python
class Solution(object):
    def detectCapitalUse(self, word):
        """
        :type word: str
        :rtype: bool
        """
        return  word.isupper() or word.istitle() or word.islower()
```

**Mark:** 38ms


__________
# Additional

[LeetCode - Keyboard Row](https://motor-taxi-master-rider.github.io/python/2016/05/10/Keyboard-Row)
