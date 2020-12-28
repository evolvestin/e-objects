import os
import io
import re
from setuptools import setup
requirements = [
    'heroku3==4.2.3',
    'aiogram==2.11.2',
    'requests>=2.25.1',
    'Unidecode==1.1.1',
    'beautifulsoup4==4.9.3',
    'pyTelegramBotApi==3.7.4',
]


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    with io.open(filename, encoding='utf-8', mode='rt') as file:
        return file.read()


setup(
    license='MIT',
    name='e-objects',
    keywords='objects',
    author='evolvestin',
    packages=['objects'],
    python_requires='>=3.7',
    install_requires=requirements,
    package_dir={'objects': 'objects'},
    author_email='evolvestin@gmail.com',
    long_description=read('README.rst'),
    version=re.sub('\n', '', read('version')),
    url='https://github.com/evolvestin/e-objects/',
    description='Some useful objects for telegram bots.',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable'
    ]
)
