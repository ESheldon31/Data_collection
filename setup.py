from setuptools import setup, find_packages

setup(name='Web scraper',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'selenium', 
        'dataclasses',  
        'uuid',  
        'requests'
    ])
