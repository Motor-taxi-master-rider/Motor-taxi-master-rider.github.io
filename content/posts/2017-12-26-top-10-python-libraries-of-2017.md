---
layout: post
title: Top 10 Python libraries of 2017
tags: Python
category: Python
---


<section class="blog-single-post__content">


<p>December is the time when you sit back and think about the accomplishments of the past year. For us programmers, this is often looking at the <strong>open source libraries</strong> that were either released this year (or close enough), or whose popularity has recently boomed because they are simply great tools to solve a particular problem.</p>

<p>For the past <a href="/blog/2016/12/20/top-10-python-libraries-of-2016/">two</a> <a href="/blog/2015/12/15/top-10-python-libraries-of-2015/">years</a>, we have done this in the form of a blog post with what we consider to be some of the best work that has been done in the Python community. Now, as we are wrapping up 2017, we had to do the same.</p>

<p>This time, the list comes with a <em>Machine Learning (ML) flavor</em>. Forgive us, authors of great non-ML libraries, but we are just too biased ;) Hopefully, people in the comments help us do some justice and mention other great pieces of software, some of which have surely have escaped our radar.</p>

<p>So, without further ado, here it goes!</p>


<h2 id="1-pipenv-https-github-com-pypa-pipenv">1. <a href="https://github.com/pypa/pipenv">Pipenv</a></h2>

<p>We couldn’t make this list without reserving the top spot for a tool that was only released early this year, but has the power to affect the workflow of every Python developer, especially more now since it has become the <a href="https://packaging.python.org/tutorials/managing-dependencies/#installing-pipenv">officially recommended tool on Python.org</a> for managing dependencies!</p>

<p>Pipenv, originally started as a <a href="https://www.kennethreitz.org/essays/announcing-pipenv">weekend project</a> by the awesome <a href="https://twitter.com/kennethreitz">Kenneth Reitz</a>, aims to bring ideas from other package managers (such as <a href="https://www.npmjs.com/">npm</a> or <a href="https://yarnpkg.com">yarn</a>) into the Python world. Forget about installing <a href="https://virtualenv.pypa.io/en/stable/">virtualenv</a>, <a href="https://virtualenvwrapper.readthedocs.io/en/latest/">virtualenvwrapper</a>, managing <code>requirements.txt</code> files and ensuring reproducibility with regards to versions of dependencies of the dependencies (read <a href="https://www.kennethreitz.org/essays/a-better-pip-workflow">here</a> for more info about this). With Pipenv, you specify all your dependencies in a <code>Pipfile</code> — which is normally built by using commands for adding, removing, or updating dependencies. The tool can generate a <code>Pipfile.lock</code> file, enabling your builds to be <em>deterministic</em>, helping you avoid those difficult to catch bugs because of some obscure dependency that you didn’t even think you needed.</p>

<p>Of course, Pipenv comes with many other perks and has <a href="https://docs.pipenv.org/">great documentation</a>, so make sure to check it out and start using it for all your Python projects, as we do at Tryolabs :)</p>

<h2 id="2-pytorch-http-pytorch-org">2. <a href="http://pytorch.org/">PyTorch</a></h2>

<p>If there is a library whose popularity has boomed this year, especially in the Deep Learning (DL) community, it’s PyTorch, the DL framework introduced by Facebook this year.</p>

<p>PyTorch builds on and improves the (once?) popular Torch framework, especially since it’s Python based — in contrast with Lua. Given how people have been switching to Python for doing data science in the last couple of years, this is an important step forward to make DL more accessible.</p>

<p>Most notably, PyTorch has become one of the go-to frameworks for many researchers, because of its implementation of the novel <em>Dynamic Computational Graph</em> paradigm. When writing code using other frameworks like <a href="https://www.tensorflow.org/">TensorFlow</a>, <a href="https://github.com/Microsoft/CNTK">CNTK</a> or <a href="https://mxnet.incubator.apache.org/">MXNet</a>, one must first define something called a <em>computational graph</em>. This graph specifies all the operations that will be run by our code, which are later <em>compiled</em> and potentially <em>optimized</em> by the framework, in order to allow for it to be able to run even faster, and in parallel on a GPU. This paradigm is called <em>Static Computational Graph</em>, and is great since you can leverage all sorts of optimizations and the graph, once built, can potentially run in different devices (since <em>execution</em> is separate from <em>building</em>). However, in many tasks such as Natural Language Processing, the amount of “work” to do is often variable: you can resize images to a fixed resolution before feeding them to an algorithm, but cannot do the same with sentences which come in variable length. This is where PyTorch and dynamic graphs shine, by letting you use standard Python control instructions in your code, the graph will be defined when it is executed, giving you a lot of freedom which is essential for several tasks.</p>

