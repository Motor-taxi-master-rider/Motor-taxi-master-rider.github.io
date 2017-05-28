---
layout: post
title: Markdown Syntax
tags:
- Markdown
categories: Python
description: The Hamming distance between two integers is the number of positions at which the corresponding bits are different.Given two integers x and y, calculate the Hamming distance.
---
# Please Note:
This is an unofficial kramdown sandbox, the official complete documentation for [kramdown](https://github.com/gettalong/kramdown/) is [here](http://kramdown.rubyforge.org/).

[documentation](https://kramdown.gettalong.org/quickref.html)

-----

### Code
This demo uses [highlight.js](http://softwaremaniacs.org/soft/highlight/en/) to enable client-side syntax highlighting

`inline` or as a block (auto detect language):

~~~
def ruby
  puts "ruby"
end
~~~

~~~
def hello():
  print "python"
~~~

Force language:

~~~ javascript
function hello() {
  alert("Javascript");
}
~~~

----

### Lists

1. One
2. Two
3. Three

* Lorem
* Ipsum
  * Dolar
  * Etc.
* Dolar

Example
: Meep
: Meep



----

### LaTeX

Using [MathJax](http://www.mathjax.org/).

Inline: $$ \varphi = \frac{1+\sqrt{5}}{2} = 1.61803\,39887\ldots. $$

Block:

$$

\int_0^{2\pi}\sin{x}\ dx=0
$$


----

### Tables

| Header1 | Header2 | Header3 |
|:--------|:-------:|--------:|
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|----
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|=====
| Foot1   | Foot2   | Foot3
{: rules="groups"}

etc.
