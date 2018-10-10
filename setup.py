# coding:utf8
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file

readme = os.path.join(here, 'Readme.md')
if os.path.exists(readme):
    with open(readme) as f:
        long_description = f.read()
else:
    long_description = ''
setup(
    name='pyfind',  # Required

    version='0.2.1',  # Required

    description='linux find command python lib',  # Required

    long_description=long_description,  # Optional

    long_description_content_type='text/markdown',  # Optional (see note above)

    url='http://github.com/ktlcove/pyfind.git',  # Optional

    author='ktlcove',  # Optional

    author_email='ktl_cove@126.com',  # Optional

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='find',  # Optional

    packages=find_packages(include=('pyfind',)),  # Required

    install_requires=[
        "six"
    ],  # Optional

    #   $ pip install sampleproject[dev]
    #
    extras_require={  # Optional
        'test': ['coverage'],
    },

    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # data_files=[('my_data', ['data/data_file'])],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'pyfind=pyfind.__main__:main',
        ],
    },

    # project_urls={  # Optional
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)
