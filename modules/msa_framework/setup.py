from setuptools import setup, find_packages


setup(
    name='MSA-Framework',
    version='0.0.1',
    packages=find_packages(),
    author='Haoyu Tan',
    author_email='haoyutan@gmail.com',
    license='MIT',
    description='Micro Service Architecture Framework',
    url='http://www.deepera.com/',
    long_description=open('README').read(),
    platforms=['Any',],

    install_requires=('django', 'djangorestframework',),
)
