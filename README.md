# 网络服务异常检测系统
```angular2html
基于Django Restframework和Spark的异常检测系统，数据库为MySQL、Redis,
消息队列为Celery，分析服务为Spark SQL和Spark Mllib;
每天0点1分自动运行定时job从全量数据中导入正常的cat数据，该数据用于kmeans做模型训练
```


# Fork项目
把项目fork到用户目录。

# 安装运行环境
```
$ sudo apt-get install redis-server
$ sudo apt-get install python3 python3-pip
$ sudo pip3 install virtualenv
$ sudo apt-get install python3-dev libmysqlclient-dev

$ git clone git_url
$ virtualenv -p python3 env_py3_spark

# 激活环境后安装依赖库
$ pip install -r requirements.txt
$ pre-commit install
```

# 本地配置文件 settings_local
进入web目录，创建新的配置文件settings_local.py。然后根据自己的环境进行配置。
例如：
```text
"""
本地开发的配置文件
"""
from web.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "USER": "root",
        "NAME": "test_cpass",
        "PASSWORD": "password",
        "PORT": "",
    },
}
```

# Celery任务启动
```
$ celery -A web worker -l info  启动celery
$ celery flower -A web --address=0.0.0.0 --port=6666  启动celery flower
```