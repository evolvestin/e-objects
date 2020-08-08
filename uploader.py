import os
os.system('python setup.py sdist')
os.system(r'twine upload --repository-url https://upload.pypi.org/legacy/ dist/* '
          r'--username evolvestin --password YweyTu7hYrTvMDfj7AnX2fYLG6ZzGeRewyym8QaY')
