# instream[In-Development]

## 需求

- 像 inbox 一样对信息流进行处理
    + 分大类
        * 广告
        * 财经类
        * 好友互动
        * 互联网新闻
        * 技术界
        * 吃/游玩
    + 浏览布局
- 信息流
- 同一个 id 的信息按天合并
- 将所有信息归类
    + 重要信息
    + 广告信息
    + 按照信息内容进行再分类
    + 博客类
    + 图片类
    + 自动识别链接内容 判断链接类型
- 架构

## Install

```sh
virtualenv -p /usr/bin/python3 .
bin/python setup.py develop
```

## Cron Job

```sh
bin/python src/instream/app.py development.yml crawler
# or
# bin/instream-app development.yml crawler
```
