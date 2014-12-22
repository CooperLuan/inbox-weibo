import pymongo

import env


def setup_db():
    global env
    env.MONGO = pymongo.MongoClient()


def main():
    setup_db()


if __name__ == '__main__':
    main()
