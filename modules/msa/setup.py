from setuptools import setup, find_packages


setup(
    name='MSA-Framework',
    version='0.2',
    packages=find_packages(),
    author='Haoyu Tan',
    author_email='hytan@deepera.com',
    license='MIT',
    description='Micro Service Architecture Framework',
    url='http://www.deepera.com/',
    long_description=open('README.md').read(),
    platforms=['Any',],

    install_requires=('django', 'djangorestframework',),
)
