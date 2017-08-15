---
layout: post
title: LeetCode - Beautiful Arrangement
tags:
- LeetCode
- Backtracking
- DFS
categories:
- Python
- C
description: Suppose you have N integers from 1 to N...
---


# Description
Suppose you have **N** integers from 1 to N. We define a beautiful arrangement as an array that is constructed by these N numbers successfully if one of the following is true for the i<sub>th</sub> position (`1 ≤ i ≤ N`) in this array:

1. The number at the i<sub>th</sub> position is divisible by **i**.
2. **i** is divisible by the number at the i<sub>th</sub> position.

Now given N, how many beautiful arrangements can you construct?

**Example 1:**

```
Input: 2
Output: 2
Explanation:

The first beautiful arrangement is [1, 2]:

Number at the 1st position (i=1) is 1, and 1 is divisible by i (i=1).

Number at the 2nd position (i=2) is 2, and 2 is divisible by i (i=2).

The second beautiful arrangement is [2, 1]:

Number at the 1st position (i=1) is 2, and 2 is divisible by i (i=1).

Number at the 2nd position (i=2) is 1, and i (i=2) is divisible by 1.

Note:

N is a positive integer and will not exceed 15.
```

[Source link](https://leetcode.com/problems/beautiful-arrangement/#/description)

__________

# Most popular

C++ version

```c++
class Solution {
public:
    int countArrangement(int N) {
        vector<int> vs;
        for (int i=0; i<N; ++i) vs.push_back(i+1);
        return counts(N, vs);
    }
    int counts(int n, vector<int>& vs) {
        if (n <= 0) return 1;
        int ans = 0;
        for (int i=0; i<n; ++i) {
            if (vs[i]%n==0 || n%vs[i]==0) {
                swap(vs[i], vs[n-1]);
                ans += counts(n-1, vs);
                swap(vs[i], vs[n-1]);
            }
        }
        return ans;
    }
};
```

**Mark:** 6ms

__________


# My solution

C++ version

```c++
class Solution {
public:
	int count = 0;
	int size = 0;
	int countArrangement(int N) {
		vector<int> vs;
		if (N == 0) return 0;
		for (int i = 0; i < N; ++i) vs.push_back(0);
		size = N;
		helper(N, vs);
		return count;
	}
	void helper(int n, vector<int> &vs) {
		if (n <= 0) {     //边界条件
			count++;
			return;
		}
		for (int i = size - 1; i >= 0; --i) {
			if ((vs[i] == 0) && ((i + 1) % n == 0 || n % (i + 1) == 0)) {    //剪枝
				vs[i] = 1;
				helper(n - 1, vs);
				vs[i] = 0;
			}
		}
	}
};
```

**Mark:** 16ms

****

DP Python version of leetcode user

```python
cache = {}
class Solution(object):
    def countArrangement(self, N):
        def helper(i, X):
            if i == 1:
                return 1
            key = (i, X)
            if key in cache:
                return cache[key]
            total = 0
            for j in range(len(X)):
                if X[j] % i == 0 or i % X[j] == 0:
                    total += helper(i - 1, X[:j] + X[j + 1:])
            cache[key] = total   #用哈希表来储存(位置,([剩余元素])):配对数量 信息
            return total
        return helper(N, tuple(range(1, N + 1)))
```

**Mark:** 66ms

__________
# Additional

**回溯算法介绍:**

[https://segmentfault.com/a/1190000006121957](https://segmentfault.com/a/1190000006121957)
