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
        number_of_shares = int(input(colored('Number of shares: ', 'blue')))
        threshold = int(input(colored('Threshold: ', 'blue')))
        string_to_split = input(colored('Enter data:\n', 'blue'))
        split(string_to_split,
              number_of_shares=number_of_shares,
              threshold=threshold)
    elif direction in ('c', 'combine'):
        combine()
    else:
        print(colored('[Error]', 'red'))
        sys.exit(1)


def split(string_to_split,
          number_of_shares,
          threshold):

    output = subprocess.check_output(
        f'echo "{string_to_split}" | ssss-split -t {threshold} -n {number_of_shares}',
        shell=True).decode()
    lines = output.split('\n')
    hex_shares = lines[1:-1]

    print()
    for hex_share in hex_shares:
        index, trimmed_hex_share = hex_share.split('-')[-2:]

        passphrase = to_passphrase(trimmed_hex_share,
                                   mode='hex',
                                   wordlist_option='bip39')

        print(f'{index} {passphrase}')
        print()


def combine():
    phrases = []
    while True:
        indexed_phrase = input(
            colored('Enter phrase (leave blank to continue): ', 'blue'))
        if indexed_phrase.strip() == '':
            break
        phrases.append(indexed_phrase)
    print()
    number_of_shares = int(input(colored('Number of total shares: ', 'blue')))
    print(
        colored(f'Threshold is assumed from number of entered phrases: {len(phrases)}',
                'blue'))
    print()

    for indexed_phrase in phrases:
        indexed_phrase_parts = indexed_phrase.split()
        index = indexed_phrase_parts[0]
        phrase = ' '.join(indexed_phrase_parts[1:])

        hex_share_not_indexed = from_passphrase(phrase.strip(),
                                                mode='hex',
                                                wordlist_option='bip39')
        hex_share = '-'.join((index, hex_share_not_indexed))

        print(hex_share)
    print()

    subprocess.run(f'ssss-combine -t {len(phrases)} -n {number_of_shares}',
                   shell=True,
                   check=True)


if __name__ == '__main__':
    main()
