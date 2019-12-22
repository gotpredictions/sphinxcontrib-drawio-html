import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinxcontrib-drawio-html",
    version="0.1",
    author="Eswar Vandanapu",
    author_email="eswar.vandanapu@gmail.com",
    description="Sphinx Extension to include draw.io files using HTML5 embedding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gotpredictions/sphinxcontrib-drawio-html",
    packages=['sphinxcontrib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Sphinx :: Extension",
    ],
    python_requires='>=3.7',
)
