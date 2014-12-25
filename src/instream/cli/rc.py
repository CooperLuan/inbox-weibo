import os
import json


def get_weibo_token():
    with open(os.path.expanduser("~/.instreamrc"), "r") as store:
        token = json.load(store)
        return token['weibo']['token']


def set_weibo_token(**kwargs):
    with open(os.path.expanduser("~/.instreamrc"), "w") as store:
        token = json.dumps(kwargs)
        store.write(token)


if __name__ == '__main__':
    set_weibo_token(
        weibo={
            'token': {
                'uid': '1745066471',
                'access_token': '2.006VHGuBlAmfeD72c1484be2HHS4bB'
            }
        }
    )
