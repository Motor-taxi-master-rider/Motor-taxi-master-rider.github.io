# 掌握Python并发让你更快享用午餐

> 一个关于线程、异步、多进程和云函数的午餐故事。
>
> 原作者：[Brendan Maginnis](https://sourcery.ai/blog/concurrency/)

## 简介

我将给你们讲一个故事来解释Python中不同的并发和并行选项。

在这个故事中，我们将看到为什么单个人的多任务处理像并发，而多个人执行自己的任务就像并行处理。 我们将在一些知名餐厅的午餐时间观察这些场景在实际中是否可以快速而有效地为客户提供服务。之后，我将使用Python模拟各类餐厅，最后比较不同的并发方案，并说明它们分别适用与何种场景。

在接下来的内容中，我会解释如下几点：

* 并发和并行之间有什么区别？
* 比较不同的并发方案，包括线程，异步，多进程和云函数
* 每种并发方案的优缺点
* 如何使用简单的流程图找到适合场景的并发方案



## 什么是并发？什么是并行？

让我们从它们的定义说起：

>如果一个系统可以同时支持两个或多个正在进行的操作，则称该系统是并发的。
>
>如果一个系统可以支持同时执行的两个或多个动作，则称该系统为并行系统。
>
>这两个概念之间的关键区别是“进行中”这一定义。
>
>——《并发的艺术》

现在让我们直接进入故事环节。

正值午餐时间，你转过一条从未见过的街道。摆在你面前的有两种就餐选择：一个叫**Concurrent Burgers**的市场摊位和一个叫**Parallel Salads**的商店。

两家店看起来都很美味，但排队的人又很多，所以你想知道哪家能先为你服务。

**Concurrent Burgers**由一名中年女士经营，工作时开心大笑，手臂上有着Python的蟒蛇纹身。她正在执行以下任务：

* 拿取一个订单
* 翻转汉堡肉饼
* 将沙拉、肉饼和调味料加入，完成订单

她在各个任务之间无缝切换：首先，她检查烤架上的肉饼，然后取出煮熟的肉饼；之后，她取出一个订单；在之后如果有肉饼，她就可以完成一个多汁的汉堡，并结束订单。

**Parallel Salads**则配备了许多人手，在工作中他们时刻微笑并礼貌地和顾客交谈。他们每个人都分别为一名顾客做沙拉。他们取订单，将所有成分添加到干净的碗中，优雅而干练，将它们充分混合，之后将沙拉放入给顾客的容器中，把之前的碗递给另一名员工。那名员工与此同时负责洗碗的工作。

两家餐厅之间的主要区别在于工人的数量以及任务的执行方式：

* **Concurrent Burgers**同时（但不是并行的）有多个正在进行的任务，只有一个工人在所有的任务之间切换。
* **Parallel Salads**并行执行多项任务，多个工人同每人执行一项任务。

你会发现两家餐厅都能以相同的速度为顾客提供服务。**Concurrent Burgers**的女老板在同一时间制作多个汉堡，整体速度受限于她的小烤架烤熟肉饼的速度。**Parallel Salads**雇用了多名员工，每人分别制作一份沙拉，整体速度被混合每份沙拉的时间所限制。

你意识到**Concurrent Burgers**处理的是**I/O密集型**任务而**Parallel Salads**则处理的是**CPU密集型**任务。

* **I/O密集型**意味着程序主要受到I/O子系统的限制，从计算机的角度来讲，I/O意味着从磁盘读取或执行网络请求之类的操作。 在**Concurrent Burgers**中，烤肉饼就是一种I/O操作
* **CPU密集型**意味着程序主要受到CPU运算速度的限制。如果CPU运行速度更快，则程序运行速度也会得到极大提升。在**Parallel Salads**中，CPU运行速度对应了制作沙拉的人的速度。

面对这两个选择，你绞尽脑汁想了五分钟依然不知所措，无法做出决定，然后有个能拿主意的朋友打断了你，邀请你去排它们中某家的队。

请注意：**Concurrent Burgers**因为“同时进行两个或多个操作”既是并发的也是并行的。并行处理是并发处理的子集。

这两家店为并发任务和并行任务之间的区别提供了直觉感受。现在，我们将研究如何用Python代码实现这两者的模式。



### 我们有哪些选择？

Python中有两种选项用于并发：

* **threading**
* **asyncio**

有内置的库用于并行：

* **multiprocessing**

如果你在云服务中运行python程序，还有另一个用于并行的选项：

* **cloud functions**



## 并发实战

让我们看一下使用**threading**和**asyncio**的两种**Concurrent Burgers**的可能实现。在这两种情况下，只有一个工人接单，烤肉饼，做汉堡。

对于**threading**和**asyncio**，只有一个处理器在执行任务，因此它在需要处理的不同任务之间进行切换。线程和异步之间的区别是如何决定任务该被切换。

* 对于**threading**库，操作系统掌握了不同线程的信息，可以在任何时候中断它们并切换成其他任务。程序本身对此没有控制权。这种模式被称为[抢先式多任务处理](https://en.wikipedia.org/wiki/Preemption_%28computing%29#Preemptive_multitasking)，因为操作系统可以抢占你的线程来进行线程间的切换在大多数编程语言中，线程可以在多核上并行运行，然而在Python中，一次只能执行一个线程。
* 借助**asyncio**，程序本身可以决定何时在任务之间进行切换 每个任务在准备好切换时都可以选择放弃控制，从而与其他任务协作。因此，这被称为[协作多任务处理](https://en.wikipedia.org/wiki/Cooperative_multitasking)，因为每个任务必须在无法继续进行时主动放弃控制权来相互协作。



### **Concurrent Burgers** 的线程实现

**threading**库可以让工人在执行过程中随时切换任务。工人可能在取单到一半时突然切换到检查肉饼或做汉堡的任务中，之后在任意时刻又可能再次切换到其他任务之中。

让我们看下用线程实现的**Concurrent Burgers**：

```python
from concurrent.futures import ThreadPoolExecutor
import queues


# 注意: 为了让你专注于实现细节，有些方法和变量被忽略了


def run_concurrent_burgers():
    # 创建阻塞队列
    customers = queue.Queue()
    orders = queue.Queue(maxsize=5)  # 一次最多处理五个订单
    cooked_patties = queue.Queue()

    # 烤架完全独立于工人,它能将生肉饼变成熟肉饼
    # 这部分就像从磁盘I/O或者网络请求一样
    grill = Grill()

    # 在线程池中运行三个任务
    with ThreadPoolExecutor() as executor:
        executor.submit(take_orders, customers, orders)
        executor.submit(cook_patties, grill, cooked_patties)
        executor.submit(make_burgers, orders, cooked_patties)


def take_orders(customers, orders):
    while True:
        customer = customers.get()
        order = take_order(customer)
        orders.put(order)


def cook_patties(grill, cook_patties):
    for position in range(len(grill)):
        grill[position] = raw_patties.pop()

    while True:
        for position, patty in enumerate(grill):
            if patty.cooked:
                cooked_patties.put(patty)
                grill[position] = raw_patties.pop()

        # 等一分钟之后再次检查
        threading.sleep(60)


def make_burgers(orders, cooked_patties):
    while True:
        patty = cooked_patties.get()
        order = orders.get()
        burger = order.make_burger(patty)
        customer = order.shout_for_customer()
        customer.serve(burger)
```

接受订单，烹饪肉饼和制作汉堡的这几个任务都是一个无限循环，不断地被执行。

`run_concurrent_burgers`中，我们在单独的线程中启动每个任务。可以手动地为每个任务创建一个线程，但是标准库中存在一个更好的接口，叫做`ThreadPoolExecutor`，它会为提交给它的每个任务创建一个线程。

当进行多线程编程时，我们必须确保一次只有一个线程正在读取或写入某个状态。否则，我们可能会遇到两个线程都握着同一块馅饼的情况，最终我们就要面对一个相当生气的客户了。这类问题被称为**线程安全**。

为避免此问题，我们使用`Queue`传递状态。在各个任务中，调用`Queues`的`get`会**阻塞**，直到有客户，订单或馅饼就绪。操作系统不会尝试切换到任何阻塞的线程，这使我们可以轻松安全地切换状态。只要线程将状态放入`Queue`的中并不再使用它，那么获取状态的线程就知道在使用该状态时时不会有其它线程对其进行更改。

#### threading的优点

* I/O过程不会阻塞其他任务
* Python不同版本和库出色支持——如果程序可以单线程运行，则绝大多数情况下它也可以用多线程运行

#### threading的缺点

* 由于系统线程之间切换的开销，性能比`asyncio`差
* 不是线程安全的
* 无法加速处理色拉之类的CPU约束问题（因为Python[仅允许一个线程同时运行](https://wiki.python.org/moin/GlobalInterpreterLock)）——单个工人同时制作多个沙拉的速度不会比他们一个个顺序制作沙拉快，因为制作所有沙拉需要花费的时间总量相同。



### **Concurrent Burgers** 的asyncio实现

在**asyncio**中，事件循环(**event loop**)管理着所有的任务。任务们可以处于各种不同的状态，最重要的两个状态是就绪态(**ready**)和等待态(**waiting**)。在每次循环中，事件循环都会检查是否有之前处于等待的任务由于其他人物的完成而就绪。然后，它会选择一个就绪的任务并运行它，直到任务完成或需要等待另一个任务为止。通常任务等待的是一种I/O操作，例如磁盘读写或发出http请求。

两个关键字可以涵盖大多数**asyncio**的用法：**async**和**await**。

* **async**用于标记某一函数必须作为单独的任务运行。
* **await**会创建一个新任务，并放弃对事件循环的控制。它将任务置于等待状态，在新任务完成时再次变成就绪态。

让我们看下用**asyncio**实现的**Concurrent Burgers**：

```python
import asyncio

# 注意: 为了让你专注于实现细节，有些方法和变量被忽略了


def run_concurrent_burgers():
    # 这些队列用于放弃控制
    customers = asyncio.Queue()
    orders = asyncio.Queue(maxsize=5)  # 一次最多处理五个订单
    cooked_patties = asyncio.Queue()

    # 烤架完全独立于工人,它能将生肉饼变成熟肉饼
    grill = Grill()

    # 在默认的asyncio event loop中执行所有任务
    asyncio.gather(
        take_orders(customers, orders),
        cook_patties(grill, cooked_patties),
        make_burgers(orders, cooked_patties),
    )


# 用async def来定义asyncio任务
async def take_orders(customers, orders):
    while True:
        # 允许在这里和下面的的await中切换到其他任务
        customer = await customers.get()
        order = take_order(customer)
        await orders.put(order)


async def cook_patties(grill, cooked_patties):
    for position in range(len(grill)):
        grill[position] = raw_patties.pop()

    while True:
        for position, patty in enumerate(grill):
            if patty.cooked:
                # put_noawait允许我们在不创建新任务放弃控制器
                # 的前提下往队列里添加元素
                cooked_patties.put_noawait(patty)
                grill[position] = raw_patties.pop()

        # 等30秒之后再次检查
        await asyncio.sleep(30)


async def make_burgers(orders, cooked_patties):
    while True:
        patty = await cooked_patties.get()
        order = await orders.get()
        burger = order.make_burger(patty)
        customer = await order.shout_for_customer()
        customer.serve(burger)
```

所有取单、烤肉饼和制作汉堡包的任务都使用`async def`声明。

在这些任务中，工作单元每次调用`await`都会切换到新任务。等待发生在以下时刻：

* 接受订单阶段
  * 将要与下一个客户交谈时
  * 将订单添加到订单队列时
* 烹调阶段
  * 当所有的肉饼都经过检查时
* 制作汉堡阶段
  * 等待煮熟的小馅饼时
  * 等待订单时
  * 给顾客上餐汉堡时

拼图的最后一块是在`run_concurrent_burger`中，调用`asyncio.gather`安排了之后由事件循环执行的所有任务，在本例中就是餐厅的工作人员。

既然我们确切地知道任务何时切换，那实际上并不需要如此小心地共享状态。我们仅用列表来替代队列就能实现目标，并且，两个任务不会因此在某一时刻持有同一块馅饼。虽然如此，我还是强烈建议使用`asyncio`队列。因为它提供了明智的挂起时点，使得我们可以非常轻松地完成任务之间的协作。

使用`asyncio`的另一个有趣的方面是`async`关键字会更改该函数的接口。因为它不能直接调用非异步函数。这同时可以被认为是一件好事和坏事。一方面，你可能会说这会损害代码的可组合性：因为你将无法混用异步函数和正常函数。另一方面，如果`asyncio`仅用于I/O，它会强制将I/O与业务逻辑分离，从而把`asyncio`代码限制在应用程序的边缘，使得代码库更易于理解和测试。在静态类型函数语言中，显式标记I/O是相当普遍的做法——这在Haskell中是必需的。

#### Asyncio的优点

* 对于I/O密集型程序而言非常快
  * 由于只有一个系统线程，所以开销比线程更少
  * 所有高性能的Web服务器框架都在使用`asyncio`——查看[测试跑分](https://www.techempower.com/benchmarks/#section=data-r19&hw=ph&test=fortune&l=zijzen-1r)
* 线程安全

#### Asyncio的缺点
* 无法加快CPU密集型问题
* Python的新特性
  * 需求Python 3.5+
  * 对大多数I/O场景都有支持，但不像非`asyncio`方案那样完整