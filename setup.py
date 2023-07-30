from pathlib import Path
from setuptools import setup, find_packages

parent_dir = Path(__file__).resolve().parent

setup(
    name="prettymapp",
    version="0.1.0",
    author="Christoph Rieke",
    author_email="christoph.k.rieke@gmail.com",
    description="",
    long_description=parent_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/chrieke/prettymapp",
    license="MIT",
    packages=find_packages(
        exclude=("prettymapp/tests", "streamlit-prettymapp", "cache")
    ),
    package_data={"": ["fonts/PermanentMarker-Regular.ttf"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pandas==1.5.2",  # osmnx subdependecies are partially unpinned
        "numpy==1.23.5",
        "matplotlib==3.6.2",
        "osmnx==1.2.3",
    ],
    extras_require={
        "test": [
            "pre-commit",
            "mock",
            "types-mock",
            "pytest",
            "pytest-sugar",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.10",
)
