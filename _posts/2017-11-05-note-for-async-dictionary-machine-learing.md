---
layout: post
title: Python async，dictionary，machine learning moudles笔记
tags:
- Async
- Dictionary
- Machine
categories:
- Python
description: weekly note of python documents and talks.
---


# Description
Jesse Jiryu Davis在 **Pycon2014** 的演讲[A. Jesse Jiryu Davis: What Is Async, How Does It Work, And When Should I Use It?](https://www.youtube.com/watch?v=9WV7juNmyE8)分析了为什么以及在什么情况下要用异步的方式处理io。之前在`300line`里，他和Guido合著的async crawler部分里就介绍了使用协程相对线程的优势：在python里线程需要50K的内存，而协程只需要3K。在该演讲中，他进一步阐述了协程的优势及应用场景。

Raymond Hettinger在 **Pycon2017** 的演讲[Modern Python Dictionaries A confluence of a dozen great ideas](https://www.youtube.com/watch?v=npw4s1QTmPg)和Brandon Rhodes的[The Dictionary Even Mightier](https://www.youtube.com/watch?v=66P5FMkWoVU)的主题是python字典在3.6版本的极大改进：减少20%-30%的内存占用及保持元素的插入顺序。

**TalkPython** 中Pete Garcin的访谈[Top 10 machine learning libraries](https://talkpython.fm/episodes/show/131/top-10-machine-learning-libraries)介绍了目前最流行的十个机器学习库，谈论了它们的异同以及初学者的学习路径。

# Async
Jesse举了纽约三种餐厅的例子作为三种不同场景。

第一个是三明治商店。顾客到柜台排队，厨师接到订单就开始制作三明治直到完成三明治。这个例子描述的是cpu密集型服务的机制，这里没有也无法使用异步机制，整个服务的吞吐量受到计算能力的限制。
<img src="https://motor-taxi-master-rider.github.io/assets/img/async_sample_subs.png"  title="{{Sandwich}}"/>

第二个是披萨店。顾客点单后，厨师需要将制作好的披萨用微波炉加热后交给顾客。由于需要等待披萨的加热，因此就有了异步操作的必要性。这种服务的吞吐量受到内存的限制，服务器也需要后台来处理pending的请求。
<img src="https://motor-taxi-master-rider.github.io/assets/img/async_sample_pizza.png"  title="{{Pizza}}"/>

第三个是一种寿司店。在这里顾客的需求由服务员告知厨房，同时厨房完成的寿司也需要服务器送到客户面前。现实中这样服务的例子就是谷歌邮箱服务：当客户登录谷歌邮箱之后并不会做太多动作，当客户收到邮件的这一事件发生的时候服务器才会将数据推到客户的面前。这就致使了大量长连接的产生。这些链接大部分的时间处于空闲状态，如果对每个链接都创建一个线程的话很快就会消耗完系统的内存。而异步正是为了最小化每个链接消耗的资源而诞生的。
<img src="https://motor-taxi-master-rider.github.io/assets/img/async_sample_omakase.png"  title="{{Omakase}}"/>

协程相对线程另一个区别与优点就是，当我们进行多线程编程时要时时注意竞态，导致我们不得不用锁来控制共享资源。这是由于线程是程序员并没有对线程的完全控制权导致的，我们并不能知道线程什么时候切换，什么时候运行和阻塞——我们将这些都交给操作系统来完成了。而协程则只会在yield处暂停和接受输入，我们完全可以控制整个异步过程。

在演讲的最后，Jesse告诉了我们哪类服务适合async而哪类不适合：
<img src="https://motor-taxi-master-rider.github.io/assets/img/async_should_use.png"  title="{{Should I Use It?}}"/>
他认为第二和第三种类型的服务是适合async的服务。这里也也指出了async的不足之处，async要求服务处理时至上而下每一部分都是异步的。因此我们的DB driver也需要支持异步，否则它将会阻塞整个程序。还有一点，async程序与线程编程将会非常不同，因此当你要实现一个异步服务时，一个async专家是必不可少的。

# Dictionary in 3.6
Brandon Rhodes在他的演讲中提到了十几年来python开发者为了使字典越来越人性化所做的努力：
- 在python2.6之前字典没有类似列表推导式的功能，python在3中加入了字典推导式并且回推给了2.7，使得字典不再是一个推导式的特例
- 字典的`keys()`等函数变成了生成器。为了和以前的借口，还实现了`__contains__`,`__sub__`,`__and__`,`__xor__`,`isdisjoint`,`__iter__`方法。这点也得益于python协议式的设计。
- 内存共享。同一个类的多个实例在内存中共享相同的`hashcode`和`key`的储存，使得python运行时刻的字典内存占用减少了10%-20%。字典创建在一个类的第一个实例`__init__`时，因此我们建议在类的`__init__`中初始化全部可能将要用到的实例变量，否则新的变量被添加时候将会用之前机制的变量字典，从而导致无法享受内存共享的优势。
- python为了防止因为hash conflict而引起的DOS攻击，在3.3版本中将hash方法的因子设置为一个随机值，因此我们每次从resize后的字典中取值时将会的到不同顺序的数值。
- SipHash是python3.4-3.6版本中对随机hash的替代。
- 受数据库及索引的启发，Raymond Hettinger在python3.6版本中部署了新的字典机制。原先的字典机制将会使字典哈希表保持1/3的空间来减少hash conflit的产生。这样每个空闲键值对将会产生24比特的内存浪费。新的机制用一个索引数组机制去除了这些空间的浪费并且使得字典中的键值对在字典resize后也能保持键值对的原本输入顺序。这个机制相较于3.5版本能减少字典20%至25%的内存使用。
- 现在每个字典会有个版本，这样我们处理当相同版本的字典时就不用从头遍历每一个字典了。

```python
dit = {-1: 'a'}
for i in range(27, 20, -1):
    dit[i] = i
print(list(dit.keys()))
for i in range(6, 20):
    dit[i] = i
print(list(dit.keys()))
```

以上这段代码在python2.7中由于resize可能会得到以下的结果：

```python
[21, 22, 23, 24, 25, 26, 27, -1]
[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, -1]
```

而在pytho3.6中则能保持元素录入的顺序：

```python
[-1, 27, 26, 25, 24, 23, 22, 21]
[-1, 27, 26, 25, 24, 23, 22, 21, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
```

# Machine learning libraries
在这个谈话中，Michael Kennedy和Pete Garcin谈论了他们认为的python最好的十个库。
- `Numpy`和`Scipy`是一切模块的基础。
- `Scikit-learn`是一个较早的模块，是`Scipy`家族的一部分。它提供给了我们一些常用的机器学习算法和分类，聚类，回归，模型工具。它非常简明直接，但缺少对GPU运算的支持。
- `Keras`是一个比较新的high-level模块，可以`Theano`,`Tensorflow`,`CNTK`中的任意一个模块作为后台。它的设计目标是机器学期程序的快速开发，因此具有极高的易用性。
- `Tensorflow`是现在热度最高的机器学习模块，它能充分利用GPU的矩阵及并行计算优势。而从Google要推出TPU这一举措来看，Google也正在大力推广这一模块。
- `Theano`比较老迈，也是同`Tensorflow`一样的low-level的机器学习模块。由于它的核心开发都跑去谷歌了，所以它和`Tensorflow`其实非常相像。
- 除了机器学习算法，为了获得干净的数据，我们也需要`Pandas`来帮助我们处理矩阵数据。它也是`Scipy`家族的一部分。
- `Caffe`和`Caffe2`是由Facebook在背后支持的机器视觉项目。它们针对互联网及移动部署做了相对的优化。
- `Jupyter`改变了数据科学家们交流和发表研究成果的方式。
- `CNTK`是微软最新的机器学习模块，擅长low-level的计算，如有向图。
- `NLTK`是一个相对成熟自然语言处理模块，擅长文本分析和处理。

Pete Garcin最后向初学者推荐了`Keras`作为了解机器学习的入口。

# Additional
