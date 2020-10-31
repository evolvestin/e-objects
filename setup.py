import os
import io
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    license='MIT',
    name='e-objects',
    keywords='objects',
    author='evolvestin',
    version=read('version'),
    packages=find_packages('objects'),
    author_email='evolvestin@gmail.com',
    long_description=read('README.rst'),
    url='https://github.com/steve10live/e-objects/',
    description='Some useful objects for telegram bots.',
    install_requires=['heroku3', 'aiogram', 'pyTelegramBotApi', 'requests', 'bs4', 'Unidecode'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
