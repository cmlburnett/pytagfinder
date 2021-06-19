
import argparse
import json
import sys

import tagfinder

def main():
	ap = argparse.ArgumentParser(description="Find Mac's Finder tags on files in Linux")
	ap.add_argument('-f', dest='find', default=False, action='store_true', help="Use when invoked from find(1) command. Only a single path is accepted and program return value of zero if path has the tag. This is slow because find invokes python interpreter for every path tested.")
	ap.add_argument('-t', dest='tag', metavar='TAG', default="Red", help="Tag to find, default is Red")
	ap.add_argument('-d', dest='depth', metavar='MAXDEPTH', default=None, help="Specify maximum recursion depth (default is unlimited)")
	ap.add_argument('-j', dest='json', action='store_true', default=False, help="Print list as JSON instead")
	ap.add_argument('PATHS', nargs="*", help="Paths to check for tags. If none passed, then STDIN is assumed (either pipe them in or type them in and ctrl-D when done). Can also pass in - as the single argument to read from STDIN. Otherwise, arguments are assumed to be paths in the current working directory.")

	args = ap.parse_args()


	# Coerce to integer if it's a string (meaning something was passed)
	if isinstance(args.depth, str):
		args.depth = int(args.depth)

		# If negative supplied, take this as unlimited so pass None
		if args.depth < 0:
			args.depth = None

	if args.find:
		ret = tagfinder.hastag(args.PATHS[0], args.tag)
		if ret:
			sys.exit(0)
		else:
			sys.exit(-1)

	# Accumulate found objects
	found = []

	# STDIN
	if len(args.PATHS) == 0 or (len(args.PATHS) == 1 and args.PATHS[0] == '-'):
		paths = sys.stdin.readlines()
		paths = [_.strip() for _ in paths]
		for a in paths:
			found += tagfinder.findtag(a, args.tag, maxdepth=args.depth)

	#
	else:
		for a in args.PATHS:
			found += tagfinder.findtag(a, args.tag, maxdepth=args.depth)


	# Output
	if args.json:
		print(json.dumps(found))
	else:
		print("\n".join(found))

if __name__ == '__main__':
	main()
