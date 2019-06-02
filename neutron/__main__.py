from neutron.neutron_main import main
import argparse

parser = argparse.ArgumentParser(description="A programming langue written in Python 3.")
parser.add_argument("filename", type=str)
parser.add_argument("-v", "--verbose")
args = parser.parse_args()

main(args.filename, verbose=arg.verbose is not None)
