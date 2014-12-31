from setuptools import setup
from setuptools import find_packages


setup(
    name='instream',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pymongo',
        'nose',
        'pyyaml',
        'numpy',
        'pandas',
        'django',
        'celery',
        'rq',
        'python-dateutil',
        'jieba3k',
    ],
    entry_points="""\
    [console_scripts]
    instream-run = instream.run:main
    instream-app = instream.app:main
    token = instream.cli.rc:get_weibo_token
    """)
