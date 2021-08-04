from setuptools import find_packages
from distutils.core import setup

setup(
    name='pygrn',
    version='0.1',
    packages=find_packages(),
    install_requires=["keras==2.2.4", 'numpy', 'PyYAML', 'tensorflow', 'tqdm'],
    license='',
    long_description=open('README.md').read(),
)
