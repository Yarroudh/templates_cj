from setuptools import setup, find_packages

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setup(
    name="templates_cj",
    version='0.1.0',
    description="CLI application to create CityJSON files from templates",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author = 'Anass Yarroudh',
    author_email = 'ayarroudh@uliege.be',
    url = 'https://github.com/Yarroudh/templates_cj',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "templates_cj=src.main:main"
        ]
    }
)
