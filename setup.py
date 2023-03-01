import os
from setuptools import setup, find_packages

setup(
    name='snap-wx-simple',
    version='1.0.0',
    url='https://github.com/yourusername/myprogram',
    author='Andy Bulka',
    author_email='youremail@example.com',

    py_modules=['rubber_band_async'],
    # py_modules=['src.rubber_band_async'],

    # You need both entries because packages tells setuptools to include all
    # packages found under the src directory, while package_dir tells it to use
    # src as the root directory for the package hierarchy. Without package_dir,
    # setuptools would look for packages relative to the root directory of the
    # project, which would result in the packages not being found. Similarly,
    # without packages, setuptools would not include any packages in the
    # distribution, even though they would be found under src.    
    # 
    # packages=['common'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[
        # Add your requirements here
    ],
    entry_points={
        'console_scripts': [
            'rubber=rubber_band_async:run'
        ],
    },    
)
