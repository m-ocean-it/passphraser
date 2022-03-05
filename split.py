'''
Script to split a secret using Shamir Secret Sharing Scheme and encode
the shares as passphrases. And restore the secret back from those
passphrases.

Requires the ssss utility installed on the system.
'''

import subprocess
import sys
from termcolor import colored

from passphraser import to_passphrase, from_passphrase


def main():
    direction = input(colored('split(s) / combine(c): ', 'blue'))
    if direction in ('s', 'split'):
        string_to_split = input(colored('Enter data:\n', 'blue'))
        split(string_to_split)
    elif direction in ('c', 'combine'):
        combine()
    else:
        print(colored('[Error]', 'red'))
        sys.exit(1)


def split(string_to_split):

    output = subprocess.check_output(
        f'echo "{string_to_split}" | ssss-split -t 3 -n 5',
        shell=True).decode()
    lines = output.split('\n')
    hex_shares = lines[1:-1]

    print()
    for hex_share in hex_shares:
        print(hex_share)
        passphrase = to_passphrase(hex_share,
                                   mode='ascii',
                                   wordlist_option='bip39')
        print(passphrase)
        print()


def combine():
    phrases = []
    while True:
        phrase = input(
            colored('Enter phrase (leave blank to continue): ', 'blue'))
        if phrase.strip() == '':
            break
        phrases.append(phrase)
    print()
    number_of_shares = int(input(colored('Number of total shares: ', 'blue')))
    print(
        colored(f'Threshold is assumed from number of entered phrases: {len(phrases)}',
                'blue'))
    print()

    hex_shares = []
    for phrase in phrases:
        hex_share = from_passphrase(phrase.strip(),
                                    mode='ascii',
                                    wordlist_option='bip39')
        hex_shares.append(hex_share)
        print(hex_share)
    print()

    subprocess.run(f'ssss-combine -t {len(phrases)} -n {number_of_shares}',
                   shell=True,
                   check=True)


if __name__ == '__main__':
    main()
