from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in neighborhood_pos/__init__.py
from neighborhood_pos import __version__ as version

setup(
	name="neighborhood_pos",
	version=version,
	description="Neighborhod Pos",
	author="Hussain",
	author_email="hussain@tabrah-holding.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
