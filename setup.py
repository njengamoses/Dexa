from setuptools import setup, find_packages

setup(
    name="dexa",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dexa=dexa.cli:main"
        ]
    }
)
