---
layout: post
title: LeetCode - Minimum Index Sum of Two Lists
tags:
- Hashtable
- Vector
categories:
- C
description: Suppose Andy and Doris want to choose a restaurant for dinner, and they both have a list of favorite restaurants represented by strings.
---


# Description
Suppose Andy and Doris want to choose a restaurant for dinner, and they both have a list of favorite restaurants represented by strings.
You need to help them find out their **common interest** with the **least list index sum**. If there is a choice tie between answers, output all of them with no order requirement. You could assume there always exists an answer.

**Example 1:**

```
Input:
["Shogun", "Tapioca Express", "Burger King", "KFC"]
["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"]
Output: ["Shogun"]
Explanation: The only restaurant they both like is "Shogun".
```

**Example 2:**

```
Input:
["Shogun", "Tapioca Express", "Burger King", "KFC"]
["KFC", "Shogun", "Burger King"]
Output: ["Shogun"]
Explanation: The restaurant they both like and have the least index sum is "Shogun" with index sum 1 (0+1).
```

**Note:**
1. The length of both lists will be in the range of [1, 1000].
2. The length of strings in both lists will be in the range of [1, 30].
3. The index is starting from 0 to the list length minus 1.
4. No duplicates in both lists.

[Source link](https://leetcode.com/problems/minimum-index-sum-of-two-lists/#/description)



# Best practice

>首先以第一个列表建一个以index为key，string为item的哈希表。
然后遍历第二个列表，当两个列表的index和比之前小时刷新输出列表，相等时在输出列表后添加第二个列表真的string。

C++ : hash table

```c++
class Solution {
public:
	int max_int = 2147483647;
	vector<string> findRestaurant(vector<string>& list1, vector<string>& list2) {
		vector<string> result;
		unordered_map<string, int> hashtable;
		int count1 = list1.size();
		int count2 = list2.size();
		for (int i = 0; i < count1; i++) {
			hashtable[list1[i]] = i;
		}
		for (int i = 0; i < count2; i++) {
			int j = hashtable.count(list2[i]) > 0 ? hashtable[list2[i]] : -1;
			if (j != -1 && i + j <= max_int) {
				if (i + j < max_int) {
					result.clear();
					max_int = i + j;
				}
				result.push_back(list2[i]);
			}
		}
		return result;
	}
};
```

**Mark:** 92ms

# Additional
