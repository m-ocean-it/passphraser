#!/bin/python3

import sys

from main import to_passphrase

hex_str = sys.stdin.readline()
passphrase = to_passphrase(hex_str)
print(passphrase, file=sys.stdout)
