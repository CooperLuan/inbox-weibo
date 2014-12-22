from setuptools import setup


setup(name='inboxweibo',
      version='0.1',
      install_requires=[
          'pymongo',
          'nose',
          'numpy',
          'pandas'
      ],
      entry_points="""\
      [console_scripts]
      token = inboxweibo.token:get_token
      """)
