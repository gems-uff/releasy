import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='releasy-uff',
    version='1.0.1',
    author="Felipe Curty",
    author_email="felipecrp@gmail.com",
    description="Releasy is a tool that collects provenance data from releases by parsing the software version control and issue tracking systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gems-uff/releasy",
    packages=setuptools.find_packages(),
    install_requires=[
        'python-dateutil',
        'requests'
    ]
)