from setuptools import setup, find_packages

version = '1.0.0'


setup(
    name='Telegram Alert',
    version=version,
    description='',
    long_description_content_type='text/md',
    url='https://github.com/arsen671games3/tgalert',
    author='Arsen',
    author_email='arsen.dev@arsen.me',
    keywords='telegram alert library python',
    python_requires='~=3.7',
    packages=find_packages(include=('tgalert',)),
    zip_safe=False,
)
