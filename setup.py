from setuptools import setup

setup(
    name='snap-wx-simple',
    version='1.0.0',
    url='https://github.com/yourusername/myprogram',
    author='Andy Bulka',
    author_email='youremail@example.com',
    py_modules=['myprogram'],
    entry_points={
        'console_scripts': [
            'myprogram=myprogram:main',
        ],
    },
)
