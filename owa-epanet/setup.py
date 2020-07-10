from skbuild import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "owa-epanet",
    version = "2.2.2",
    author = "Sam Hatchett",
    author_email = "samhatchett@gmail.com",
    description = "a thin wrapper for epanet hydraulic toolkit",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/OpenWaterAnalytics/epanet-python",
    cmake_args=["-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9"],
    #cmake_with_sdist = True,
    package_dir = {"":"packages"},
    packages = ["epanet"],
    package_data = {"epanet":["*.dylib", "*.dll", "*.so"]},
    zip_safe=False
)
