from distutils.core import setup
import re

s = open('agetsmscode/version.py').read()
v = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", s, re.M).group(1)

setup(name='agetsmscode',
    version=v,
    description='Async API wrapper for getsmscode',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['getsmscode','sms','async'],
    url='https://github.com/optinsoft/agetsmscode',
    packages=['agetsmscode']
)