---
layout: post
title: Python yield tutorial markdown
tags:
- Coroutine
categories:
- Python
description: A markdown version of the yield jupyter notebook.
---

# Description
本文是我的[jupyter notebook](https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/coroutine.ipynb)的markdown版本。

# An introduction to Python yield

## WHAT

### A function and a generater


```python
def fun():
    return 'fun'

def gen():
    yield 'gen'
```


```python
fun()
```




    'fun'




```python
gen()
```




    <generator object gen at 0x0000000007503780>



### A range() like example


**for** ... **in range()** loop is used quite often when iterating objects in `python`.

In below example, we made a generator to mock **range()** function.


```python
def counter(top):
    n = 0
    while n < top:
        yield n
        n += 1
```


```python
for i in counter(10):
    print(i)
```

    0
    1
    2
    3
    4
    5
    6
    7
    8
    9


### Under the covers

Generator object runs in response to **next()** or **send()**


```python
def counter_sample(top):
    n = 0
    while n < top:
        print('-> before yield')
        yield n
        print('-> after yield')
        n += 1

c = counter_sample(5)
```


```python
print(next(c))
```

    -> before yield
    0


**StopIteration** raised when function returns


```python
print(c.send(None))
```

    -> after yield
    -> before yield
    1


### Create coroutine with yield

You can **send** data to a coroutine.


```python
def generator():
    item = yield
    print('item = {}'.format(item))
    yield 10
```

**Prime** the coroutine


```python
g = generator()
g.send(None)
```

<img src="https://github.com/Motor-taxi-master-rider/Python/tree/master/Script/generator_send_data.PNG">

Send data


```python
value = g.send(20)
```

    item = 20



```python
print('value = {}'.format(value))
```

    value = 10




A coroutine which **receives** data as well as **produces** data


```python
def averager():
    total, count, average = 0.0, 0, None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
```


```python
avg = averager()
avg.send(None)
```


```python
avg.send(10)
```




    10.0




```python
avg.send(20)
```




    15.0




```python
avg.send(30)
```




    20.0



**Three features of coroutines:**
- When a coroutine run into **yield**, it will suspend
- A **caller** should **schedule** the coroutine when it suspended
- When a coroutine suspended, it will **return control** to the **caller**

## WHY

### A tornado example


```python
import time
import tornado.ioloop
import tornado.web
import tornado.gen


class BadStupidHandler(tornado.web.RequestHandler):
    def get(self):
        for i in range(20):
            self.write('{}<br>'.format(i))
            self.flush()
            time.sleep(0.5)


class GoodStupidHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        for i in range(20):
            self.write('{}<br>'.format(i))
            self.flush()
            yield tornado.gen.sleep(0.5)

app = tornado.web.Application([
     (r'/bad', BadStupidHandler),
     (r'/good', GoodStupidHandler)
])

```

