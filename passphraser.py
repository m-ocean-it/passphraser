#!/bin/python3

import argparse
import sys

from lib import to_passphrase, from_passphrase


def main():
    parser = argparse.ArgumentParser(description='description...')
    parser.add_argument('input', nargs='?', default=None)
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-m', '--mode', default='hex',
                        help='specify how to parse input')
    parser.add_argument('-w', '--wordlist', default='bip39')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    stdin_present = stdin_is_present()
    if args.input:
        input_str = args.input
        if stdin_present:
            print('[Warning] Ignoring stdin since argument was provided.')
    else:
        if not stdin_present:
            print('Enter the value:')
        input_str = sys.stdin.readline().strip()
        if not input_str:
            print('[Error] No input provided.')
            sys.exit(1)

    if args.decrypt:
        result = from_passphrase(input_str,
                                 mode=args.mode,
                                 wordlist_option=args.wordlist,
                                 verbose=args.verbose)
    else:
        result = to_passphrase(input_str,
                               mode=args.mode,
                               wordlist_option=args.wordlist,
                               verbose=args.verbose)

    print(f'[Result] {result}', file=sys.stdout)


def stdin_is_present():
    if not sys.stdin.isatty():
        return True
    return False


if __name__ == '__main__':
    main()
