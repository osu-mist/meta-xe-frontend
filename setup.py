from setuptools import setup

setup(
    name='meta-xe-frontend',
    version='0.1',
    author='Andrew Ekstedt',
    author_email='ekstedta@oregonstate.edu',
    packages = [
        'metaxe',
    ],
    install_requires = [
        'Flask>=0.11.1',
        'Flask-SeaSurf>=0.2.2',
        'requests>=2.11',
        'urllib3[secure]>=1.16',
    ],
)
