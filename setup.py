
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddh2ext",
    version="0.1a",
    author="Rochelle O'Hagan",
    # author_email="author@example.com",
    description="DDH2ext provides a python interface to the World Bank's DDH2 platform intended for external use by the public.",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spatialexplore/ddh2ext",
    packages=setuptools.find_packages(),
    # include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    install_requires=['requests'],
    python_requires='>=3.0',
)
