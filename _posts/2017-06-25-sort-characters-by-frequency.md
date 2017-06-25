---
layout: post
title: LeetCode - Sort Characters By Frequency
tags:
- LeetCode
- Hashtable
- String
categories:
- C++
- Python
description: Given a string, sort it in decreasing order based on the frequency of characters.
---


# Description
Given a string, sort it in decreasing order based on the frequency of characters.

**Example 1:**
```
Input:
"tree"

Output:
"eert"

Explanation:
'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
```

**Example 2:**
```
Input:
"cccaaa"

Output:
"cccaaa"

Explanation:
Both 'c' and 'a' appear three times, so "aaaccc" is also a valid answer.
Note that "cacaca" is incorrect, as the same characters must be together.
```

**Example 3:**
```
Input:
"Aabb"

Output:
"bbAa"

Explanation:
"bbaA" is also a valid answer, but "Aabb" is incorrect.
Note that 'A' and 'a' are treated as two different characters.
```
[Source link](https://leetcode.com/problems/sort-characters-by-frequency/#/description)


# Best practice

>使用队列。

C++ version

```c++
class Solution {
public:
    string frequencySort(string s) {
        vector<int> m(256, 0);
        priority_queue<pair<int, char> > pq;
        for(int i = 0; i < s.length(); i++)
            m[s[i]]++;
        for(int i =0; i < 256; i++)
            pq.push(make_pair(m[i], i));
        string ans;
        while(pq.size()){
            ans.append(pq.top().first, pq.top().second);
            pq.pop();
        }
        return ans;
    }
};
```

**Mark:** 12ms

----
>python版本使用了sorted函数并通过opterator库的itemgetter函数来提高检索字典效率。string乘法则是python的另一个特性。

python version

```python
from operator import itemgetter

class Solution(object):
    def frequencySort(self, s):
        """
        :type s: str
        :rtype: str
        """
        dct = {}
        result = ""
        for item in s:
            dct[item] = dct.get(item, 0) + 1
        for item in sorted(dct.items(), key=itemgetter(1), reverse=True):
            result += item[0] * item[1]
        return result
```

**Mark:** 76ms

# Additional
