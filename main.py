import os

from utils import get_max_fitting_degree_of_two


WORDLISTS_DIR = 'wordlists'


def to_passphrase(
        hex_str: str,
        wordlist_option: str = 'BIP39') -> str:

    binary_str = bin(int(hex_str, 16))[2:]

    wordlist = get_wordlist(wordlist_option)
    chunk_size = get_max_fitting_degree_of_two(len(wordlist))

    binary_chunks = []
    for i in range(0, len(binary_str), chunk_size):
        chunk = binary_str[i:i+chunk_size].rjust(chunk_size, '0')

        binary_chunks.append(chunk)

    integers = [int(x, 2) for x in binary_chunks]

    words = [wordlist[i] for i in integers]

    return ' '.join(words)


def from_passphrase(
        passphrase: str,
        wordlist_option: str = 'BIP39') -> str:

    words = passphrase.split()

    wordlist = get_wordlist(wordlist_option)

    integers = [wordlist.index(word)
                for word in words]

    binary_chunks = [Binary(i) for i in integers]

    binary_str = ''.join(binary_chunks)

    hex_num = binToHex(binary_str)
    hex_str = str(hex_num)[2:]

    return hex_str


def get_wordlist(wordlist_option: str = 'BIP39'):
    path = os.path.join(WORDLISTS_DIR, wordlist_option)
    with open(path) as file:
        return [line.rstrip() for line in file]


def Binary(n):
    s = bin(n)

    # removing "0b" prefix
    s1 = s[2:]

    return s1


def binToHex(n):

    # convert binary to int
    num = int(n, 2)

    # convert int to hexadecimal
    hex_num = hex(num)
    return hex_num
