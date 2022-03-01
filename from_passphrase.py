#!/bin/python3

import sys

from main import from_passphrase

passphrase = sys.stdin.readline()
hex_str = from_passphrase(passphrase)
print(hex_str, file=sys.stdout)