<p>Of course, PyTorch also <a href="http://pytorch.org/docs/master/autograd.html">computes gradients for you</a> (as you would expect from any modern DL framework), is very fast, and <a href="http://pytorch.org/docs/master/notes/extending.html">extensible</a>, so why not give it a try?</p>

<h2 id="3-caffe2-https-caffe2-ai">3. <a href="https://caffe2.ai">Caffe2</a></h2>

<p>It might sound crazy, but Facebook also released another great DL framework this year.</p>

<p>The original <a href="http://caffe.berkeleyvision.org/">Caffe framework</a> has been widely used for years, and known for unparalleled performance and battle-tested codebase. However, recent trends in DL made the framework stagnate in some directions. Caffe2 is the attempt to bring Caffe to the modern world.</p>

<p>It supports distributed training, deployment (even in mobile platforms), the newest CPUs and CUDA-capable hardware. While PyTorch may be better for research, Caffe2 is suitable for large scale deployments as seen on Facebook.</p>

<p>Also, check out the <a href="https://research.fb.com/facebook-and-microsoft-introduce-new-open-ecosystem-for-interchangeable-ai-frameworks/">recent ONNX effort</a>. You can build and train your models in PyTorch, while using Caffe2 for deployment! Isn’t that great?</p>

<h2 id="4-pendulum-https-github-com-sdispater-pendulum">4. <a href="https://github.com/sdispater/pendulum">Pendulum</a></h2>

<p>Last year, <a href="https://github.com/crsmithdev/arrow">Arrow</a>, a library that aims to make your life easier while working with datetimes in Python, made the list. This year, it is the turn of Pendulum.</p>

<p>One of Pendulum’s strength points is that it is a drop-in replacement for Python’s standard <code>datetime</code> class, so you can easily integrate it with your existing code, and leverage its functionalities only when you actually need them. The authors have put special care to ensure timezones are handled correctly, making every instance timezone-aware and UTC by default.  You will also get an extended <code>timedelta</code> to make datetime arithmetic easier.</p>

<p>Unlike other existing libraries, it strives to have an API with predictable behavior, so you know what to expect. If you are doing any non trivial work involving datetimes, this will make you happier! Check out <a href="https://pendulum.eustace.io/docs/">the docs</a> for more.</p>

<h2 id="5-dash-https-plot-ly-products-dash">5. <a href="https://plot.ly/products/dash/">Dash</a></h2>

<p>You are doing data science, for which you use the excellent available tools in the Python ecosystem like <a href="https://pandas.pydata.org/">Pandas</a> and <a href="http://scikit-learn.org/">scikit-learn</a>. You use <a href="https://jupyter.org/">Jupyter Notebooks</a> for your workflow, which is great for you and your colleagues. But how do you share the work with people who do not know how to use those tools? How do you build an interface so people can easily play around with the data, visualizing it in the process? It used to be the case that you needed a dedicated frontend team, knowledgeable in Javascript, for building these GUIs. Not anymore.</p>

<p>Dash, <a href="https://medium.com/@plotlygraphs/introducing-dash-5ecf7191b503">announced this year</a>, is an <a href="https://github.com/plotly/dash">open source</a> library for building web applications, especially those that make good use of data visualization, in pure Python. It is built on top of <a href="http://flask.pocoo.org/">Flask</a>, <a href="https://plot.ly/javascript/">Plotly.js</a> and <a href="https://reactjs.org/">React</a>, and provides abstractions that free you from having to learn those frameworks and let you become productive quickly. The apps are rendered in the browser and will be responsive so they will be usable in mobile devices.</p>

<p>If you would like to know more about what is possible with Dash, the <a href="https://plot.ly/dash/gallery">Gallery</a> is a great place for some eye-candy.</p>

<h2 id="6-pyflux-https-github-com-rjt1990-pyflux">6. <a href="https://github.com/RJT1990/pyflux">PyFlux</a></h2>

<p>There are many libraries in Python for doing data science and ML, but when your data points are metrics that evolve over time (such as stock prices, measurements obtained from instruments, etc), that is not the case.</p>

<p>PyFlux is an open source library in Python built specifically for working with <strong>time series</strong>. The study of time series is a subfield of statistics and econometrics, and the goals can be describing how time series behave (in terms of latent components or features of interest), and also predicting how they will behave the future.</p>

<p>PyFlux allows for a probabilistic approach to time series modeling, and has implementations for several modern time series models like <a href="https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity">GARCH</a>. Neat stuff.</p>

<h2 id="7-fire-https-github-com-google-python-fire">7. <a href="https://github.com/google/python-fire">Fire</a></h2>

