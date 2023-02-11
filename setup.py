"""Package info."""

from setuptools import find_packages, setup

setup(
    name='open-parliament',
    version='0.0.0',
    description='A scraper for https://parlament.gv.at.',
    license='',
    # long_description=(''),
    # url='',
    author='',
    entry_points={
        'console_scripts': ['open-parliament=cli:cli'],
    },
    python_requires='~=3.5',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'bs4==0.0.1',
        'click',
        'urllib3==1.24.2',
        'requests==2.21.0',
        'scrapy==2.8.0',
    ],
)
