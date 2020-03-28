import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('posterior_agreement/VERSION.txt', 'r') as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="posterior_agreement",
    version=version,
    author="Sebastian Bocquet",
    author_email="sebastian.bocquet@gmail.com",
    description="Compute posterior agreement between two probability distributions",
    long_description=long_description,
    long_description_content_type="text/md",
    url="https://github.com/SebastianBocquet/PosteriorAgreement",
    packages=['posterior_agreement'],
    package_data={'posterior_agreement': ["VERSION.txt"],},
    install_requires = ['numpy', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