<p>It is often the case that you need to make a Command Line Interface (CLI) for your project. Beyond the traditional <a href="https://docs.python.org/3/library/argparse.html">argparse</a>, Python has some great tools like <a href="http://click.pocoo.org">click</a> or <a href="http://docopt.org/">docopt</a>. Fire, <a href="https://opensource.googleblog.com/2017/03/python-fire-command-line.html">announced by Google this year</a>, has a different take on solving this same problem.</p>

<p>Fire is an open source library that can <em>automatically</em> generate a CLI for any Python project. The key here is <em>automatically</em>: you almost don’t need to write any code or docstrings to build your CLI! To do the job, you only need to call a <code>Fire</code> method and pass it whatever you want turned into a CLI: a function, an object, a class, a dictionary, or even pass no arguments at all (which will turn your entire code into a CLI).</p>

<p>Make sure to read <a href="https://github.com/google/python-fire/blob/master/docs/guide.md">the guide</a> so you understand how it works with examples. Keep it under your radar, because this library can definitely save you a lot of time in the future.</p>

<h2 id="8-imbalanced-learn-https-github-com-scikit-learn-contrib-imbalanced-learn">8. <a href="https://github.com/scikit-learn-contrib/imbalanced-learn">imbalanced-learn</a></h2>

<p>In an ideal world, we would have perfectly balanced datasets and we would all train models and be happy. Unfortunately, the real world is not like that, and certain tasks favor very imbalanced data. For example, when predicting fraud in credit card transactions, you would expect that the vast majority of the transactions (+99.9%?) are actually legit. Training ML algorithms naively will lead to dismal performance, so extra care is needed when working with these types of datasets.</p>

<p>Fortunately, this is a studied research problem and a variety of techniques exist. Imbalanced-learn is a Python package which offers implementations of some of those techniques, to make your life much easier.  It is compatible with <a href="http://scikit-learn.org/stable/">scikit-learn</a> and is part of <a href="https://github.com/scikit-learn-contrib">scikit-learn-contrib</a> projects. Useful!</p>

<h2 id="9-flashtext-https-github-com-vi3k6i5-flashtext">9. <a href="https://github.com/vi3k6i5/flashtext">FlashText</a></h2>

<p>When you need to search for some text and replace it for something else, as is standard in most data-cleaning work, you usually turn to regular expressions. They will get the job done, but sometimes it happens that the number of terms you need to search for is in the thousands, and then, reg exp can become painfully slow to use.</p>

<p>FlashText is a better alternative just for this purpose. In the <a href="https://medium.freecodecamp.org/regex-was-taking-5-days-flashtext-does-it-in-15-minutes-55f04411025f">author’s initial benchmark</a>, it improved the runtime of the entire operation by a huge margin: from 5 days to 15 minutes. The beauty of FlashText is that the runtime is the same no matter how many search terms you have, in contrast with regexp in which the runtime will increase almost linearly with the number of terms.</p>

<p>FlashText is a testimony to the importance of the design of algorithms and data structures, showing that, even for simple problems, better algorithms can easily outdo even the fastest CPUs running naive implementations.</p>

<h2 id="10-luminoth-https-luminoth-ai">10. <a href="https://luminoth.ai/">Luminoth</a></h2>

<p><em>Disclaimer: this library was built by Tryolabs’ R&amp;D area.</em></p>

<p>Images are everywhere nowadays, and understanding their content can be critical for several applications. Thankfully, image processing techniques have advanced a lot, fueled by the advancements in DL.</p>

<p>Luminoth is an open source Python toolkit for computer vision, built using <a href="https://www.tensorflow.org/">TensorFlow</a> and <a href="https://github.com/deepmind/sonnet">Sonnet</a>. Currently, it out-of-the-box supports object detection in the form of a model called Faster R-CNN.</p>

<p>But Luminoth is not only an implementation of a particular model. It is built to be modular and extensible, so customizing the existing pieces or extending it with new models to tackle different problems should be straightforward, with as much code reuse as there can be. It provides tools for easily doing the engineering work that are needed when building DL models: converting your data (in this case, images) to adequate format for feeding your data pipeline (<a href="https://www.tensorflow.org/programmers_guide/datasets#consuming_tfrecord_data">TensorFlow’s tfrecords</a>), doing data augmentation, running the training in one or multiple GPUs (distributed training will be a must when working with large datasets), running evaluation metrics, easily <a href="https://www.tensorflow.org/get_started/summaries_and_tensorboard">visualizing stuff in TensorBoard</a> and deploying your trained model with a simple API or browser interface, so people can play around with it.</p>

