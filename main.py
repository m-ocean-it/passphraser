import os
from termcolor import colored

from utils import (Binary,
                   binToHex,
                   get_max_fitting_degree_of_two,
                   amount_of_chars_in_beginning)


WORDLISTS_DIR = 'wordlists'


def to_passphrase(
        hex_str: str,
        wordlist_option: str = 'BIP39',
        verbose=False) -> str:

    binary_str = bin(int(hex_str, 16))[2:]
    wordlist = get_wordlist(wordlist_option)
    chunk_size = get_max_fitting_degree_of_two(len(wordlist))

    binary_chunks = []
    for i in range(0, len(binary_str), chunk_size):
        chunk = binary_str[i:i+chunk_size]
        binary_chunks.append(chunk)

    last_chunk = binary_chunks[-1]
    zeroes_added = 0
    while len(last_chunk) < chunk_size:
        last_chunk += '0'
        zeroes_added += 1
    binary_chunks[-1] = last_chunk
    control_chunk = ''.join(['1']*zeroes_added).ljust(chunk_size, '0')
    binary_chunks.append(control_chunk)

    integers = [int(x, 2) for x in binary_chunks]
    words = [wordlist[i] for i in integers]

    passphrase = ' '.join(words)

    if verbose:
        binary_chunks_strings = []
        for i in range(len(binary_chunks)):
            chunk = binary_chunks[i]
            if i == len(binary_chunks) - 1:
                chunk = f'[{chunk}]'
            binary_chunks_strings.append(chunk)
        binary_chunks_str = ' '.join(binary_chunks_strings)

        print(colored('-------->>>--------', 'yellow'))
        print('Wordlist:', wordlist_option)
        print(
            f'{colored(hex_str, "blue")}\n-> {binary_str}\n-> {binary_chunks_str}\n-> {integers}\n-> {colored(passphrase, "blue")}')
        print(colored('--------<<<--------', 'yellow'))

    return passphrase


def from_passphrase(
        passphrase: str,
        wordlist_option: str = 'BIP39',
        verbose=False) -> str:

    words = passphrase.split()
    wordlist = get_wordlist(wordlist_option)
    chunk_size = get_max_fitting_degree_of_two(len(wordlist))

    integers = [wordlist.index(word)
                for word in words]

    binary_chunks: Tuple[str] = tuple(Binary(i) for i in integers)
    control_chunk: str = binary_chunks[-1]
    zeroes_added: int = amount_of_chars_in_beginning(control_chunk, '1')
    data_chunks: tuple = binary_chunks[:-1]
    last_chunk: str = data_chunks[-1].rjust(chunk_size, '0')
    unpadded_data_chunks: tuple = \
        data_chunks[:-1] + (last_chunk[:-zeroes_added],)

    binary_str = ''.join(unpadded_data_chunks)

    hex_num = binToHex(binary_str)
    hex_str = str(hex_num)[2:]

    if verbose:
        binary_chunks_strings = []
        for i in range(len(binary_chunks)):
            chunk = binary_chunks[i]
            if i == len(binary_chunks) - 1:
                chunk = f'[{chunk}]'
            binary_chunks_strings.append(chunk)
        binary_chunks_str = ' '.join(binary_chunks_strings)
        unpadded_data_chunks_str = ' '.join(unpadded_data_chunks)
        print(colored('-------->>>--------', 'yellow'))
        print('Wordlist:', wordlist_option)
        print(
            f'{colored(passphrase, "blue")}\n-> {integers}\n-> {binary_chunks_str}\n-> {unpadded_data_chunks_str}\n-> {colored(hex_str, "blue")}')
        print(colored('--------<<<--------', 'yellow'))

    return hex_str


def get_wordlist(wordlist_option: str = 'BIP39'):
    path = os.path.join(WORDLISTS_DIR, wordlist_option)
    with open(path) as file:
        return [line.rstrip() for line in file]
