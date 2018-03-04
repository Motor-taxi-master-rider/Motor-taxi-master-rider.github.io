---
layout: post
title: Python Coroutine Example -- Rock Paper Scissors
tags: Coroutine
category: Python
---


### Description
本代码来自Ian Ward的Jupyter Notebook -- “Iterables, Iterators, and Generators” 教程，实现了剪刀石头布的游戏。

### 预激协程
The flow is always the same when working with generators.
a generator object is created by the caller
the caller starts the generator
the generator passes data to the caller (or signals the end of the sequence)
the caller passes data to the generator
repeat from (3)

For generators that are driven by input to .send() no data is transferred in the first 3 steps above.

This is a decorator that arranges for .next() to be called once immediately after a generator is created. This will turn a generator function into a function that returns a generator immediately ready to receive data (step 4).

```python
def advance_generator_once(original_fn):
    "decorator to advance a generator once immediately after it is created"
    def actual_call(*args, **kwargs):
        gen = original_fn(*args, **kwargs)
        assert gen.next() is None
        return gen
    return actual_call
```

## 实例协程
As shown, one of the ways to pass a message to a generator is with .send(). This interface allows you to pass a single object to a generator. For this object we can pass tuples, dicts or anything else we choose.

You decide the protocol for your generator by documenting the types and values of objects you will send from caller to generator and yield from generator to caller.

Tuples are perfect for a generator that needs two objects each time, e.g. a player number and a key press.

This is a Rock-Paper-Scissors game where each player's play is passed in separately, and once both players have played the result of the game is yielded. Players can change their mind choose a different play if the other player hasn't chosen yet. Games will continue indefinitately.

This generator uses a common pattern of storing the result that will be yielded in a local variable so that there are fewer yield statements in the generator function. Having fewer yield statements makes it easier to understand where it is possible for execution to be paused within the generator function.

The outer while loop runs once for each full game. The inner while loop collects input from the users until the game result can be decided.

```python
@advance_generator_once
def rock_paper_scissors():
    """
    coroutine for playing rock-paper-scissors

    yields: 'invalid key': invalid input was sent
            ('win', player, choice0, choice1): when a player wins
            ('tie', None, choice0, choice1): when there is a tie
            None: when waiting for more input

    accepts to .send(): (player, key):
        player is 0 or 1, key is a character in 'rps'
    """
    valid = 'rps'
    wins = 'rs', 'sp', 'pr'
    result = None

    while True:
        chosen = [None, None]
        while None in chosen:
            player, play = yield result
            result = None
            if play in valid:
                chosen[player] = play
            else:
                result = 'invalid key'

        if chosen[0] + chosen[1] in wins:
            result = ('win', 0) + tuple(chosen)
        elif chosen[1] + chosen[0] in wins:
            result = ('win', 1) + tuple(chosen)
        else:
            result = ('tie', None) + tuple(chosen)
```

### Additional
参考文献:
1. [源教程](http://nbviewer.ipython.org/github/wardi/iterables-iterators-generators/blob/master/Iterables,%20Iterators,%20Generators.ipynb)
