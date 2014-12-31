# Instream

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

## Workflow

### Scheduler

create `schedule` document in `schedules`, call `Route` to add crawler job

### Crawler

- process `schedule`, create `seeds`
- process `seed`, yield `ETL` job by `Route`

### ETL
### NLP
### ML
### FGD
### FE

## Jobs DataStructure

### Schedule

> input

```javascript
{
    "route": "",
    "title": "",
    "args": [],
    "kwargs": {},
}
```

> output

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

> input

document `_id` of schedule

> ouput

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

> input

document `_id` of webpage

> ouput

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
// streams
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

## Celery

### Queues

- scheduler
- crawler
- extractor
- transformer
- loader
- nlp
- ml
- fdg
