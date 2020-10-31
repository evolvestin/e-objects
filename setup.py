from setuptools import setup
setup(
    license='MIT',
    name='e-objects',
    keywords='objects',
    author='evolvestin',
    packages=['objects'],
    version=open(os.path.abspath('version')).read(),
    package_dir={'objects': 'objects'},
    author_email='evolvestin@gmail.com',
    package_data={'objects': ['LICENSE.rst']},
    long_description=open(os.path.abspath('README.rst')).read(),
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
