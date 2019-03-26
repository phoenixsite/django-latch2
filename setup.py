#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import setuptools

BASE_DIR = os.path.abspath(__file__)
with open(os.path.join(BASE_DIR, "README.md"), "r") as f:
    long_description = f.read()

setuptools.setup(
    name='django-latch',
    version='0.2',
    description='Django latch module.',
    long_description=long_description,
    author='Javier Moral (forked RootedCON, see README)',
    author_email='moraljlara@gmail.com',
    license='Apache License 2.0',
    url='https://github.com/moraljlara/django-latch',
    packages=setuptools.find_packages(),
    install_requires=[
        "Django>=2.0",
    ],
    data_files=[
        ('locales', ['latch/locale/es/LC_MESSAGES/django.mo', 'latch/locale/es/LC_MESSAGES/django.po']),
        ('templates', [
            'latch/templates/latch_message.html',
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
