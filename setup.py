from setuptools import setup, find_packages

setup(
    name = "paraphraser",
    version="0.1.1",
    author="Munj B Patel",
    author_email="patelmunj2011@gmail.com",
    description="A simple package which can be used for paraphrasing a given text in multiple languages.",
    packages=find_packages(),
    install_requires=[
    "fake_useragent",
    "my_fake_useragent",
    "requests"
    ],
    classifiers=[
        "Programming Language::Python"
        ],
    entry_points = {
        'pytest11':[
            'tox_tested_package = tox_tested_package.fixtures'
        ]
    }
)