<p>Moreover, Luminoth has straightforward integration with <a href="https://cloud.google.com/ml-engine/">Google Cloud’s ML Engine</a>, so even if you don’t own a powerful GPU, you can train in the cloud with a single command, just as you do in your own local machine.</p>

<p>If you are interested in learning more about what’s behind the scenes, you can read the <a href="https://tryolabs.com/blog/2017/10/10/launching-luminoth-our-open-source-computer-vision-toolkit/">announcement blog post</a> and watch the <a href="https://tryolabs.com/blog/2017/11/15/our-odsc-talks-in-video/">video of our talk</a> at ODSC.</p>

<h2 id="bonus-watch-out-for-these">Bonus: watch out for these</h2>

<h3 id="pyvips-https-github-com-jcupitt-pyvips"><a href="https://github.com/jcupitt/pyvips">PyVips</a></h3>

<p>You may have never heard of the <a href="https://jcupitt.github.io/libvips/">libvips</a> library. In that case, you must know that it’s an image processing library, like <a href="https://pillow.readthedocs.io/">Pillow</a> or <a href="https://www.imagemagick.org/">ImageMagick</a>, and supports a wide range of formats. However, when comparing to other libraries, <a href="https://github.com/jcupitt/libvips/wiki/Speed-and-memory-use">libvips is faster and uses less memory</a>. For example, <a href="https://github.com/jcupitt/vips-benchmarks">some benchmarks</a> show it to be about 3x faster and use less than 15x memory as ImageMagick. You can read more about why libvips is nice <a href="https://github.com/jcupitt/libvips/wiki/Why-is-libvips-quick">here</a>.</p>

<p>PyVips is a recently released Python binding for libvips, which is compatible with Python 2.7-3.6 (and even PyPy), easy to install with <code>pip</code> and drop-in compatible with the old binding, so if you are using that, you don’t have to modify your code.</p>

<p>If doing some sort of image processing in your app, definitely something to keep an eye on.</p>

<h3 id="requestium-https-github-com-tryolabs-requestium"><a href="https://github.com/tryolabs/requestium">Requestium</a></h3>

<p><em>Disclaimer: this library was built by Tryolabs.</em></p>

<p>Sometimes, you need to automatize some actions in the web. Be it when scraping sites, doing application testing, or filling out web forms to perform actions in sites that do not expose an API, automation is always necessary. Python has the excellent <a href="https://github.com/requests/requests">Requests</a> library which allows you perform some of this work, but unfortunately (or not?) many sites make heavy client side use of Javascript. This means that the HTML code that Requests fetches, in which you could be trying to find a form to fill for your automation task, may not even have the form itself! Instead, it will be something like an empty <em>div</em> of some sort that will be generated in the browser with a modern frontend library such as <a href="https://reactjs.org/">React</a> or <a href="https://vuejs.org/">Vue</a>.</p>

<p>One way to solve this is to reverse-engineer the requests that Javascript code makes, which will mean many hours of debugging and fiddling around with (probably) uglified JS code. No thanks. Another option is to turn to libraries like <a href="https://selenium-python.readthedocs.io/">Selenium</a>, which allow you to programmatically interact with a web browser and run the Javascript code. With this, the problems are no more, but it is still slower than using plain Requests which adds very little overhead.</p>

<p>Wouldn’t it be cool if there was a library that let you start out with Requests and seamlessly switch to Selenium, only adding the overhead of a web browser when actually needing it? Meet Requestium, which acts as a drop-in replacement for Requests and does just that. It also integrates <a href="https://github.com/scrapy/parsel">Parsel</a>, so writing all those selectors for finding the elements in the page is much cleaner than it would otherwise be, and has helpers around common operations like clicking elements and making sure stuff is actually rendered in the DOM. Another time saver for your web automation projects!</p>

<h3 id="skorch-https-github-com-dnouri-skorch"><a href="https://github.com/dnouri/skorch">skorch</a></h3>

<p>You like the awesome API of scikit-learn, but need to do work using PyTorch? Worry not, skorch is a wrapper which will give PyTorch an interface like sklearn. If you are familiar with those libraries, the syntax should be straightforward and easy to understand. With skorch, you will get some code abstracted away, so you can focus more on the things that really matter, like doing your data science.</p>

<h2 id="conclusion">Conclusion</h2>

<p>What an exciting year! If you know of a library that deserves to be on this list, make sure you mention it in the comments below. There are so many good developments that it’s hard to keep up. As usual, thanks to everybody in the community for such great work!</p>

<p>Finally, don’t forget to <a href="#subscribe">subscribe to our newsletter</a> so that you don’t miss out future editions of this post or our ML related content.</p>

    </section>
