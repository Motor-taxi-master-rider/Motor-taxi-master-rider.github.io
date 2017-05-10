---
layout: post
title: LeetCode - Reverse Words in a String III
tags:
- Python
- LeetCode
- Python_map
categories: Python
description: Given a string, you need to reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.
---


# Description

Given a string, you need to reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.

**Example 1:**

```
Input: "Let's take LeetCode contest"
Output: "s'teL ekat edoCteeL tsetnoc"
```

**Note:** In the string, each word is separated by single space and there will not be any extra space in the string.

[Source link](https://leetcode.com/problems/reverse-words-in-a-string-iii/#/description)

__________
# Most popular solution

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        return " ".join(map(lambda x: x[::-1], s.split()))
```

__________
# My solution

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        string = ''
        for item in s.split():
            string += (item[::-1] + ' ')
        return string[:-1]
```

**Mark:** 38%

__________
# Additional
