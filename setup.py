from setuptools import setup
from version import version, requirements
setup(
    license='MIT',
    version=version,
    name='e-objects',
    keywords='objects',
    author='evolvestin',
    packages=['objects'],
    install_requires=requirements,
    package_dir={'objects': 'objects'},
    author_email='evolvestin@gmail.com',
    package_data={'objects': ['LICENSE.rst']},
    long_description=open('README.rst').read(),
    url='https://github.com/steve10live/e-objects/',
    description='Some useful objects for telegram bots.',
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
