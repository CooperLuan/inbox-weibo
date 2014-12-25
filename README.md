# instream

## Stack

- buildout
- django
- AngularJS
- Restful API
- celery / flower
- pandas
- gevent/asyncio
- machine learning
    + clustering
- ansible

## thoughts

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

## Architecture

- Jobs & Celery
    + Crawler
    + ETL
    + NLP
    + ML
    + FGD
- FE
    + AngularJS
    + Less
- Deploy
    + ansible | fabric
- API
- Schedule

## Jobs DataStructure

### Schedule

```javascript
// schedules
var doc_schedule = {
    "_id": ObjectId(),
    "title": "weibo crawler 20141225",      // crawler/ETL/NLP/ML/ML
    "route": "crawler.weibo.statuses",
    "created": 1419328052.869,
    "incremental": true,
    "kwargs": {
        "since_id": 0,
        "token": "SKJGPA9801JKLABG-ADHGHBB",
    }
}
// seeds
var doc_seed = {
    "_id": ObjectId(),
    "_scheduleId": ObjectId(),
    "_status": "done",                  // started/done
    "_seedId": null,
    "_ancestors": [],
    "route": "crawler.weibo.statuses",
    "incremental": true,
    "created": 1419328052.869,
    "updated": null,
    "kwargs": {
        "since_id": 0,
        "token": "SKJGPA9801JKLABG-ADHGHBB",
        "page": 1,
        "count": 100,
    }
}
```

### Crawler

```javascript
// webpages
var doc_webpage = {
    "_id": ObjectId(),
    "scheduled": {
        "_scheduleId": ObjectId(),
        "time": 1419328052.869,
        "data": {
            "title": "",
            "route": "crawler.weibo.statuses",
        }
    },
    "collected": {
        "_seedId": ObjectId(),
        "time": 1419328052.869,
        "errs": [null],
        "data": {
            "route": "crawler.weibo.statuses",
            "body": {}
        }
    },
}
```

### ETL

```javascript
// etl
var doc_etl = {
    "_id": ObjectId(),
    "_webpageId": ObjectId(),
    "collected": {
        "_seedId": ObjectId(),
        "time": 1419328052.869,
        "data": {
            "route": "crawled.weibo.statuses",
        }
    },
    "crawled": {
        "ok": true,
        "errs": [],
        "data": {
            "route": "crawled.weibo.statuses",
        }
    },
    "extracted": {
        "ok": true,
        "data": {},
        "errs": []
    },
    "transformed": {
        "ok": true,
        "data": {},
        "errs": []
    },
    "loaded": {
        "ok": true,
        "data": {},
        "errs": []
    }
}
// stream
var doc_stream = {
    "_id": ObjectId(),
    "source": "weibo",
    "id": "3791639811870824",
    "text": "",
    "tags": "",
    "link": "",
    "created": "",
    "_profileId": ObjectId()
}
// profiles
var doc_profile = {
    "_id": ObjectId(),
    "id": 2853016445,
    "name": "",
    "link": "",
    "avatar": "",
}
```

### NLP

```javascript
var doc_stream = {
    "_id": ObjectId(),
    "nlp": {
        "keywords": ['Python', 'DevelopWorks'],
    }
}
```

### ML

```javascript
var doc_stream = {
    "_id": ObjectId(),
    "ml": {
        "tags": {'Financal': 3, 'Shopping': 1},
        "category": "Forum",
    }
}
```

### FGD

TODO

### FE

### API
