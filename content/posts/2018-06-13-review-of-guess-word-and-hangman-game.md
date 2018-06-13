---
layout: post
title: [Review] Guess word and hangman game
tags: Game,Coroutine
---


### Guess max score word
这个游戏来自[Pybites](http://pybit.es/codechallenge02.html)。

整个游戏的流程是这样的：

首先随机的给出十个英文字母，如`O, S, J, I, O, O, R, H, X, D`, 之后玩家以这些字母拼出合理的英文单词。以给出字母为例，可以组成`DOOR`，但无法使用超过给出字母数量的单词来组词。之后会根据字母的稀有度给玩家所组单词来打分，如`E`、`A`等字母为一分，而`Y`,`Z`等字母则算作八九分。系统同时计算出这些字母实际能组成的最高分的单词，并计算玩家的打分比例。如果我们猜测的值为`DOOR`，则我们获得的字母分为五分，而给出的字母能组成的最高分单词为`SHOJI`(商会)分值为十五分，我们的得分比例则为33%。

该游戏的源码可在此[获得](https://github.com/Motor-taxi-master-rider/challenges/blob/master/02/game.py)。

在寻找给出字母能组成的最高分单词时，我们使用了以下代码:

```python
def get_possible_dict_words(draw):
    """Get all possible words from draw which are valid dictionary words.
    Use the _get_permutations_draw helper and DICTIONARY constant"""
    return set(DICTIONARY) & set(map("".join, _get_permutations_draw(draw)))


def _get_permutations_draw(draw):
    """Helper for get_possible_dict_words to get all permutations of draw letters.
    Hint: use itertools.permutations"""
    for length in range(1, len(draw) + 1):
        yield from set(itertools.permutations(draw, length))
```

`_get_permutations_draw`生成器使用了`itertools.permutations`方法生成了所给单词组的所有长度的组合。这里`ab`和`ba`要被作为两个单词存在，所以需要使用组合。我在生成器里就早早使用了`set`方法去重，之后在`get_possible_dict_words`方法里又将组成的字符串再次去重，实际上是没有必要的。可以只保留后面一个去重步骤来提高整体函数的运行效率。

在`get_possible_dict_words`中，我运用了python集合的交集操作来取得所有在字典里的有效词组组合。最终返回所要求的单词集合。

### Additional
