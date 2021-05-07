---
layout: post
title: Java反射基础二三事
tags: Java,Reflection

---

> 来自：[Java核心技术(高阶)](https://www.icourse163.org/course/ECNU-1206500807)

在此总结在该MOOC课程中第三章Java反射作业中遇到的问题及迷思。

## 问题

```java
给定一个A.java，可以带包名。

//===========

class A

{

   public void f1()

  {

     System.out.println("hello java");

  }

}

//===========



再给定一个conf.txt，里面的内容如下

#==============

A,f1,5

#==============



请编写一个程序，读取conf.txt的第一行，自动按照每5秒执行一次A.f1()。
```



# 分析

这个问题的解决方案分为两个部分：

1. 读取文件并解析出所需的三个参数（类名，方法名，执行间隔）
2. 使用反射的方式动态执行方法

首先是读文件解析参数的代码：

```Java
String line = "";
try (var in = new Scanner(new FileInputStream("conf.txt"), StandardCharsets.UTF_8)) {
    line = in.nextLine();
}
```

这边用了`try-with-resource`语法糖。需要注意的是`conf.txt`需要存放在`System.getProperty("user.dir")`目录下而非是在`.java`文件的同级目录。额外的，因为Java有块级作用域的概念，所以`line`得定义在`try`块外部。

反射部分的代码：

```java
String[] tokens = line.split(",");
String cls = tokens[0];
String method = tokens[1];
Integer interval = Integer.parseInt(tokens[2]);
Class a = Class.forName(cls);
Method m = a.getMethod(method);
Constructor[] cs = a.getDeclaredConstructors();
Object o = null;
for (var c : cs) {
    if (c.getParameterCount() == 0) {
        o = c.newInstance();
    }
}
while (true) {
    m.invoke(o);
    Thread.currentThread().sleep(interval * 1000);
}
```

这部分我遇到了几个问题。

首先是第7行，刚开始我调用了`a.getConstructors()`方法，因此只能获取在`A`类里面定义的构造函数。`a.getDeclaredConstructors()`能获取所有包括父类中继承过来的构造函数。

在第15行，对于无参方法，课程中教的调用方法为`m.invoke(null)`。实际上这种方式只对静态方法访问不到`this`的方法有效，对于普通方法会抛出`NullPointerException`。根据[StackOverflow上](https://stackoverflow.com/questions/18802277/getting-java-lang-nullpointerexception-when-calling-method-invoke)的问题的提示，需要传入的参数为类的实例。

16行中，没有找到`Python`里`time.sleep`那样简单的睡眠方法，需要指明线程睡眠。



# 源代码

[链接](https://github.com/Motor-taxi-master-rider/Thoughts/blob/master/ScriptJava/MOOC_Core_Java_III/Main.java)

