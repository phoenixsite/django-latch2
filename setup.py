#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import setuptools

def long_description():
    try:
        return codecs.open('README.md', 'r', 'utf-8').read()
    except OSError:
        return 'Long description error: Missing README.md file'


setuptools.setup(
    name='django-latch',
    version='0.3',
    description='Django latch module.',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Javier Moral et al. (see README)',
    author_email='moraljlara@gmail.com',
    license='Apache License 2.0',
    url='https://github.com/javimoral/django-latch',
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    install_requires=[
        "Django>=2.0",
    ],
    data_files=[
        ('locales', ['latch/locale/es/LC_MESSAGES/django.mo', 'latch/locale/es/LC_MESSAGES/django.po']),
        ('templates', [
            'latch/templates/latch_pair.html',
            'latch/templates/latch_status.html',
            'latch/templates/latch_unpair.html',
        ])
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
