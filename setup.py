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
    ],
    entry_points="""\
    [console_scripts]
    token = instream.token:get_token
    """)
