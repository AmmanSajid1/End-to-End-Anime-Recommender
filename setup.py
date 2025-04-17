from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Anime-Recommender",
    version='0.0.1',
    author='Amman Sajid',
    author_email="ammansajid1@gmail.com",
    packages=find_packages(),
    install_requires=requirements
)
