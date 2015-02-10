import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


setup(
    name='dripper',
    version='0.3.1',
    license='MIT',
    packages=['dripper'],
    install_requires=[],
    description='Cleaning your messy data.',
    long_description=README + '\n\n' + CHANGES,
    author='Hiroki KIYOHARA',
    author_email='hirokiky@gmail.com',
    url='https://github.com/hirokiky/dripper',
    keywords='dict data converter cleaning mapping',
    include_package_data=True,
    zip_safe=False,
)
