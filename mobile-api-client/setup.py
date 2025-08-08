"""Setup script for Mobile API Client"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="framna-mobile-api-client",
    version="1.0.0",
    author="Framna Feedback",
    description="Python client for Framna Feedback Mobile API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/framna/mobile-api-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "urllib3>=1.26.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "framna-mobile=mobile_form_cli:main",
        ],
    },
)