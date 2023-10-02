from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="neura-launch-cli",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        requirements
    ],
    entry_points={
        "console_scripts": [
            "neura-launch = app.cli:main",
        ],
    },
    author="Lainforge",
    author_email="tomartarun@2001@gmail.com",
    description="CLI tool for neura launch.",
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
