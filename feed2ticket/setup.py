from setuptools import setup, find_packages

setup(
    name='feed2ticket',
    version='1.0',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'feed2ticket=main:main',
        ],
    },
)