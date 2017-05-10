---
title: Top 10 Python libraries of 2016
date: 2017-05-06 00:00:00
tags:
- Python
categories:
- Python
---
description: we try to avoid most established choices such as Django, Flask, etc. that are kind of standard nowadays. Also, some of these libraries date prior to 2016, but either they had an explosion in popularity this year or we think they are great enough to deserve the spot. Here we go!
<!-- more -->
<div class="post">
    <p>Last year, we did a recap with what we thought were the <a href="https://tryolabs.com/blog/2015/12/15/top-10-python-libraries-of-2015/">best Python libraries of 2015</a>, which was widely shared within the Python community (see post in<a href="https://www.reddit.com/r/Python/comments/3wyiuv/top_10_python_libraries_of_2015/">r/Python</a>).
        A year has gone by, and again it is time to give due credit for the awesome work that has been done by the <strong>open source community</strong> this year.</p>
    <p>Again, we try to avoid most established choices such as Django, Flask, etc. that are kind of standard nowadays. Also, some of these libraries date prior to 2016, but either they had an explosion in popularity this year or we think they are great enough
        to deserve the spot. Here we go!</p>
    <h2>1. <a href="https://www.zappa.io/">Zappa</a></h2>
    <p>Since the release of <a href="https://aws.amazon.com/lambda/details/">AWS Lambda</a> (and <a href="https://cloud.google.com/functions/docs/">others</a> that <a href="https://azure.microsoft.com/en-us/services/functions/">have</a> <a href="https://www.ibm.com/cloud-computing/bluemix/openwhisk">followed</a>),
        all the rage has been about <a href="http://martinfowler.com/articles/serverless.html">serverless architectures</a>. These allow microservices to be deployed in the cloud, in a fully managed environment where one doesn’t have to care about managing
        any server, but is assigned stateless, ephemeral <em>computing containers</em> that are fully managed by a provider. With this paradigm, events (such as a traffic spike) can trigger the execution of more of these <em>containers</em> and therefore
        give the possibility to handle “infinite” horizontal scaling.</p>
    <p>Zappa is <strong>the serverless framework for Python</strong>, although (at least for the moment) it only has support for AWS Lambda and AWS API Gateway. It makes building so-architectured apps very simple, freeing you from most of the tedious setup
        you would have to do through the AWS Console or API, and has all sort of commands to ease deployment and managing different environments.</p>
    <h2>2. <a href="https://github.com/channelcat/sanic">Sanic</a> + <a href="https://magic.io/blog/uvloop-blazing-fast-python-networking/">uvloop</a></h2>
    <p>Who said Python couldn’t be fast? Apart from competing for the <a href="http://knowyourmeme.com/memes/sanic-hegehog">best name</a> of a software library ever, Sanic also competes for the fastest Python web framework ever, and appears to be the winner
        by a clear margin. It is a Flask-like Python 3.5+ web server that is designed for speed. Another library, <em>uvloop</em>, is an ultra fast drop-in replacement for <em>asyncio</em>’s event loop that uses <a href="https://github.com/libuv/libuv">libuv</a>        under the hood. Together, these two things make a great combination!</p>
    <p>According to the Sanic author’s <a href="https://github.com/channelcat/sanic#benchmarks">benchmark</a>, <em>uvloop</em> could power this beast to handle more than <strong>33k requests/s</strong> which is just insane (and faster than <em>node.js</em>).
        Your code can benefit from the new <em>async/await</em> syntax so it will look neat too; besides we love the Flask-style API. Make sure to give Sanic a try, and if you are using <em>asyncio</em>, you can surely benefit from <em>uvloop</em> with
        very little change in your code!</p>
    <h2>3. <a href="https://github.com/MagicStack/asyncpg">asyncpg</a></h2>
    <p>In line with recent developments for the <em>asyncio</em> framework, the folks from<a href="https://magic.io/">MagicStack</a> bring us this efficient asynchronous (currently CPython 3.5 only) database interface library designed specifically for PostgreSQL.
        It has zero dependencies, meaning there is no need to have <em>libpq</em> installed. In contrast with <em>psycopg2</em> (the most popular PostgreSQL adapter for Python) which exchanges data with the database server in text format, <em>asyncpg</em>        implements PostgreSQL <strong>binary I/O protocol</strong>, which not only allows support for generic types but also comes with numerous performance benefits.</p>
    <p>The benchmarks are clear: <em>asyncpg</em> is on average, at least <strong>3x faster</strong> than <em>psycopg2</em> (or <em>aiopg</em>), and faster than the <em>node.js</em> and <em>Go</em> implementations.</p>
    <h2>4. <a href="https://github.com/boto/boto3">boto3</a></h2>
    <p>If you have your infrastructure on AWS or otherwise make use of their services (such as S3), you should be very happy that <a href="https://github.com/boto/boto">boto</a>, the Python interface for AWS API, got a completely rewrite from the ground
        up. The great thing is that you don’t need to migrate your app all at once: you can use <em>boto3</em> and <em>boto</em> (2) <em>at the same time</em>; for example using boto3 only for new parts of your application.</p>
    <p>The new implementation is much <strong>more consistent</strong> between different services, and since it uses a data-driven approach to generate classes at runtime from JSON description files, it will always get fast updates. No more lagging behind
        new Amazon API features, move to <em>boto3</em>!</p>
    <h2>5. <a href="https://www.tensorflow.org/">TensorFlow</a></h2>
    <p>Do we even need an introduction here? Since it was released by Google in November 2015, this library has gained a huge momentum and has become the #1 trendiest GitHub Python repository. In case you have been living under a rock for the past year,
        TensorFlow is a library for <strong>numerical computation</strong> using data flow graphs, which can run over GPU or CPU.</p>
    <p>We have quickly witnessed it become a trend in the Machine Learning community (especially Deep Learning, see our post on <a href="https://tryolabs.com/blog/2016/11/18/10-main-takeaways-from-mlconf/">10 main takeaways from MLconf</a>), not only growing
        its uses in research but also being widely used in production applications. If you are doing Deep Learning and want to use it through a higher level interface, you can try using it as a backend for <a href="https://keras.io/">Keras</a> (which
        made it to last years post) or the newer <a href="https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/slim">TensorFlow-Slim</a>.</p>
    <h2>6. <a href="https://gym.openai.com/">gym</a> + <a href="https://universe.openai.com/">universe</a></h2>
    <p>If you are into AI, you surely have heard about the <a href="https://openai.com/">OpenAI</a> non-profit artificial intelligence research company (backed by Elon Musk et al.). The researchers have open sourced some Python code this year! Gym is a toolkit
        for developing and comparing <a href="https://en.wikipedia.org/wiki/Reinforcement_learning">reinforcement learning</a> algorithms. It consists of an open-source library with a collection of test problems (environments) that can be used to test
        reinforcement learning algorithms, and a site and API that allows to compare the performance of trained algorithms (agents). Since it doesn’t care about the implementation of the agent, you can build them with the computation library of your choice:
        bare numpy, TensorFlow, Theano, etc.</p>
    <p>We also have the recently released <em>universe</em>, a software platform for researching into <strong>general intelligence</strong> across games, websites and other applications. This fits perfectly with <em>gym</em>, since it allows any real-world
        application to be turned into a <em>gym</em> environment. Researchers hope that this limitless possibility will <strong>accelerate research</strong> into smarter agents that can solve general purpose tasks.</p>
    <h2>7. <a href="http://bokeh.pydata.org/">Bokeh</a></h2>
    <p>You may be familiar with some of the libraries Python has to offer for data visualization; the most popular of which are <a href="http://matplotlib.org/">matplotlib</a> and <a href="http://seaborn.pydata.org/">seaborn</a>. Bokeh, however, is created
        for <strong>interactive visualization</strong>, and targets modern web browsers for the presentation. This means Bokeh can create a plot which lets you_explore_ the data from a web browser. The great thing is that it integrates tightly with
        <a
            href="https://jupyter.org/">Jupyter Notebooks</a>, so you can use it with your probably go-to tool for your research. There is also an optional server component, <code class="highlighter-rouge">bokeh-server</code>, with many powerful capabilities like server-side downsampling
            of large dataset (no more slow network tranfers/browser!), streaming data, transformations, etc.</p>
    <p>Make sure to check the <a href="http://bokeh.pydata.org/en/latest/docs/gallery.html">gallery</a> for examples of what you can create. They look awesome!</p>
    <h2>8. <a href="https://blaze.readthedocs.io/en/latest/index.html">Blaze</a></h2>
    <p>Sometimes, you want to run <strong>analytics</strong> over a dataset too big to fit your computer’s RAM. If you cannot rely on numpy or Pandas, you usually turn to other tools like PostgreSQL, MongoDB, Hadoop, Spark, or many others. Depending on the
        use case, one or more of these tools can make sense, each with their own strengths and weaknesses. The problem? There is a big overhead here because you need to learn how each of these systems work and how to insert data in the proper form.</p>
    <p>Blaze provides a <strong>uniform interface</strong> that abstracts you away from several database technologies. At the core, the library provides a way to <strong>express computations</strong>. Blaze itself doesn’t actually do any computation: it
        just knows how to instruct a specific <em>backend</em> who will be in charge of performing it. There is so much more to Blaze (thus the ecosystem), as libraries that have come out of its development. For example, <a href="http://dask.pydata.org/en/latest/">Dask</a>        implements a drop-in replacement for NumPy array that can handle content larger than memory and leverage multiple cores, and also comes with dynamic task scheduling. Interesting stuff.</p>
    <h2>9. <a href="https://github.com/crsmithdev/arrow">arrow</a></h2>
    <p>There is a famous saying that there are only two hard problems in Computer Science: cache invalidation and naming things. I think the saying is clearly missing one thing: <strong>managing datetimes</strong>. If you have ever tried to do that in Python,
        you will know that the standard library has a gazillion modules and types: <code class="highlighter-rouge">datetime</code>,<code class="highlighter-rouge">date</code>, <code class="highlighter-rouge">calendar</code>, <code class="highlighter-rouge">tzinfo</code>,
        <code class="highlighter-rouge">timedelta</code>, <code class="highlighter-rouge">relativedelta</code>, <code class="highlighter-rouge">pytz</code>, etc. Worse, it is timezone naive by default.</p>
    <p>Arrow is “datetime for humans”, offering a sensible approach to creating, manipulating, formatting and converting dates, times, and timestamps. It is a<strong>replacement</strong> for the <code class="highlighter-rouge">datetime</code> type that supports
        Python 2 or 3, and provides a much nicer interface as well as filling the gaps with new functionality (such as<code class="highlighter-rouge">humanize</code>). Even if you don’t really <em>need</em> arrow, using it can greatly reduce the boilerplate
        in your code.</p>
    <h2>10. <a href="http://www.hug.rest/">hug</a></h2>
    <p>Expose your internal API externally, drastically simplifying <strong>Python API</strong>development. Hug is a next-generation Python 3 (only) library that will provide you with the cleanest way to create HTTP REST APIs in Python. It is not a web framework
        per se (although that is a function it performs exceptionally well), but only focuses on exposing idiomatically correct and standard internal Python APIs externally. The idea is simple: you define logic and structure once, and you can expose your
        API through <strong>multiple means</strong>. Currently, it supports exposing REST API or command line interface.</p>
    <p>You can use type annotations that let <em>hug</em> not only generate <strong>documentation</strong> for your API but also provide with <strong>validation</strong> and clean error messages that will make your life (and your API user’s) a lot easier.
        Hug is built on <a href="https://github.com/falconry/falcon">Falcon’s</a> high performance HTTP library, which means you can deploy this to production using any wsgi-compatible server such as <a href="http://gunicorn.org/">gunicorn</a>.</p>
    <p>Follow the discussion of this post on: <a href="https://www.reddit.com/r/Python/comments/5jf64k/top_10_python_libraries_of_2016/">Reddit</a></p>
    <hr>
    <p><em>Original source:</em> <a href="https://tryolabs.com/blog/2016/12/20/top-10-python-libraries-of-2016/"><em>https://tryolabs.com/blog/2016/12/20/top-10-python…</em></a></p>
</div>