---
layout: post
title: LeetCode - Hamming Distance
tags:
- Python
- LeetCode
- Algorithms
- Hamming Distance
- Python Bit Manipulation
categories: Python
description: The Hamming distance between two integers is the number of positions at which the corresponding bits are different.Given two integers x and y, calculate the Hamming distance.
---

> Description

The [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between two integers is the number of positions at which the corresponding bits are different.

Given two integers x and y, calculate the Hamming distance.

-**Note:**
0 ≤ x, y < 231.

-**Example:**
```
Input: x = 1, y = 4

Output: 2

Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑

The above arrows point to positions where the corresponding bits are different.
```

[Source link](https://leetcode.com/problems/hamming-distance/#/description)

<!-- more -->
> Most popular solution

```
class Solution(object):
    def hammingDistance(self, x, y):
      """
      :type x: int
      :type y: int
      :rtype: int
      """
      return bin(x^y).count('1')
```
使用了bin函数将


> My solution

```
class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        bit = x ^ y
        count = 0
        while bit:
            if bit & 1 == 1:
                count += 1
            bit = bit >> 1
        return count
```

**Mark:** 97%

> Additional

-**Hamming distance**

在信息论中，两个等长字符串之间的**汉明距离**(Hamming distance）是两个字符串对应位置的不同字符的个数。换句话说，它就是将一个字符串变换成另外一个字符串所需要替换的字符个数。

**汉明重量**是字符串相对于同样长度的零字符串的汉明距离，也就是说，它是字符串中非零的元素个数：对于二进制字符串来说，就是1的个数，所以11101的汉明重量是4。

-**Python 位运算**

*按位与:* &

*按位或:* |

*按位异或:* ^

*按位翻转:* ~       +1 之后乘以 -1

*左移运算符* <<      X<<N 将一个数字X向左移动N位

*右移运算符* >>       
