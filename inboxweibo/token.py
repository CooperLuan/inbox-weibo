import os
import json


def get_token():
    with open(os.path.expanduser("~/.inbox-weiborc"), "r") as store:
        token = json.load(store)
        return token['token']


def set_token(**kwargs):
    with open(os.path.expanduser("~/.inbox-weiborc"), "w") as store:
        token = json.dumps(kwargs)
        store.write(token)


if __name__ == '__main__':
    set_token(
        token={
            'uid': '1745066471',
            'access_token': '2.006VHGuBlAmfeD72c1484be2HHS4bB'
        }
    )
