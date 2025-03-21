from setuptools import setup, find_packages

setup(
    name="cao",
    version="0.1",
    packages=find_packages(),
    install_requires=["click", "Pillow", "geopandas", "pyarrow"],
    entry_points={
        "console_scripts": [
            "cao = cao.cli:cli",
        ],
    },
)
