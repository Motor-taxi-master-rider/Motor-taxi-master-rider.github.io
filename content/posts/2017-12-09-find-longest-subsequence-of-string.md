---
layout: post
title: Find longest word in dictionary that is a subsequence of a given string
tags: Algorithm
category: Python
---


### Description
Given a string `S` and a set of words `D`, find the longest word in `D` that is a subsequence of `S`.

Word `W` is a subsequence of `S` if some number of characters, possibly zero, can be deleted from `S` to form `W`, without reordering the remaining characters.

Note: `D` can appear in any format (list, hash table, prefix tree, etc.

For example, given the input of `S = "abppplee"` and `D = {"able", "ale", "apple", "bale", "kangaroo"}` the correct output would be `"apple"`.

* The words "able" and "ale" are both subsequences of S, but they are shorter than "apple".
* The word "bale" is not a subsequence of S because even though S has all the right letters, they are not in the right order.
* The word "kangaroo" is the longest word in D, but it isn't a subsequence of S.


### Solution
## Check each dictionary word using a greedy algorithm
一个比较容易想到的方法就是将字典中的单词与`S`逐个比较，这样最差时间复杂度为O(N*W*M)。`W`位字典中的单词数量，`M`为单词的平均长度。虽然可以将字典中的单词按长度降序排列来减少一般状态下的运行时间，但不会减少最差时间复杂度。将`L`设为字典中所有单词字母长度之和，时间复杂度也可以表示为O(N*L)。

代码如下：

```python
s = 'abppplee'
d = ['able', 'ale', 'apple', 'bale', 'kangaroo']


def compare(s, w):
    i = 0
    for character in w:
        while i < len(s):
            if character == s[i]:
                i += 1
                break
            i += 1
        else:
            break
    else:
        return True
    return False


def solution(s, d):
    for w in sorted(d, key=len, reverse=True):
        if compare(s, w):
            return w


print(solution(s, d))
```

## Improving the greedy approach
我们也可以对`S`做一些预处理操作，记录其中字母的出现：

```
S = "abppplee"

a -> [0]
b -> [1]
p -> [2, 3, 4]
l -> [5]
e -> [6, 7]
```

这一操作的的时间复杂度为O(n)。在我们查找时，对于一个字典中的单词`w`，首先判断它的字母`X`是否在上述数据结构中，之后再去二分查找到数据结构中的满足：最小的index大于`X`的`Y`字母，其中`Y`为`X`的下一个字母。这样处理的时间复杂度为O(N + L * logN)。

Google提供的代码如下：

```python
import collections
import sys
def find_longest_word_in_string(letters, words):
    letter_positions = collections.defaultdict(list)
    # For each letter in 'letters', collect all the indices at which it appears.
    # O(#letters) space and speed.
    for index, letter in enumerate(letters):
        letter_positions[letter].append(index)
    # For words, in descending order by length...
    # Bails out early on first matched word, and within word on
    # impossible letter/position combinations, but worst case is
    # O(#words # avg-len) * O(#letters / 26) time; constant space.
    # With some work, could be O(#W * avg-len) * log2(#letters/26)
    # But since binary search has more overhead
    # than simple iteration, log2(#letters) is about as
    # expensive as simple iterations as long as
    # the length of the arrays for each letter is
    # “small”.  If letters are randomly present in the
    # search string, the log2 is about equal in speed to simple traversal
    # up to lengths of a few hundred characters.              
    for word in sorted(words, key=lambda w: len(w), reverse=True):
        pos = 0
        for letter in word:
            if letter not in letter_positions:
                break
        # Find any remaining valid positions in search string where this
        # letter appears.  It would be better to do this with binary search,
        # but this is very Python-ic.
        possible_positions = [p for p in letter_positions[letter] if p >= pos]
        if not possible_positions:
            break
        pos = possible_positions[0] + 1
        else:
            # We didn't break out of the loop, so all letters have valid positions  
            return word
if __name__ == '__main__':
    print subdict(sys.argv[1], sys.argv[2:])
```

## An optimal O(N + L) approach for any alphabet
首先是一个基于上述算法的，适用于`S`的长度不长的情况的优化方案。我们将`p -> [2, 3, 4]`拓展成`p -> [2, 2, 3, 4, -1, -1, -1, -1]`，其中列表的每个元素对应`S`中该位置后出现该列表key的字母的序号（包括该位置的序号）。如果不存在就以`-1`表示。这样我们就不用二分法来查找列表，但随之带来的问题是：算法的实际复杂度变为O(N*A + L)，`A`为`S`的字母集合的长度，并且消耗O（NA）的空间。因此当`S`过长时并非一个很好的优化。

除此之外，我们还可以通过同时遍历所有`D`中的单词来压榨我们的时间复杂度。字典中的每个单词放入(w,i)元组。其中w为单词本身，i记录了序号为i的字母已经达成匹配。这样我们就可以形成类似这样的数据结构：

```
D = {"able", "ale", "apple", "bale", "kangaroo"}

a -> [("able", 0), ("ale", 0), ("apple", 0)]
b -> [("bale", 0)]
k -> [("kangaroo", 0)]
```

我们遍历`S`中的每个元素时，将所有该字母key对应列表里的元组`t`的i增加1，将这些元素移到`t.w[t.i]`对应的键下。当某个`t`的i等于w的长度时它就是一个符合条件的单词，将它移至一个结果列表。最终我们找出这个列表中的最长单词。这么做的时间复杂度为O(W + N + W' * logW')，其中`W'`为结果集中的单词数量，最差等于`W`，使得其复杂度非常接近理论最优的O(N + L)。代码如下：

```python
s = 'abppplee'
d = ['able', 'ale', 'apple', 'bale', 'kangaroo']

from collections import defaultdict

Alphabets = defaultdict(list)
for word in d:
    Alphabets[word[0]].append([word, 0])


def solution(s, d):
    result = ''
    for character in s:
        alphabet_list = Alphabets[character]
        for i in reversed(range(len(alphabet_list))):
            temp = alphabet_list.pop(i)
            temp[1] += 1
            if len(temp[0]) == temp[1]:
                if temp[1] >= len(result):
                    result = temp[0]
            else:
                Alphabets[temp[0][temp[1]]].append(temp)
    return result


print(solution(s, d))
```

### Additional
