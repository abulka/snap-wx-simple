import os
from setuptools import setup, find_packages

setup(
    name='snap-wx-simple',
    version='1.0.0',
    url='https://github.com/yourusername/myprogram',
    author='Andy Bulka',
    author_email='youremail@example.com',
    py_modules=['rubber_band_async'],
    # packages=find_packages(where='src'),
    # package_dir={'': 'src'},
    install_requires=[
        # Add your requirements here
    ],
    entry_points={
        'console_scripts': [
            'rubber=rubber_band_async:run'
        ],
    },    
)
