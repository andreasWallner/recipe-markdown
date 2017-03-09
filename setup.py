from setuptools import setup, find_packages
import pkg_resources
setup(
    name='recipemd',

    version='0.1',

    description='Recipe Markdown',

    author='Andreas Wallner',
    author_email='A.Wallner@innovative-solutions.at',

    license='MIT',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['jinja2', 'lxml'],

    entry_points={
        'console_scripts': [
            'recipemd = recipemd.main:main'
        ],
    },
)
