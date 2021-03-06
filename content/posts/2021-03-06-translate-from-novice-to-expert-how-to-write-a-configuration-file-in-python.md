---
layout: post
title: [Translate]从新手到专家：如何用Python编写配置文件
tags: Translate,Python,Configuration
---

> 原作者：[Xiaoxu Gao](https://towardsdatascience.com/from-novice-to-expert-how-to-write-a-configuration-file-in-python-273e171a8eb3)

>将配置文件视为生产代码
>

设计软件时，我们通常要花费很多精力编写高质量代码。但这还不够，一个好的软件还应关注它的生态系统，例如测试，部署，网络等，这其中最重要的一方面就是配置管理。

好的配置管理应允许在任何环境下执行软件，并且无需更改代码。它可以帮助运维们管理所有麻烦的设置，并提供了有关过程中可能发生的情况的视图，甚至允许他们在运行时更改软件的行为。

最常见的配置文件有数据库的秘钥和外部服务的证书，及已部署服务器的主机名，动态参数等。

在本文中，我想与你们分享一些配置管理的最佳实践，以及如何在Python中实现它们。如果你有更多想法，请在下面留下你的评论。



## 什么时候需要一个单独的配置文件？

在编写任何配置文件前，我们应该问问自己为什么需要一个外部文件？难道不能把它们变成代码里的常数吗？实际上，著名的[《十二要素应用》](https://12factor.net)已经为我们回答了这个问题：

>一个验证应用程序的所有确配置是否均已正确地从代码中分解出来的试金石是：代码库是否随时可以在不损害任何证书的情况下开源。请注意，配置的定义**不**包括内部应用程序配置，例如Rails中的`config /routes.rb`或是[Spring](https://spring.io/)中[代码模块的连接方式](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans)。这种类型的配置在不同部署版本之间不会有所不同，因此最好直接写在代码里。

这篇文章建议将任何依赖于环境的参数（如数据库秘钥）存放于外部文件中。否则，就将它们作为代码中的普通常量。还有一种常见的用例是将动态变量存储在外部文件中，例如黑名单或白名单。配置也可以是一定范围内的数字（例如超时）或一些任意的文本。这些变量在每个环境中可能都相同，但是配置文件能使软件更加灵活，易于编辑。但是，如果配置文件的规模增长太快，可以会考虑将其移到数据库中。



## 应该使用哪种格式的配置文件？

事实上，只要代码可以读取和解析配置文件，就无需限制配置文件的格式。但是，有一些好的实践供参考。最常见的标准化格式是YAML，JSON，TOML和INI。一种好的配置文件应至少满足以下三个条件：

1. **易于阅读和编辑:** 应基于文本并以易于理解的方式进行结构化，让非开发人员也应该能够阅读。
2. **允许添加注释:** 配置文件不是仅被开发人员阅读的文件。在生产环境中，让非开发人员了解整个流程并修改软件行为也非常重要。添加注释就是一种快速解释事情的方法，它能使配置文件更具表现力。
3. **易于部署:** 所有操作系统和环境都应识别配置文件，还应该通过CDaaS（持续集成作为服务）管道将其轻松部署至服务器。

如果你仍然不知道哪种配置文件是更好的选择，但在Python的上下文中考虑的话，那么答案将是YAML或INI。 大多数Python程序和软件包都很好地接收YAML和INI。INI可能是最简单的解决方案，仅具有1级层次结构。但是，INI中没有数据类型的概念，所有数据都会被编码为字符串。

```ini
[APP]
ENVIRONMENT = test
DEBUG = True
# Only accept True or False

[DATABASE]
USERNAME = xiaoxu
PASSWORD = xiaoxu
HOST = 127.0.0.1
PORT = 5432
DB = xiaoxu_database
```

YAML中的相同配置如下所示。如你所见，YAML能很好地支持嵌套结构（例如JSON）。此外，YAML可以原生地编码一些数据类型，例如字符串，整型，双精度型，布尔型，列表，字典等。

```yaml
APP:
  ENVIRONMENT: test
  DEBUG: True
  # Only accept True or False

DATABASE:
  USERNAME: xiaoxu
  PASSWORD: xiaoxu
  HOST: 127.0.0.1
  PORT: 5432
  DB: xiaoxu_database
```

JSON与YAML非常相似，并且是一种流行的格式，然而我们无法在JSON中添加注释。我在程序内部大量使用JSON作为内部配置，但我想与其他人共享配置时则不使用JSON。

```json
{
    "APP": {
        "ENVIRONMENT": "test",
        "DEBUG": true
    },
    "DATABASE": {
        "USERNAME": "xiaoxu",
        "PASSWORD": "xiaoxu",
        "HOST": "127.0.0.1",
        "PORT": 5432,
        "DB": "xiaoxu_database"
    }
}
```

另一方面，TOML与INI类似，但支持更多数据类型，并为嵌套结构定义了语法。 在Python包管理系统（例如pip或poetry）中已经大量使用了它。但如果配置文件中的嵌套层级过多，则YAML会是更好的选择。以下文件看起来像INI，但每个字符串值都带有引号。

```toml
[APP]
ENVIRONMENT = "test"
DEBUG = true
# Only accept True or False

[DATABASE]
USERNAME = "xiaoxu"
PASSWORD = "xiaoxu"
HOST = "127.0.0.1"
PORT = 5432
DB = "xiaoxu_database"
```

至此为止，我已经解释了为什么使用配置文件和使用什么配置文件。在下一部分中，我将向你展示如何使用配置文件。



## 选项1：YAML / JSON --- 简单读取一个外部文件

像往常一样，我们从最基本的方式开始，简单地创建一个外部文件并读取它。Python有内置的模块来解析YAML和JSON文件。从下面的代码中可以发现，实际上它们返回相同的字典对象，因此两个文件的属性完全相同。

### 读取

由于[安全问题](https://security.openstack.org/guidelines/dg_avoid-dangerous-input-parsing-libraries.html)，建议使用`yaml.safe_load()`而不是`yaml.load()`以防止代码注入。

```python
import json
import yaml

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

assert read_json("data/sample.json") == read_yaml("data/sample.yaml")
```

### 校验

如果文件不存在，这两个包都将抛出`FileNotFoundError`。对于非YAML文件和无效的YAML文件，YAML会抛出不同的异常，JSON则只会抛出`JSONDecoderError`。

```python
import pytest

def test_validation_json():
    with pytest.raises(FileNotFoundError):
        read_json(file_path="source/data/non_existing_file.json")

    with pytest.raises(json.decoder.JSONDecodeError):
        # only show the first error
        read_json(file_path="source/data/sample_invalid.json")
        read_json(file_path="source/data/sample_invalid.yaml")

def test_validation_yaml():
    with pytest.raises(FileNotFoundError):
        read_yaml(file_path="source/data/non_existing_file.yaml")

    with pytest.raises(yaml.scanner.ScannerError):
        # only show the first error
        read_yaml(file_path="source/data/sample_invalid.yaml")

    with pytest.raises(yaml.parser.ParserError):
        # only show the first error
        read_yaml(file_path="source/data/sample_invalid.json")
```



## 选项2：Cofigureparser --- Python内置包

从此开始，我将介绍专为配置管理而设计的软件包。先从内置包开始：[`Configureparser`](https://docs.python.org/3/library/configparser.html)。

`Configureparser`主要用于读取和写入INI文件，但它也支持字典和可迭代文件对象作为输入。每个INI文件都由多个部分组成，每个部分有多个键值对。以下是如何访问其中字段的例子。

### 读取

```python
import configparser

def read_ini(file_path, config_json):
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            print((key, config[section][key]))
 
read_ini("source/data/sample.ini", config_json)
# ('environment', 'test')
# ('debug', 'True')
# ('username', 'xiaoxu')
# ('password', 'xiaoxu')
# ('host', '127.0.0.1')
# ('port', '5432')
# ('db', 'xiaoxu_database')
```

`Configureparser`不会猜测配置文件中的数据类型，因此每个项都会被储存为字符串。但是它提供了一些将字符串转换为正确数据类型的方法。最有趣的是布尔类型，它可以识别`'yes'`[/](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'no'`[, ](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'on'`[/](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'off'`[, ](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'true'`[/](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'false'`[ and ](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'1'`[/](https://docs.python.org/3/library/configparser.html#supported-datatypes)`'0'`。

就像我们前面所说的，它也可以使用`read_dict()`从字典中读取数据，或者使用`read_string()`从字符串中读取，亦或者使用`read_file()`从文件对象中读取。

```python
import configparser

def read_ini_extra(file_path, dict_obj=None):
    config = configparser.ConfigParser()
    if dict_obj:
        config.read_dict(dict_obj)
    else:
        config.read(file_path)
    debug = config["APP"].getboolean("DEBUG")
    print(type(debug))
    # <class 'bool'>
    name = config.get('APP', 'NAME', fallback='NAME is not defined')
    print(name)
    return debug

# read ini file
read_ini_extra(file_path="source/data/sample.ini")

# read dict obj
config_json = read_json(file_path="source/data/sample.json")
read_ini_extra(dict_obj=config_json)
```



### 校验

`Configureparser`的校验并不像YAML和JSON那样简单。首先，如果文件不存在，它不会抛出`FileNotFoundError`，而是在尝试访问键值时抛出`KeyError`。

此外，程序包“忽略”了缩进错误。像下面的示例一样，如果在“ DEBUG”之前有多余的Tab或空格，则“ ENVIRONMENT”和“ DEBUG”都将被赋成错误的值。
但是，`Configureparser`能够返回`ParserError`以获取多个错误（请参阅最后一个测试用例）。该设计有助于我们一口气解决所有问题。

```python
import pytest

def test_validation_configureparser():
    # doesn't raise FileNotFoundError, but raise KeyError
    # when it tries to access a Key
    with pytest.raises(KeyError):
        read_ini_extra(file_path="source/data/non_existing_file.ini")

    # [APP]
    # ENVIRONMENT = test
    #     DEBUG = True
    # doesn't raise exception for wrong indentation
    debug = read_ini_extra(
        file_path="source/data/sample_wrong_indentation.ini"
    )
    print(debug)
    # None
    # However, config["APP"]["ENVIRONMENT"] will return 'test\nDEBUG = True'

    # [APP]
    # ENVIRONMENT = test
    # DEBUG  True

    # [DATABASE]
    # USERNAME = xiaoxu
    # PASSWORD xiaoxu
    with pytest.raises(configparser.ParsingError):
        debug = read_ini_extra(
            file_path="source/data/sample_wrong_key_value.ini"
        )
    # show all the errors
    # configparser.ParsingError: Source contains parsing errors: 'source/data/sample_wrong_key_value.ini'
    #         [line  3]: 'DEBUG  True\n'
    #         [line  8]: 'PASSWORD xiaoxu\n'
```



## 选项3：python-dotenv  --- 将配置作为环境变量

现在，我们转到使用第三方库。到目前为止，我已经错过了一种类型的配置文件`.env`。 `.env`文件中的变量将由[python-dotenv](https://github.com/theskumar/python-dotenv)加载至环境变量，可以由`os.getenv`直接访问。

基本上一个`.env`文件看起来像这样。默认的寻找路径会是你项目的根文件夹。

```
ENVIRONMENT=test
DEBUG=true
USERNAME=xiaoxu
PASSWORD=xiaoxu
HOST=127.0.0.1
PORT=5432
```

### 读取

该库非常易于使用。你可以决定是否使用参数`override`覆盖环境中已有的变量。

```python
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('DEBUG'))
# true

load_dotenv(override=True)
# override existing variable in the environment
```

### 校验

`python-dotenv`并不会校验`.env`文件。如果给它这样的`.env`文件，并且想访问DEBUG，则得到None作为返回值而不会抛出异常。

```shell
# .env
ENVIRONMENT=test
DEBUG
# load.py
load_dotenv()
print('DEBUG' in os.environ.keys())
# False
```



## 选项4：Dynaconf --- Python的强大配置模块

[Dynaconf](https://dynaconf.readthedocs.io/en/docs_223/)是用于Python的非常强大的配置模块，支持多种文件格式：yaml，json，ini，toml和py。 它可以自动加载`.env`文件并支持自定义校验规则。简而言之，它涵盖了前三个选项的几乎所有功能，甚至远超这些。例如，你可以存储加密的密码，然后使用[自定义加载器](https://dynaconf.readthedocs.io/en/docs_223/guides/extend.html#creating-new-loaders)解密密码。它还与Flask，Django和Pytest完美集成。我不会在本文中提及它所有的功能，更多详细信息，请参阅其[文档](https://dynaconf.readthedocs.io/en/docs_223/)。

### 读取

![](https://miro.medium.com/max/500/1*fSaf_r2bQmDxIsxKB6IKDw.png)

`Dynaconf`使用`.env`文件查找所有设置文件，并使用其中字段填充`settings`对象。 如果两个设置文件具有相同的变量，则该值将被后面的设置文件覆盖。

### 校验

对我来说，其中一个有趣的功能是自定义[验证器](https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea)。之前提到过`Configureparser`对于INI文件的校验不够严格，但这点却可以在`dynaconf`中实现。在下面的示例中，我检查了文件中是否存在某些键以及这些键是否具有正确的值。 如果你从支持多种数据类型的YAML或TOML文件中读取数据，甚至可以检查某个数字是否在一定范围内。

```python
# settings.ini
# [default]
# ENVIRONMENT = test
# DEBUG = True
# USERNAME = xiaoxu
# PASSWORD = xiaoxu
# HOST = 127.0.0.1
# PORT = 5432
# DB = xiaoxu_database

# [production]
# DEBUG = False

from dynaconf import settings, Validator

settings.validators.register(
    Validator('ENVIRONMENT', 'DEBUG', 'USERNAME', must_exist=True),
    Validator('PASSWORD', must_exist=False),
    Validator('DEBUG', eq='False', env='production')
)

# Fire the validator
settings.validators.validate()

# dynaconf.validator.ValidationError: PASSWORD cannot exists in env test
```

### 与Pytest集成

另一个有趣的功能是与`pytest`的集成。单元测试的设置通常与其他环境不同。你可以使用`FORCE_ENV_FOR_DYNACONF`来让应用程序读取配置文件中完全不同的部分，也可以使用`monkeypatch`来替换设置文件中特定的键值对。

```python
import pytest
from dynaconf import settings

@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")

def test_dynaconf(monkeypatch):
    monkeypatch.setattr(settings, 'HOST', 'localhost')
```

### 运动时刷新配置

`Dynaconf`还支持`reload()`，它会清理并执行所有加载器。如果你希望应用程序在运行时重新加载设置文件，这将很有帮助。比如修改配置文件后，应用程序将自动重新加载设置。



## 选项5：Hydra --- 通过动态创建分层配置来简化开发

最后的选项不仅仅是一个文件加载器。[Hydra](https://hydra.cc/)是Facebook开发的框架，它用于优雅地配置复杂的应用程序。

除了读取，写入和校验配置文件外，`Hydra`还提供了一种简化多配置文件管理的策略，我们可以通过命令行界面覆盖配置文件，或是为每次运行创建快照等等。

### 读取

这里是`hydra`的基本用法。`+APP.NAME`意味着往配置中加入一个新的字段，你也可使用`APP.NAME=hydra1.1`去覆盖已经存在的字段。

```python
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()

# python3 source/hydra_basic.py +APP.NAME=hydra
# APP:
#   ENVIRONMENT: test
#   DEBUG: true
#   NAME: hydra
```

### 校验

`Hydra`可以与`@datackass`很好地集成来执行最基本的验证，例如类型检查和只读字段。但是它不支持`__post_init__`方法来进行更高级的值检查，正如我[上一篇文章](https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea)中所述。

```python
from dataclasses import dataclass
from omegaconf import MISSING, OmegaConf
import hydra
from hydra.core.config_store import ConfigStore

@dataclass
# @dataclass(frozen=True) means they are read-only fields
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING

@dataclass
class Config:
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)

@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

### 配置组

`Hydra`引入了另一个叫做[配置组](https://hydra.cc/docs/tutorials/basic/your_first_app/config_groups/)的概念。这个想法是将具有相同类型的配置分组，在执行过程中可以选择其中之一。 例如，你可以有一个“数据库”组，其中一个配置用于Postgres，另一个用于MySQL。

当整件事情变得更加复杂时，你的程序中可能会有这样的布局（`Hydra`文档中的示例）。

```
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   ├── schema
│       ├── school.yaml
│       ├── support.yaml
│       └── warehouse.yaml     
└── my_app.py
```

当你想使用`db`,`schema`和`ui`的不同组合对应用程序进行基准测试时，则可以运行：

```
python my_app.py db=postgresql schema=school.yaml
```

### 更多...

`Hydra`通过`--multirun`选项支持[参数扫描](https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run)，使用不同的配置文件在同一时间运行多个作业。对于前面的示例，我们可以运行以下命令：

```
python my_app.py schema=warehouse,support,school db=mysql,postgresql -m
```

之后会同时启动六个任务

```
[2019-10-01 14:44:16,254] - Launching 6 jobs locally
[2019-10-01 14:44:16,254] - Sweep output dir : multirun/2019-10-01/14-44-16
[2019-10-01 14:44:16,254] -     #0 : schema=warehouse db=mysql
[2019-10-01 14:44:16,321] -     #1 : schema=warehouse db=postgresql
[2019-10-01 14:44:16,390] -     #2 : schema=support db=mysql
[2019-10-01 14:44:16,458] -     #3 : schema=support db=postgresql
[2019-10-01 14:44:16,527] -     #4 : schema=school db=mysql
[2019-10-01 14:44:16,602] -     #5 : schema=school db=postgresql
```



## 结论

在本文中，我从WHY，WHAT和HOW的角度讨论了Python中的配置管理。根据不同的用例，复杂的工具/框架并不总是比简单的软件包更好。但无论选择哪一种，都应始终考虑可读性，可维护性以及如何尽早地发现错误。事实上，可以说配置文件只是另一种类型的代码。

希望你能喜欢这篇文章，随时欢迎你留下评论。



