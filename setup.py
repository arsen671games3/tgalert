from setuptools import setup, find_packages

version = '1.0.2'

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='Telegram Alert',
    version=version,
    description='Library for sending error messages to Telegram',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/arsen671games3/tgalert',
    author='Arsen',
    author_email='arsen.dev@arsen.me',
    keywords='telegram alert library python',
    python_requires='~=3.7',
    packages=find_packages(include=('tgalert',)),
    zip_safe=False,
)
