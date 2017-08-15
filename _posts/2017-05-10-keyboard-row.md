---
layout: post
title: LeetCode - Keyboard Row
tags:
- LeetCode
- Re
categories:
- Python
description: Given a List of words, return the words that can be typed using letters of alphabet on only one row's of American keyboard like the image below.
---


# Description
Given a List of words, return the words that can be typed using letters of alphabet on only one row's of American keyboard like the image below.

<img src="/{{ site.assets }}/img/_keyboard_row_1.png"  title="{{site.title }}"/>

**Example 1:**

```
Input: ["Hello", "Alaska", "Dad", "Peace"]
Output: ["Alaska", "Dad"]
```

**Note:**
1. You may use one character in the keyboard more than once.
2. You may assume the input string will only contain letters of alphabet.

[Source link](https://leetcode.com/problems/keyboard-row/#/description)

__________

# My solution

```python
class Solution(object):
    def findWords(self, words):
        return list(filter(re.compile(r'(?i)^([qwertyuiop]+|[asdfghjkl]+|[zxcvbnm]+)$'). match, words))

```

__________
# Additional

[**Regular Expression**](https://docs.python.org/3/library/re.html)
