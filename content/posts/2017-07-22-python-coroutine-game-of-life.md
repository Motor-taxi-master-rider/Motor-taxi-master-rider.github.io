---
layout: post
title: Python Coroutine Example -- Game of life
tags: Coroutine
category: Python
---


### Description
本文所列代码实现了 John Conway 发明的“生命游戏”（https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life），使用协程管理游戏运行过程中各个细胞的状态。
源自Brett Slatkin 写的《Effective Python：编写高质量 Python 代码的 59 个有效方法》一书。


### 代码及注释

```python
from collections import namedtuple

ALIVE = '*'
EMPTY = '-'
TICK = object()

Query = namedtuple('Query', 'y x')

Transition = namedtuple('Transition', 'y x state')


def count_neighbors(y, x):
  """
  获取邻居状态的子协程。
  返回存活邻居的数量给step_cell的neighbor变量。
  """
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
  """
  细胞转换的条件。
  """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state


def step_cell(y, x):
  """
  先抛出目标细胞自身，再逐个抛出邻居。
  获得以上所有细胞的状态之后再根据细胞转换条件抛出目标细胞
  在下一世代的状态。
  """
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate(height, width):
  """
  为gird的每个元素抛出其自身及其邻居给客户程序。
  TICK为终止条件。
  """
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


class Grid(object):
  """
  细胞生活的地方。实现了getitem和setitem方法方便live_a_generation方法操作。
  """
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

    def __getitem__(self, position):
        y, x = position
        return self.rows[y % self.height][x % self.width]

    def __setitem__(self, position, state):
        y, x = position
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
  """
  一世代的生命模拟。
  """
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    #TICK为一世代的模拟的结束信号。
    while item is not TICK:
        #如果协程抛出的是query，则传入这一世代该query对应细胞的存活情况
        #如果是transition则表示对某一细胞的转换状态判断已完成，改变其存活情况
        if isinstance(item, Query):
            state = grid[item.y, item.x]
            item = sim.send(state)
        else:  # Must be a Transition
            progeny[item.y, item.x] = item.state
            item = next(sim)
    return progeny


class ColumnPrinter(object):
  """
  将测试结果打印出来。
  columns的每个元素是每次模拟后的结果grid。
  """
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)
        rows = [''] * row_count
        print(rows)
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    rows[j] += str(i).center(len(line))
                else:
                    rows[j] += line
                if (i + 1) < len(self.columns):
                    rows[j] += ' | '
        return '\n'.join(rows)


def main():
  """
  测试代码。
  初始生成的grid为：
    ---*-----
    ----*----
    --***----
    ---------
    ---------
  """
    grid = Grid(5, 9)
    grid[0, 3] = ALIVE
    grid[1, 4] = ALIVE
    grid[2, 2] = ALIVE
    grid[2, 3] = ALIVE
    grid[2, 4] = ALIVE

    columns = ColumnPrinter()
    sim = simulate(grid.height, grid.width)
    for i in range(10):
         columns.append(str(grid))
         grid = live_a_generation(grid, sim)
    print(columns)


if __name__ == "__main__":
    main()
```



### Additional
参考文献:
1. [原书示例](http://www.effectivepython.com/2015/03/10/consider-coroutines-to-run-many-functions-concurrently/)
2. [原书代码](https://github.com/bslatkin/effectivepython/blob/master/example_code/item_40.py)
