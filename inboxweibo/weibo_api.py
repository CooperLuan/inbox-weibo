# -*- coding: utf-8 -*-
# coding: utf-8
import logging
import json
import requests


class WeiboAPIError(BaseException):

    def __init__(self, url, params, resp):
        self._url = url
        self._params = params
        self._resp = resp

    def __str__(self):
        return 'api error when get %s with %s\n%s' % (
            self._url, self._params,
            json.dumps(self._resp, indent=4))


class WeiboAPI(object):

    def __init__(self, uid=None, access_token=None):
        self._uid = uid
        self._access_token = access_token

    @property
    def access_token(self):
        assert self._access_token
        return self._access_token

    @property
    def uid(self):
        assert self._uid
        return self._uid

    def api_get(self, url, params, required_filed=None):
        logging.info('weibo api get %s %s', url, params)
        params.update({'access_token': self.access_token})
        resp = requests.get(url, params=params).json()
        if required_filed and resp.get(required_filed, None) is None:
            raise WeiboAPIError(url, params, resp)
        return resp

    def users_show(self, uid=None, screen_name=None):
        url = 'https://api.weibo.com/2/users/show.json'
        params = {
            'uid': uid or screen_name or self.uid
        }
        return self.api_get(url, params)

    def statuses_friends_timeline(self, since_id=0, max_id=0, count=20, page=1, trim_user=0):
        url = 'https://api.weibo.com/2/statuses/friends_timeline.json'
        params = {
            'since_id': since_id,
            'max_id': max_id,
            'count': count,
            'page': page,
            'trim_user': trim_user
        }
        return self.api_get(url, params, required_filed='statuses')
