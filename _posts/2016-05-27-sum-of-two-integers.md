---
layout: post
title: 总结：如何用位运算来简单高效地解决问题
tags:
- Python
- C++
- Bit_Manipulation
- Translation
categories:
- Python
- C++
description: Bit manipulation is the act of algorithmically manipulating bits or other pieces of data shorter than a word. Computer programming tasks that require bit manipulation include low-level device control, error detection and correction algorithms, data compression, encryption algorithms, and optimization. For most other tasks, modern programming languages allow the programmer to work directly with abstractions instead of bits that represent those abstractions. Source code that does bit manipulation makes use of the bitwise operations: AND, OR, XOR, NOT, and bit shifts.
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

位操作的核心是位运算符 & (与), | (或), ~ (非) and ^ (异或) 和 移位操作 a << b and a >> b.

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

求所给数字二进制表示中的1的数量：

```c++
int count_one(int n) {
    while(n) {
        n = n&(n-1);
        count++;
    }
    return count;
}
```

是4的幂数嘛？ (事实上图检查方法、 迭代和递归可以做到一样的效果)

```c++
bool isPowerOfFour(int n) {
    return !(n&(n-1)) && (n&0x55555555);
    //只有一个1位(0x55555555 =1010101010101010101010101010101);
}
```

## `^` 的技巧

`^` 可以用来消除偶数个个一模一样的数字并且保留奇数的数字对, 或者保存不一样的对应位并且移除一样的对应位.

两数求和

使用 `^` 和 `&` 来进行两数求和

```c++
int getSum(int a, int b) {
    return b==0? a:getSum(a^b, (a&b)<<1);
		//注意终止条件，(0,1)对应位为1，(1,1)对应位进位;
}
```

丢失的数字

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

保存尽可能多的1位

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

反转比特

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

选择指定的位

反转整数中的位

```c++
x = ((x & 0xaaaaaaaa) >> 1) | ((x & 0x55555555) << 1);
x = ((x & 0xcccccccc) >> 2) | ((x & 0x33333333) << 2);
x = ((x & 0xf0f0f0f0) >> 4) | ((x & 0x0f0f0f0f) << 4);
x = ((x & 0xff00ff00) >> 8) | ((x & 0x00ff00ff) << 8);
x = ((x & 0xffff0000) >> 16) | ((x & 0x0000ffff) << 16);
```

位运算符 AND  数字范围

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

1的数量


```c++
int hammingWeight(uint32_t n) {
    ulong mask = 1;
    int count = 0;
    for(int i = 0; i < 32; ++i){ //31 will not do, delicate;
        if(mask & n) count++;
        mask <<= 1;
    }
    return count;
}
```　

##　应用

重复DNA序列

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

主要的元素

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times. (bit-counting as a usual way, but here we actually also can adopt sorting and Moore Voting Algorithm)


```c++
int majorityElement(vector<int>& nums) {
    int len = sizeof(int)*8, size = nums.size();
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

Single Number III

Given an array of integers, every element appears three times except for one. Find that single one. (Still this type can be solved by bit-counting easily.) But we are going to solve it by digital logic design

Solution

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
;
Maximum Product of Word Lengths

Given a string array words, find the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. You may assume that each word will contain only lower case letters. If no such two words exist, return 0.

Example 1:
Given ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
Return 16
The two words can be "abcw", "xtfn".
Example 2:
Given ["a", "ab", "abc", "d", "cd", "bcd", "abcd"]
Return 4
The two words can be "ab", "cd".
Example 3:
Given ["a", "aa", "aaa", "aaaa"]
Return 0
No such pair of words.
Solution

Since we are going to use the length of the word very frequently and we are to compare the letters of two words checking whether they have some letters in common:

using an array of int to pre-store the length of each word reducing the frequently measuring process;
since int has 4 bytes, a 32-bit type, and there are only 26 different letters, so we can just use one bit to indicate the existence of the letter in a word.
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
Attention

result after shifting left(or right) too much is undefined
right shifting operations on negative values are undefined
right operand in shifting should be non-negative, otherwise the result is undefined
The & and | operators have lower precedence than comparison operators
Sets
All the subsets
A big advantage of bit manipulation is that it is trivial to iterate over all the subsets of an N-element set: every N-bit value represents some subset. Even better, if A is a subset of B then the number representing A is less than that representing B, which is convenient for some dynamic programming solutions.

It is also possible to iterate over all the subsets of a particular subset (represented by a bit pattern), provided that you don’t mind visiting them in reverse order (if this is problematic, put them in a list as they’re generated, then walk the list backwards). The trick is similar to that for finding the lowest bit in a number. If we subtract 1 from a subset, then the lowest set element is cleared, and every lower element is set. However, we only want to set those lower elements that are in the superset. So the iteration step is just i = (i - 1) & superset.

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
Actually there are two more methods to handle this using recursion and iteration respectively.

Bitset
A bitset stores bits (elements with only two possible values: 0 or 1, true or false, ...).
The class emulates an array of bool elements, but optimized for space allocation: generally, each element occupies only one bit (which, on most systems, is eight times less than the smallest elemental type: char).

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
Always welcom new ideas and practical tricks, just leave them in the comments!