Refer to documentation [Frequently Asked Questions](http://www.tornadoweb.org/en/stable/faq.html).

## HOW

### Use coroutine to simplfy your context manager

A context manager is to change:


```python
try:
    f = open('some.txt')
    print(f.readline()) # do something with f
finally:
    f.close()
```

    coroutine



To:


```python
with open('some.txt') as f:
    print(f.readline()) # do something with f
```

    coroutine



You can define your own context manager with a **class** implements `__enter__` and `__exit__` method


```python
class Mirror:
    def __init__(self, num):
        self.num = num

    def __enter__(self):
        import sys


        def reverse_write(text):
            self.original_write(text[::-1])

        self.original_write = sys.stdout.write
        sys.stdout.write = reverse_write
        return 'This is mirror {}'.format(self.num)

    def __exit__(self,exc_type, exc_value, traceback):
        import sys

        sys.stdout.write = self.original_write
```


```python
with Mirror(1000) as first_string:
    print(first_string)
    print(123456789)
print('Out there')
```

    0001 rorrim si sihT
    987654321
    Out there


Use decorator `contextlib.contextmanager` and `generator` to simplfy your own context manager


```python
import contextlib

@contextlib.contextmanager
def Mirror_new(num):
    import sys


    def reverse_write(text):
        original_write(text[::-1])

    original_write = sys.stdout.write
    sys.stdout.write = reverse_write
    yield 'This is mirror {}'.format(num)
    sys.stdout.write = original_write
```


```python
with Mirror_new(1000) as first_string:
    print(first_string)
    print(123456789)
print('Out there')
```

    0001 rorrim si sihT
    987654321
    Out there


How does it work?

We define a warpper class to proxy our generator:


```python
class  GeneratorCM:        
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        self._gen = self._func(*args, **kwargs)
        return self

    def __enter__(self):
        return self._gen.send(None)

    def __exit__(self,exc_type, exc_value, traceback):
        try:
            self._gen.send(None)
        except StopIteration:
            return True
```


```python
@GeneratorCM
def Mirror_custom(num):
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'This is mirror {}'.format(num)
    sys.stdout.write = original_write
```


```python
with Mirror_custom(1000) as first_string:
    print(first_string)
    print(123456789)
print('Out there')
```

    0001 rorrim si sihT
    987654321
    Out there


GeneratorCM with full try catch is listed below:


```python
class  GeneratorCM:        
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        self._gen = self._func(*args, **kwargs)
        return self

    def __enter__(self):
        return self._gen.send(None)

    def __exit__(self,exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                next(self._gen)
            else:
                self._gen.throw(exc_type, exc_value, traceback)
                raise RuntimeError("Generator didn't stop")
        except StopIteration:
                return True
        except:
                if sys.exc_info()[1] is not exc_value: raise
```

### Inlined yield

Following statement is very common in tornado framwork


```python
from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
```

How does it work?

First,define a slow function to mock `http.fetch` :


```python
import time
import random

def func(x, y):    
    sleep_time = random.random() * 3
    time.sleep(sleep_time)
    print('sleep for {} seconds'.format(sleep_time))
    return x + y
```

We need to our function work like this:


```python
from concurrent.futures import ThreadPoolExecutor, Future
pool = ThreadPoolExecutor(max_workers=8)
```
@inlined_future
def do_func(x, y):
   result = yield pool.submit(func, x, y)
   print('Got:', result)
Inspired by @contextmanager：

<img src="https://github.com/Motor-taxi-master-rider/Python/tree/master/Script/inline_yield.PNG">


```python
import wrapt

class Task:
    def __init__(self, gen):
        self._gen = gen
        initive = Future()
        initive.set_result(None)
        self.step(initive)

    def step(self, future):
        try:
            next_future = self._gen.send(future.result())
        except StopIteration as exc:
            if exc.value is not None:
                raise exc
        else:
            next_future.add_done_callback(self.step)

@wrapt.decorator
def inlined_future(wrapped, instance, args, kwargs):
    Task(wrapped(*args,**kwargs))
```


```python
@inlined_future
def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print('Got:', result)

def do_func_slow(x,y):
    result=func(x , y)
    print('Got:', result)
```


```python
for i in range(5):
    do_func_slow(i,i)
```

    sleep for 2.4873064812324777 seconds
    Got: 0
    sleep for 1.4432468827933995 seconds
    Got: 2
    sleep for 1.9532320529696823 seconds
    Got: 4
    sleep for 0.584825861467138 seconds
    Got: 6
    sleep for 1.8091265383050155 seconds
    Got: 8



```python
for i in range(5):
    do_func(i,i)
```

## Additional: How coroutine work


```python
import dis
import inspect

def gen_fn():
    result = yield 1
    print('result of yield: {}'.format(result))
    result2 = yield 2
    print('result of 2nd yield: {}'.format(result2))
    return 'done'

def normal_fn():
    return 1
```


```python
a = gen_fn()
```


```python
a.send(None)
```




    1




```python
gen_fn
```




    <function __main__.gen_fn>




```python
normal_fn
```




    <function __main__.normal_fn>




```python
bool(gen_fn.__code__.co_flags & inspect.CO_GENERATOR)
```




    True




```python
bin(inspect.CO_GENERATOR)
```




    '0b100000'




```python
bool(normal_fn.__code__.co_flags & inspect.CO_GENERATOR)
```




    False




```python
gen1 = gen_fn()

type(gen1)
```




    generator




```python
gen1.gi_code.co_name
```




    'gen_fn'



<img src="https://github.com/Motor-taxi-master-rider/Python/blob/master/Script/generator_object.PNG">

All generators from calls to gen_fn point to this same code. But each has its own stack frame. This stack frame is not on any actual stack, it sits in heap memory.


```python
gen2 = gen_fn()

gen1.gi_code is gen2.gi_code
```




    True




```python
gen1.gi_frame is gen2.gi_frame
```




    False




```python
gen1.send(None)

gen1.gi_frame.f_lasti
```




    2




```python
dis.dis(gen1)
```

      5           0 LOAD_CONST               1 (1)
                  2 YIELD_VALUE
                  4 STORE_FAST               0 (result)

      6           6 LOAD_GLOBAL              0 (print)
                  8 LOAD_CONST               2 ('result of yield: {}')
                 10 LOAD_ATTR                1 (format)
                 12 LOAD_FAST                0 (result)
                 14 CALL_FUNCTION            1
                 16 CALL_FUNCTION            1
                 18 POP_TOP

      7          20 LOAD_CONST               3 (2)
                 22 YIELD_VALUE
                 24 STORE_FAST               1 (result2)

      8          26 LOAD_GLOBAL              0 (print)
                 28 LOAD_CONST               4 ('result of 2nd yield: {}')
                 30 LOAD_ATTR                1 (format)
                 32 LOAD_FAST                1 (result2)
                 34 CALL_FUNCTION            1
                 36 CALL_FUNCTION            1
                 38 POP_TOP

      9          40 LOAD_CONST               5 ('done')
                 42 RETURN_VALUE



```python
gen1.send('hello')

gen1.gi_frame.f_lasti
```

    result of yield: hello





    22




```python
gen1.gi_frame.f_locals
```




    {'result': 'hello'}




```python
gen1.send('world')
```

    result of 2nd yield: world



    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-124-b432c08ca417> in <module>()
    ----> 1 gen1.send('world')


    StopIteration: done


    sleep for 0.9637312558255126 seconds
    Got: 8
    sleep for 1.0164703671835906 seconds
    Got: 2
    sleep for 1.0941822049442602 seconds
    Got: 4
    sleep for 2.2731928774129755 seconds
    Got: 0
    sleep for 2.4067928659249773 seconds
    Got: 6


## Reference

1. [Generators: The Final Frontier](http://www.dabeaz.com/finalgenerator/)
2. [Effective Python：Consider Coroutines to Run Many Functions Concurrently](http://www.effectivepython.com/2015/03/10/consider-coroutines-to-run-many-functions-concurrently/)
3. [Python Cookbook 3: 不用递归实现访问者模式](http://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p22_implementing_visitor_pattern_without_recursion.html)
4. [500 line or less:A Web Crawler With asyncio Coroutines](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)
5. [一个简单的文本解析计算器](https://motor-taxi-master-rider.github.io/python/2017/08/31/a-simple-text-complie-calculator-with-coroutine-and-other-tricks)
