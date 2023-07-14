from distutils.core import setup

setup(name='agetsmscode',
    version='1.1',
    description='Async API wrapper for getsmscode',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['getsmscode','sms','async'],
    url='https://github.com/optinsoft/agetsmscode',
    packages=['agetsmscode']
)