import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='mailerlite-python',
      version='0.1.0',
      description='API wrapper for MailerLite written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/mailerlite-python',
      author='Juan Carlos Rios',
      author_email='juankrios15@gmail.com',
      license='GPL',
      packages=['mailerlite'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
