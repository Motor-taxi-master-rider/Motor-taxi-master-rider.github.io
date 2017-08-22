---
layout: post
title: LeetCode - Replace Words
tags:
- LeetCode
- Tire
- Defaultdict
- Lambda
categories:
- Python
description: In English, we have a concept called root, which can be followed by some other words to form another longer word - let's call this word successor. For example, the root an, followed by other, which can form another word another.
---


# Description
In English, we have a concept called `root`, which can be followed by some other words to form another longer word - let's call this word `successor`. For example, the root `an`, followed by `other`, which can form `another` word another.

Now, given a dictionary consisting of many roots and a sentence. You need to replace all the `successor` in the sentence with the `root` forming it. If a `successor` has many `roots` can form it, replace it with the root with the shortest length.

You need to output the sentence after the replacement.

**Example 1:**
```
Input: dict = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

**Note:**
1. The input will only have lower-case letters.
2. 1 <= dict words number <= 1000
3. 1 <= sentence words number <= 1000
4. 1 <= root length <= 100
5. 1 <= sentence words length <= 1000

[Source link](https://leetcode.com/problems/replace-words/description/)


# Best practice

>在这里用到的数据结构是Tire树。
Trie树，即字典树，又称单词查找树或键树，是一种树形结构，是一种哈希树的变种。典型应用是用于统计和排序大量的字符串（但不仅限于字符串），所以经常被搜索引擎系统用于文本词频统计。它的优点是：最大限度地减少无谓的字符串比较，查询效率比哈希表高。
Trie的核心思想是空间换时间。利用字符串的公共前缀来降低查询时间的开销以达到提高效率的目的。


python version

```python
from collections import defaultdict
import functools


class Solution(object):
    def replaceWords(self, dict, sentence):
        """
        :type dict: List[str]
        :type sentence: str
        :rtype: str
        """
        IS_WORD = True  #Tire树中表示节点为单词末字母的标识符，这里额外存储完整单词

        def generateTire(dct):
            #这是一个很强大的递归生成defaultdict树的表达式
            _tire = lambda: defaultdict(_tire)
            tire = _tire()
            for word in dct:
                node = tire
                for char in word:
                    node = node[char]
                node[IS_WORD] = word
            return tire

        def searchWord(tire, word):
            #在tire树种查找到最短的单词successor，这里
            #只要遇到IS_WORD键就返回查到的单词
            node = tire
            for char in word:
                if char not in node: break
                node = node[char]
                if IS_WORD in node:
                    return node[IS_WORD]
            return word

        #利用partial方法构造map函数
        replace = functools.partial(searchWord, generateTire(dict))
        return " ".join(map(replace, sentence.split()))
```

**Mark:** 116 ms


# Additional
