from distutils.core import setup

majv = 1
minv = 0

setup(
	name = 'tagfinder',
	version = "%d.%d" %(majv,minv),
	description = "Looks for tags set by Mac's Finder",
	author = "Colin ML Burnett",
	author_email = "cmlburnett@gmail.com",
	url = "",
	packages = ['tagfinder'],
	package_data = {'tagfinder': ['tagfinder/__init__.py', 'tagfinder/__main__.py']},
	classifiers = [
		'Programming Language :: Python :: 3.9'
	]
)
