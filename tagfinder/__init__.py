"""
tagfinder looks for tags set by Mac's Finder.
The standard tags are colors but custom tags can be set.
Finder prefers to use extended attributes, if able, otherwise falls back to .DS_Store files.
Currently, only extended attributes are searched for tags as Mac with Linux+netatalk is capable of using xattr's.
I welcome using a DS_Store parser to find these tags if xattr's isn't used, but most of the documentation I find doesn't list tags
 so it would probably require investigation into where in the file the tags are stored.

TODO: Currently only tested on Linux, but could expand to include python on mac support.
TODO: DS_Store parsing.
TODO: settag()
"""

# Builtin libraries
import os
import plistlib
import sys

# Requires xattr: https://pyxattr.k1024.org/
#  apt install python3-pyxattr
import xattr


def findtag(p, tag='Red', maxdepth=None):
	"""
	Given the path @p, do a recursive directory crawl and find all directories and files with tag @tag set (default "Red").
	This returns os.DirEntry objects.

	If maxdepth is set, then no further recursion occurs after that depth (default is None meaning no limit).
	If you only want to check the directory itself, then pass maxdepth == 0.
	If you want to check the directory and only it's children, then pass maxdepth == 1.
	"""

	# Code is easier if it's a number, and a million depth search is insanely high (max path length is 4096 in linux)
	if maxdepth is None:
		maxdepth = 10000000

	# Coerce to string as tags are all strings (standard color tags are also assigned numbers so just in case one is passed)
	if not isinstance(tag, str):
		tag = str(tag)

	# Found files/directories that have the tag
	found = []

	# Check provided path itself for tags
	val = hastag(p, tag)
	if val is True:
		found.append(p)

	# Recursion
	if os.path.isdir(p):
		if maxdepth > 0:
			for f in os.scandir(p):
				if f == '.' or f == '..': continue

				found += findtag(os.path.join(p, f.name), tag, maxdepth-1)

	return found


def gettags(p):
	"""
	Get all tags for the path @p.
	Returned is a list of 2-tuples (eg, [('Red',6)]
	"""

	try:
		val = xattr.getxattr(p, "user.com.apple.metadata:_kMDItemUserTags")
		val = plistlib.loads(val)
	except OSError:
		# TODO: look into DS_Store

		return None

	return [tuple(_.split('\n')) for _ in val]

def hastag(p, tag):
	"""
	Check if path @p has a tag @tag: True if so, False if not.
	"""

	val = gettags(p)
	if val is None:
		return False

	for v in val:
		if tag in v:
			return True
	return False

def settag(p, tag, typ='xattr'):
	"""
	Set tag for path @p to @tag.
	Set tag type @typ ('xattr', 'dsstore')
	"""

	raise NotImplementedError

