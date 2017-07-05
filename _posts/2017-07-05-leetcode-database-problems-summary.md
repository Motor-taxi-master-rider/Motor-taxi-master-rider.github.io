---
layout: post
title: LeetCode - Database problems summary
tags:
- LeetCode
- Mysql
categories:
- SQL
description: Here is a summary of LeetCode Database section.
---


# Description
Here is a summary of LeetCode Database section.

[Source link](https://leetcode.com/problemset/database/)


# Best practice

>其实很简单，放上来是因为记录一下python和c各自不同的解决方式。然后c的0ms实在是太夸张了。

C++ version

```c++
class Solution {
public:
	vector<int> constructRectangle(int area) {
		int ceil = floor(sqrt(area));
		while (area%ceil != 0) {
			--ceil;
		}
		return vector<int>({ area / ceil, ceil });
	}
};
```

**Mark:** 0ms

----

python version

```python
import math

class Solution(object):
    def constructRectangle(self, area):
        """
        :type area: int
        :rtype: List[int]
        """
        for i in range(math.floor(math.sqrt(area)), 0, -1):
            if area % i == 0:
                return [int(area / i), i]
```

**Mark:** 46ms

# Additional
