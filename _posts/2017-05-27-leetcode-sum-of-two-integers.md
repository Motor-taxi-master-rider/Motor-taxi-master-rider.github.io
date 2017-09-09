---
layout: post
title: 总结：如何用位运算来简单高效地解决问题
tags:
- Bit_manipulation
- Translation
categories:
- Python
- C
description: Bit manipulation is the act of algorithmically manipulating bits or other pieces of data shorter than a word. Computer programming tasks that require bit manipulation include low-level device control, error detection and correction algorithms, data compression, encryption algorithms, and optimization.
---
# Question
Calculate the sum of two integers a and b, but you are **not allowed** to use the operator `+` and `-`.

**Example:**
Given a = 1 and b = 2, return 3.


[Source link](https://leetcode.com/problems/sum-of-two-integers/#/description)



# 简介
位运算是指用算法来操作比特或者其他小于一个字母的数据. 常见的需要利用位运算实现的编程任务有：底层设备控制、错误检测和矫正算法、数据压缩、加密算法及优化算法. 对于其他大部分任务而言， 现代编程语言通常允许程序员跟抽象化的位运算交互而非直接使用位运算. 位运算通常包含以下操作符: AND, OR, XOR, NOT和bit shifts.

在某些情况下，由于位操作是并行进行的， 因此通常能够去除或者减少对一个数据格式的循环遍历， 带来运算速度的成倍提升. 但与此同时， 位操作的代码也会更难编写和维护。




# 详细内容

## 基础

位操作的核心是位运算符 & (与), &#x7C;&nbsp;(或), ~ (非) and ^ (异或) 和 移位操作 a << b and a >> b.

>异或运算符没有对应的布尔运算符，在这里我们对它作一个简单的解释. 异或操作符接受两个输入，当且仅当有且只有一个输入为1的时候它才会返回1. 也就是当两个输入不同的时候返回1，相同的时候就会返回0. 异或操作符通常用^符号表示，缩写为XOR.

* Set 并集 `A | B`
* Set 交集 `A & B`
* Set 差集 `A & ~B`
* Set 非集 `ALL_BITS^ A or ~A`
* 将A的第bit位设为1 `A |= 1 << bit`
* 将A的第bit位设为0 `A &= ~(1 << bit)``
* 测试第bit位是否为0 `(A & 1 << bit) != 0`
* 取出最后1的值 `A&-A` or `A&~(A-1)` or `x^(x&(x-1))`
* 删除最后1的值 `A&(A-1)`
* 构建全为1的二进制数 `~0` (((unsigned)~0) >> 1 == 01111111111111111111111111111111)

**负数的运算是以补码形式进行的，如果运算结果首位为1，结果也需要求一次补码.**

## 实例

### 求所给数字二进制表示中的1的数量：

```c++
int count_one(int n) {
    while(n) {
        n = n&(n-1);
        count++;
    }
    return count;
}
```

### 是4的幂数嘛？ (事实上图检查方法、 迭代和递归可以做到一样的效果)

```c++
bool isPowerOfFour(int n) {
    return !(n&(n-1)) && (n&0x55555555);
    //只有一个1位(0x55555555 =1010101010101010101010101010101);
}
```

## `^` 的技巧

`^` 可以用来消除偶数个个一模一样的数字并且保留奇数的数字对, 或者保存不一样的对应位并且移除一样的对应位.

### 两数求和

使用 `^` 和 `&` 来进行两数求和

```c++
int getSum(int a, int b) {
    return b==0? a:getSum(a^b, (a&b)<<1);
		//注意终止条件，(0,1)对应位为1，(1,1)对应位进位;
}
```

### 丢失的数字

已知一个数组包含n个不同的数字： 0, 1, 2, ..., n, 找到那个不在数组中的数字。 例如, 所给数组 = [0, 1, 3] 则返回 2.

```c++
int missingNumber(vector<int>& nums) {
    int ret = 0;
    for(int i = 0; i < nums.size(); ++i) {
        ret ^= i;
        ret ^= nums[i];
    }
    return ret^=nums.size();
}
```

## `|` 的技巧

### 保存尽可能多的1位

找到小于或等于N的2的最大的幂数 (最大二进制数).

```c++
long largest_power(long N) {
    //将所有右侧的位 置为 1.
    N = N | (N>>1);
    N = N | (N>>2);
    N = N | (N>>4);
    N = N | (N>>8);
    N = N | (N>>16);
    return (N+1)>>1;
}
```

### 反转比特

反转一个所给的 32 bits unsigned integer.

```c++
uint32_t reverseBits(uint32_t n) {
    unsigned int mask = 1<<31, res = 0;
    for(int i = 0; i < 32; ++i) {
        if(n & 1) res |= mask;
        mask >>= 1;
        n >>= 1;
    }
    return res;
}
```

```c++
uint32_t reverseBits(uint32_t n) {
	uint32_t mask = 1, ret = 0;
	for(int i = 0; i < 32; ++i){
		ret <<= 1;
		if(mask & n) ret |= 1;
		mask <<= 1;
	}
	return ret;
}
```

## `&` 的技巧

`&`具有选择指定的位的功能。

### 反转整数中的位

```c++
x = ((x & 0xaaaaaaaa) >> 1) | ((x & 0x55555555) << 1);
x = ((x & 0xcccccccc) >> 2) | ((x & 0x33333333) << 2);
x = ((x & 0xf0f0f0f0) >> 4) | ((x & 0x0f0f0f0f) << 4);
x = ((x & 0xff00ff00) >> 8) | ((x & 0x00ff00ff) << 8);
x = ((x & 0xffff0000) >> 16) | ((x & 0x0000ffff) << 16);
```

### 位运算符 AND  数字范围

已知范围 [m, n] 其中 0 <= m <= n <= 2147483647, 返回对范围中的所有数据按位计算符AND计算的结果。 例如, 输入 [5, 7], 则返回 4.

```c++
int rangeBitwiseAnd(int m, int n) {
    int a = 0;
    while(m != n) {
        m >>= 1;
        n >>= 1;
        a++;
    }
    return m<<a;
}
```

### 1的数量


```c++
int hammingWeight(uint32_t n) {
    ulong mask = 1;
    int count = 0;
    for(int i = 0; i < 32; ++i){
       //31 will not do, delicate;
        if(mask & n) count++;
        mask <<= 1;
    }
    return count;
}
```

## 应用

### 重复DNA序列

所有DNA由一系列缩写为A、G、C、T的核苷酸组成, 例如: "ACGAATTCCG". 当研究DNA序列的时候，DNA中的重复序列是一个很重要的的部分. 编写一个函数来找到出现多于两次的十字符长度序列。
例如,
给出 s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",
返回: ["AAAAACCCCC", "CCCCCAAAAA"].


```c++
class Solution {
public:
	vector<string> findRepeatedDnaSequences(string s) {
		int sLen = s.length();
		vector<string> v;
		if (sLen < 11) return v;
		char keyMap[1 << 21]{ 0 };
		int hashKey = 0;
		for (int i = 0; i < 9; ++i) hashKey = (hashKey << 2) | (s[i] - 'A' + 1) % 5;
		for (int i = 9; i < sLen; ++i) {
			if (keyMap[hashKey = ((hashKey << 2) | (s[i] - 'A' + 1) % 5) & 0xfffff]++ == 1)
				v.push_back(s.substr(i - 9, 10));
		}
		return v;
	}
};
```

> 以上方法会在重复序列出现太多次时候失效。 为了避免这种情况的发生，我们可以使用 `unordered_map<int, int> keyMap` 来替代这里的 `char keyMap[1<<21]{0}`.

### 主元素

对于一个大小为n的数组，求其主元素. 主元素是在数组中出现次数大于 ⌊ n/2 ⌋ 次的元素. (比特计数是不是一个通常方法, 我们通常会应用排序和Moore Voting算法)


```c++
int majorityElement(vector<int>& nums) {
    int len = sizeof(int)*8, size = nums.size();*
    int count = 0, mask = 1, ret = 0;
    for(int i = 0; i < len; ++i) {
        count = 0;
        for(int j = 0; j < size; ++j)
            if(mask & nums[j]) count++;
        if(count > size/2) ret |= mask;
        mask <<= 1;
    }
    return ret;
}
```

### 单一数字 III

对于给予的一个整数数组, 除了一个元素以外的所有元素会出现三次，你的目标是找到那个单一的数字. (这种类型的问题同样也可以用比特计数简单地解决，但在这里我们将使用`digital logic design`来处理它)

```c++
//inspired by logical circuit design and boolean algebra;
//counter - unit of 3;
//current   incoming  next
//a b            c    a b
//0 0            0    0 0
//0 1            0    0 1
//1 0            0    1 0
//0 0            1    0 1
//0 1            1    1 0
//1 0            1    0 0
//a = a&~b&~c + ~a&b&c;
//b = ~a&b&~c + ~a&~b&c;
//return a|b since the single number can appear once or twice;
int singleNumber(vector<int>& nums) {
    int t = 0, a = 0, b = 0;
    for(int i = 0; i < nums.size(); ++i) {
        t = (a&~b&~nums[i]) | (~a&b&nums[i]);
        b = (~a&b&~nums[i]) | (~a&~b&nums[i]);
        a = t;
    }
    return a | b;
}
```


### 最大字母长度组合

对于给予的一组单词, 找到单词长度(word[i]) * length(word[j])之积的最大值， 要求两个单词不能有相同的字母. 你可以假定所有单词只包含小写字母. 如果没有符合条件的单词组存在则返回 0.

>示例 1:
给予 ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
返回 16
符合条件的两个单词可以是 "abcw", "xtfn".

>示例 2:
给予 ["a", "ab", "abc", "d", "cd", "bcd", "abcd"]
返回 4
符合条件的两个单词可以是 "ab", "cd".

>示例 3:
给予 ["a", "aa", "aaa", "aaaa"]
返回 0
没有符合条件的单词组.


显然我们将会频繁使用单词的长度以及比较两个单词是否拥有相同的字母:

* 使用一个整形数组去预存每个单词的长度将能够有效减少测量长度这一过程频度;
* 整形是一个四个字节三十二位存储单元, 而我们只有二十六个不同的字母, 所以我们就可以用每一位来表示单词是否包含某一字母.

```c++
int maxProduct(vector<string>& words) {
    vector<int> mask(words.size());
    vector<int> lens(words.size());
    for(int i = 0; i < words.size(); ++i) lens[i] = words[i].length();
    int result = 0;
    for (int i=0; i<words.size(); ++i) {
        for (char c : words[i])
            mask[i] |= 1 << (c - 'a');
        for (int j=0; j<i; ++j)
            if (!(mask[i] & mask[j]))
                result = max(result, lens[i]*lens[j]);
    }
    return result;
}
```

## 注意

* 左右位移太多的返回值是 undefined
* 对于负数的右移太多的返回值是 undefined
* right operand in shifting should be non-negative, otherwise the result is undefined
* `&` 和 `|` 运算符相对于比较运算符来说拥有更低的优先级

# 集合

所有的子集

在这种情况下位操作会体现出巨大的优势：当遍历一个N元素集合的所有子集是非常繁琐的时候，而一个N位比特值能够表示其所有子集。 如果A是B的子集，则表达A所需的数字小于直接表示B时候，位操作对于一些动态的编程方案是一个更好的选择。

如果你不介意以逆序遍历子集的话，你也可以在一个特定的子集里遍历到所有可能的子集星矢 (用比特模式表示). 使用的技巧和找到数字中的最低位的方法相似. 如果我们从一个子集中减去1, 则集合的最低的元素将会被清楚, 并且每个更低的元素将会被设置. 然而, 我们仅仅想要在父集合中设置这些更低的元素. 因此遍历的步骤只会是 i = (i - 1) & superset.

```c++
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> vv;
    int size = nums.size();
    if(size == 0) return vv;
    int num = 1 << size;
    vv.resize(num);
    for(int i = 0; i < num; ++i) {
        for(int j = 0; j < size; ++j)
            if((1<<j) & i) vv[i].push_back(nums[j]);   
    }
    return vv;
}
```

事实上还有另外两种方式： recursion 和 iteration 也能分别解决这个问题.

# Bitset类

Bitset储存位 (只有两种可能值的元素: 0 or 1, true or false, ...).
这个类有些类似布尔值数组，不过具有空间优化：通常每个元素只占一位 (在大部分系统中比最小的元素种类：char小八倍).

```c++
// bitset::count
#include <iostream>       // std::cout
#include <string>         // std::string
#include <bitset>         // std::bitset

int main () {
  std::bitset<8> foo (std::string("10110011"));
  std::cout << foo << " has ";
  std::cout << foo.count() << " ones and ";
  std::cout << (foo.size()-foo.count()) << " zeros.\n";
  return 0;
}
```
