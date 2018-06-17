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

`_get_permutations_draw`生成器使用了`itertools.permutations`方法生成了所给单词组的所有长度的排列。这里`ab`和`ba`要被作为两个单词存在，所以需要使用排列。我在生成器里就早早使用了`set`方法去重，之后在`get_possible_dict_words`方法里又将组成的字符串再次去重，实际上是没有必要的。可以只保留后面一个去重步骤来提高整体函数的运行效率。

在`get_possible_dict_words`中，我运用了python集合的交集操作来取得所有在字典里的有效词组组合。最终返回所要求的单词集合。

那些最高分的单词中都是一些冷门词汇，所以总的来说，这还是个比较有趣的游戏。


### Hangman
这里还有另一个有意思的[Hangman](https://zh.wikipedia.org/wiki/%E7%8C%9C%E5%96%AE%E8%A9%9E%E9%81%8A%E6%88%B2)小游戏。

Hangman是一系列猜词游戏的简称。在我们的Hangman中，我们需要猜的是电源的英文名称。每次失败将都会在Hangman添加一笔，最终形成一副完整的Hangman图，游戏失败。

```code
________      
|      |      
|      0      
|     /|\     
|     / \     
|"""
```

该游戏的源码可在此[获得](https://github.com/Motor-taxi-master-rider/challenges/blob/master/10/hangman.py)。

首先我们先处理一下要猜的单词：

```python
def _construct_word(self, word: str) -> defaultdict:
    character_dict = defaultdict(set)
    for index, character in enumerate(word):
        if character.strip() and character in ASCII:
            character_dict[character].add(index)
    return character_dict
```

在此我们将所有的有效字母及其序号保存在字典中，如`tootsie`中的`o`则被保存为`o: (1, 2)`。此外，将谜面作为一个列表储存，还未揭晓的数字用`PlACEHOLDER`替代，则猜到`o`后的谜面为`['_', 'o', 'o', '_', '_', '_', '_']`。这样在之后玩家猜到字典中的字母时我们: 1.将该字母从字典里弹出；2.将谜面列表中所有该字母储存的序号的元素替换为该字母。当字典里没有元素时候，用户便猜出了相关单词。

另外需要考虑的是用户猜测失败的例子，有两种情况会导致一次猜测的失败。一是用户所猜字母不在我们所给的谜底之中，这时我们输出一张Hangman的图片，如果用户的错误次数过多将导致游戏的失败。二是用户猜了一个之前猜过的字母，我们这时仁慈的弹出提示并给予用户一次额外的猜测机会。这部分实现的代码如下:

```python
@types.coroutine
def _hangman_popper(self):
    """print a hangman graph if guess is not right"""
    guessed_character = set()
    graphics = hang_graphics()
    graph = next(graphics)

    while True:
        guess = yield False
        if guess not in guessed_character:
            guessed_character.add(guess)
            if guess in self._word:
                print(f'{colored(len(self._word[guess]),"green")} of {colored(guess,"green")} in the word.')
                for index in self._word.pop(guess):
                    self._guess[index] = guess
                if not self._word:
                    yield True
            else:
                print(f'{colored(guess,"green")} is not in the word!\n'
                      f'{graph}\n')
                try:
                    graph = next(graphics)
                except StopIteration:
                    raise NoChance
        else:
            print(f'You have guessed {colored(guess,"green")} before, please choose another character.\n')
```

输出越来越完整的Hangman图片是以生成器的方式实现的，这启发了我以协程的方式实现游戏与用户的交互过程。协程有三种输出，分别是猜测失败时的`yield False`，完成谜底时的`yield True`和机会用完时的`raise NoChane`。一个还需要注意的地方是，我们需要在Hangman类的构造函数中预激该生成器。

这也是一个相当长知识的游戏，不仅如此，用协程实现的过程也是相当有趣的，是一种不一样的编程体验。

### Additional
