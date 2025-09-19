from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="datalens-weaviate-db",
    version="0.1",
    author="Son Ba",
    author_email="bagiangson2001@gmail.com",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
)
