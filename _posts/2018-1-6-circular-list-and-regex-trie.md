---
layout: post
title: Build a circular list and regex trie
tags:
- Algorithm
categories:
- Python
description: two interesting algorithm question.
---


# Dacing programs
这个问题来自`Advent of code`的[第十六日](http://adventofcode.com/2017/day/16)。

解决代码如下:

```python
def solution(lst, order):
    # 循环数组，start为头指针
    result_list = list(order)
    # 减少Partner时间复杂度的字典
    result_dict = {s: i for i, s in enumerate(result_list)}
    length = len(result_list)
    start = 0

    for action in lst:
        if action.startswith('s'):
            start = (start + length) % length - int(action[1:])
            continue

        if action.startswith('x'):
            x, y = action[1:].split('/')
            x_real = (start + int(x)) % length
            y_real = (start + int(y)) % length
        elif action.startswith('p'):
            x, y = action[1:].split('/')
            x_real = result_dict[x]
            y_real = result_dict[y]
        result_list[x_real], result_list[y_real] = result_list[y_real], result_list[x_real]
        result_dict[result_list[x_real]], result_dict[result_list[y_real]] = result_dict[result_list[y_real]], \
                                                                             result_dict[result_list[x_real]]
    return "".join(result_list[i % length] for i in range(start, start + length))


def solution2(lst，order):
    orders = []
    while order not in orders:
        orders.append(order)
        order = solution(lst, order)

    return orders[1000000000 % len(orders)]
```

对于第一部分涉及到的三个操作。第一个操作Spin *sX* ，只需将头指针后移X位。对于第二个操作Exchange和第三个操作Partner，由于涉及到index和值的比较，因此我们通过建立{值：index}字典的形式来减少Partner操作的时间复杂度。

第二部分问题由于要循环一亿次，全部遍历时间复杂度过高。测试发现当输入相同的操作序列时，多次遍历后会出现循环的情况，因此有解法二。


# Regex replacement
来源于Stack Overflow的一个问题: [Speed up millions of regex replacements in Python 3](https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3)。

赞同最多的`"\b(word1|word2|word3)\b"`方法其实不是最好的算法，正则并集会带来O(1)的最好时间复杂度，O(n)的平均及最差时间复杂度。验证代码如下：

```python
import re
import timeit
import random

with open('/usr/share/dict/american-english') as wordbook:
    english_words = [word.strip().lower() for word in wordbook]
    random.shuffle(english_words)

print("First 10 words :")
print(english_words[:10])

test_words = [
    ("Surely not a word", "#surely_NöTäWORD_so_regex_engine_can_return_fast"),
    ("First word", english_words[0]),
    ("Last word", english_words[-1]),
    ("Almost a word", "couldbeaword")
]


def find(word):
    def fun():
        return union.match(word)
    return fun

for exp in range(1, 6):
    print("\nUnion of %d words" % 10**exp)
    union = re.compile(r"\b(%s)\b" % '|'.join(english_words[:10**exp]))
    for description, test_word in test_words:
        time = timeit.timeit(find(test_word), number=1000) * 1000
        print("  %-17s : %.1fms" % (description, time))
```

Output:

```python
First 10 words :
["geritol's", "sunstroke's", 'fib', 'fergus', 'charms', 'canning', 'supervisor', 'fallaciously', "heritage's", 'pastime']

Union of 10 words
  Surely not a word : 0.7ms
  First word        : 0.8ms
  Last word         : 0.7ms
  Almost a word     : 0.7ms

Union of 100 words
  Surely not a word : 0.7ms
  First word        : 1.1ms
  Last word         : 1.2ms
  Almost a word     : 1.2ms

Union of 1000 words
  Surely not a word : 0.7ms
  First word        : 0.8ms
  Last word         : 9.6ms
  Almost a word     : 10.1ms

Union of 10000 words
  Surely not a word : 1.4ms
  First word        : 1.8ms
  Last word         : 96.3ms
  Almost a word     : 116.6ms

Union of 100000 words
  Surely not a word : 0.7ms
  First word        : 0.8ms
  Last word         : 1227.1ms
  Almost a word     : 1404.1ms
```

这会导致整体算法的时间复杂度变为O(n^2),因此有如下两个解法：

```python
import re
with open('/usr/share/dict/american-english') as wordbook:
    banned_words = set(word.strip().lower() for word in wordbook)


def delete_banned_words(matchobj):
    word = matchobj.group(0)
    if word.lower() in banned_words:
        return ""
    else:
        return word

sentences = ["I'm eric. Welcome here!", "Another boring sentence.",
             "GiraffeElephantBoat", "sfgsdg sdwerha aswertwe"] * 250000

for sentence in sentences:
    sentence = re.sub('\w+', delete_banned_words, sentence)
```

这个解法时间发复杂度为O(n)，但是会在去掉单词时留下空格。因为它是扫描`\w+`的，因此无法避免这个问题。

一个对之前正则并集的改进是通过字典树的方式创建正则并集，该算法的时间复杂度也为O(n)。

```python
class Trie():
    """Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                recurse = self._pattern(data[char])
                if recurse:
                    alt.append(self.quote(char) + recurse)
                else:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())
```

这段代码首先会生成所有被ban单词的字典树，然后parse该树生成像如下这样的正则表达式：

```
(?:a(?:(?:\'s|a(?:\'s|chen|liyah(?:\'s)?|r(?:dvark(?:(?:\'s|s))?|on))|b(?:\'s|a(?:c(?:us(?:(?:\'s|es))?|[ik])|ft|lone(?:(?:\'s|s))?|ndon(?:(?:ed|ing|ment(?:\'s)?|s))?|s(?:e(?:(?:ment(?:\'s)?|[ds]))?|h(?:(?:e[ds]|ing))?|ing)|t(?:e(?:(?:ment(?:\'s)?|[ds]))?|ing|toir(?:(?:\'s|s))?))|b(?:as(?:id)?|e(?:ss(?:(?:\'s|es))?|y(?:(?:\'s|s))?)|ot(?:(?:\'s|t(?:\'s)?|s))?|reviat(?:e[ds]?|i(?:ng|on(?:(?:\'s|s))?))|y(?:\'s)?|\é(?:(?:\'s|s))?)|d(?:icat(?:e[ds]?|i(?:ng|on(?:(?:\'s|s))?))|om(?:en(?:(?:\'s|s))?|inal)|u(?:ct(?:(?:ed|i(?:ng|on(?:(?:\'s|s))?)|or(?:(?:\'s|s))?|s))?|l(?:\'s)?))|e(?:(?:\'s|am|l(?:(?:\'s|ard|son(?:\'s)?))?|r(?:deen(?:\'s)?|nathy(?:\'s)?|ra(?:nt|tion(?:(?:\'s|s))?))|t(?:(?:t(?:e(?:r(?:(?:\'s|s))?|d)|ing|or(?:(?:\'s|s))?)|s))?|yance(?:\'s)?|d))?|hor(?:(?:r(?:e(?:n(?:ce(?:\'s)?|t)|d)|ing)|s))?|i(?:d(?:e[ds]?|ing|jan(?:\'s)?)|gail|l(?:ene|it(?:ies|y(?:\'s)?)))|j(?:ect(?:ly)?|ur(?:ation(?:(?:\'s|s))?|e[ds]?|ing))|l(?:a(?:tive(?:(?:\'s|s))?|ze)|e(?:(?:st|r))?|oom|ution(?:(?:\'s|s))?|y)|m\'s|n(?:e(?:gat(?:e[ds]?|i(?:ng|on(?:\'s)?))|r(?:\'s)?)|ormal(?:(?:it(?:ies|y(?:\'s)?)|ly))?)|o(?:ard|de(?:(?:\'s|s))?|li(?:sh(?:(?:e[ds]|ing))?|tion(?:(?:\'s|ist(?:(?:\'s|s))?))?)|mina(?:bl[ey]|t(?:e[ds]?|i(?:ng|on(?:(?:\'s|s))?)))|r(?:igin(?:al(?:(?:\'s|s))?|e(?:(?:\'s|s))?)|t(?:(?:ed|i(?:ng|on(?:(?:\'s|ist(?:(?:\'s|s))?|s))?|ve)|s))?)|u(?:nd(?:(?:ed|ing|s))?|t)|ve(?:(?:\'s|board))?)|r(?:a(?:cadabra(?:\'s)?|d(?:e[ds]?|ing)|ham(?:\'s)?|m(?:(?:\'s|s))?|si(?:on(?:(?:\'s|s))?|ve(?:(?:\'s|ly|ness(?:\'s)?|s))?))|east|idg(?:e(?:(?:ment(?:(?:\'s|s))?|[ds]))?|ing|ment(?:(?:\'s|s))?)|o(?:ad|gat(?:e[ds]?|i(?:ng|on(?:(?:\'s|s))?)))|upt(?:(?:e(?:st|r)|ly|ness(?:\'s)?))?)|s(?:alom|c(?:ess(?:(?:\'s|e[ds]|ing))?|issa(?:(?:\'s|[es]))?|ond(?:(?:ed|ing|s))?)|en(?:ce(?:(?:\'s|s))?|t(?:(?:e(?:e(?:(?:\'s|ism(?:\'s)?|s))?|d)|ing|ly|s))?)|inth(?:(?:\'s|e(?:\'s)?))?|o(?:l(?:ut(?:e(?:(?:\'s|ly|st?))?|i(?:on(?:\'s)?|sm(?:\'s)?))|v(?:e[ds]?|ing))|r(?:b(?:(?:e(?:n(?:cy(?:\'s)?|t(?:(?:\'s|s))?)|d)|ing|s))?|pti...
```

# Additional
