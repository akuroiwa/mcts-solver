# -*- coding: utf-8 -*-

import glob
from setuptools import setup, find_packages

setup(
    name='mcts_solver',
    version='0.0.2',
    url='https://github.com/akuroiwa/mcts-solver',
    # # PyPI url
    # download_url='',
    license='GNU/GPLv3+',
    author='Akihiro Kuroiwa',
    author_email='akuroiwa@env-reform.com',
    description='Monte-Carlo tree search solver for chess-ant',
    # long_description="\n%s" % open('README.md').read(),
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    # python_requires=">=3.8",
    python_requires=">=3.7",
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        # 'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    keywords=['mcts', 'monte', 'carlo', 'tree', 'search', 'solver'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['mcts'],
)
