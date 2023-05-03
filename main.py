import json
import sys
import argparse
from scripts import *
from sid_framework.utils.geographic.address_geocoding import dane_geocoding

parser = argparse.ArgumentParser()
parser.add_argument("--job", help = "Specific job to be executed")
parser.add_argument("--arguments", help = "Arguments file to execute")

args = parser.parse_args()

print(args.arguments)
input = json.loads(args.arguments)

if __name__ == '__main__':
    if args.job == "geocoding":
        print(dane_geocoding(**input))