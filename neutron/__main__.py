try:
    from neutron.neutron_main import main
except ModuleNotFoundError:
    from neutron_main import main

import argparse

parser = argparse.ArgumentParser(description="A programming langue written in Python 3.")
parser.add_argument("filename", type=str)
parser.add_argument("-v", "--verbose", action='store_true')
args = parser.parse_args()

main(args.filename, verbose=args.verbose)
