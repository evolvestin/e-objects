import os
import base64
import heroku3
from time import sleep
from version import version
from ast import literal_eval
command = 'twine upload --repository-url %(url)s --username %(username)s --password %(password)s'
data = 'eyd1c2VybmFtZSc6ICdldm9sdmVzdGluJywgJ3VybCc6ICdodHRwczovL3VwbG9hZC5weXBpLm9yZy9sZWdhY3kv' \
       'IGRpc3QvKicsICdwYXNzd29yZCc6ICdZd2V5VHU3aFlyVHZNRGZqN0FuWDJmWUxHNlp6R2VSZXd5eW04UWFZJ30='
data = literal_eval(base64.b64decode(data).decode('utf-8'))

while True:
    sleep(10)
    print(version, '-', os.environ.get('version'))
    if os.environ.get('version') != version:
        os.system('python setup.py sdist')
        os.system(command % data)
        if os.environ.get('api'):
            connection = heroku3.from_key(os.environ.get('api'))
            for app in connection.apps():
                config = app.config()
                config['version'] = version
