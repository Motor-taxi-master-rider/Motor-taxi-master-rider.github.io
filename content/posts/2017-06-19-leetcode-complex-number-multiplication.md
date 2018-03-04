---
layout: post
title: Complex Number Multiplication
tags: LeetCode,Re,Stringstream
category: C,Python
---


### Description
Given two strings representing two complex numbers.
You need to return a string representing their multiplication. Note $$i^2 = -1$$ according to the definition.

**Example 1:**

```
Input: "1+1i", "1+1i"
Output: "0+2i"
Explanation: (1 + i) * (1 + i) = 1 + i2 + 2 * i = 2i, and you need convert it to the form of 0+2i.
```

**Example 2:**

```
Input: "1+-1i", "1+-1i"
Output: "0+-2i"
Explanation: (1 - i) * (1 - i) = 1 + i2 - 2 * i = -2i, and you need convert it to the form of 0+-2i.
```

**Note:**
1. The input strings will not have extra blank.
2. The input strings will be given in the form of `a+bi`, where the integer `a` and `b` will both belong to the range of [-100, 100]. And **the output should be also in this form.**

[Source link](https://leetcode.com/problems/complex-number-multiplication/#/description)


### Best practice

>在c++中使用Stringstream来提取字符串中的信息。

C++ version

```c++
class Solution {
public:
    string complexNumberMultiply(string a, string b) {
        int ra, ia, rb, ib;
        char buff;
        stringstream aa(a), bb(b), ans;
        aa >> ra >> buff >> ia >> buff;
        bb >> rb >> buff >> ib >> buff;
        ans << ra*rb - ia*ib << "+" << ra*ib + rb*ia << "i";
        return ans.str();
    }
};
```

**Mark:**

----

Python version -- use re

```python
class Solution(object):
    def complexNumberMultiply(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        pattern = re.compile(r'([\-0-9]*)\+([\-0-9]*)i')

        la = [int(item) for item in pattern.search(a).groups()]
        lb = [int(item) for item in pattern.search(b).groups()]
        lc = [la[0] * lb[0] - la[1] * lb[1], la[0] * lb[1] + la[1] * lb[0]]
        return '{}+{}i'.format(*lc)
```

**Mark:** 36ms

### Additional
