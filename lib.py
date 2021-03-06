import os
import sys
from termcolor import colored
from typing import Tuple

from utils import (Binary,
                   get_max_fitting_power_of_two,
                   amount_of_chars_in_beginning)


WORDLISTS_DIR = 'wordlists'


def to_passphrase(
        input_str: str,
        mode: str,
        wordlist_option: str = 'bip39',
        verbose=False) -> str:

    assert mode in ('ascii', 'hex')

    input_str = input_str.strip()

    if mode == 'ascii':
        ascii_codes = tuple(ord(char) for char in input_str)
        bin_chunks = tuple(bin(code)[2:].rjust(8, '0')
                           for code in ascii_codes)
    elif mode == 'hex':
        bin_chunks = []
        for char in input_str:
            try:
                i = int(char, 16)
            except ValueError:
                print('[Error] Wrong hexadecimal value.')
                sys.exit(1)
            bin_chunk = bin(i)[2:].rjust(4, '0')
            bin_chunks.append(bin_chunk)
        bin_chunks = tuple(bin_chunks)

    binary_arr = ''.join(bin_chunks)
    wordlist = get_wordlist(wordlist_option)
    chunk_size: int = get_max_fitting_power_of_two(len(wordlist))

    data_chunks = []
    for i in range(0, len(binary_arr), chunk_size):
        chunk: str = binary_arr[i:i+chunk_size]
        data_chunks.append(chunk)

    data_chunks: Tuple[str] = tuple(data_chunks)
    last_chunk: str = data_chunks[-1]
    zeroes_added = 0
    while len(last_chunk) < chunk_size:
        last_chunk += '0'
        zeroes_added += 1
    padded_data_chunks: Tuple[str] = data_chunks[:-1] + (last_chunk,)
    control_chunk: str = ''.join(['1']*zeroes_added).ljust(chunk_size, '0')
    binary_chunks: Tuple[str] = padded_data_chunks + (control_chunk,)

    integers = tuple(int(x, 2) for x in binary_chunks)
    words: Tuple[str] = tuple(wordlist[i] for i in integers)

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
            f'{colored(input_str, "blue")}\n-> {binary_arr}\n-> {data_chunks}\n-> {binary_chunks_str}\n-> {integers}\n-> {colored(passphrase, "blue")}')
        print(colored('--------<<<--------', 'yellow'))

    return passphrase


def from_passphrase(
        passphrase: str,
        mode: str,
        wordlist_option: str = 'bip39',
        verbose=False) -> str:

    assert mode in ('ascii', 'hex')

    words = passphrase.split()
    wordlist = get_wordlist(wordlist_option)
    chunk_size = get_max_fitting_power_of_two(len(wordlist))

    integers = []
    for word in words:
        try:
            i = wordlist.index(word)
        except ValueError:
            print(
                f'[ERROR] No word "{word}" in the wordlist "{wordlist_option}".')
            sys.exit(1)
        integers.append(i)
    integers = tuple(integers)

    binary_chunks: Tuple[str] = tuple(
        Binary(i).rjust(chunk_size, '0') for i in integers)

    control_chunk: str = binary_chunks[-1]
    zeroes_added: int = amount_of_chars_in_beginning(control_chunk, '1')

    data_chunks: tuple = binary_chunks[:-1]

    last_chunk: str = data_chunks[-1]

    if zeroes_added > 0:
        unpadded_last_chunk = last_chunk[:-zeroes_added]
    else:
        unpadded_last_chunk = last_chunk

    unpadded_data_chunks: tuple = \
        data_chunks[:-1] + (unpadded_last_chunk,)
    assert len(unpadded_data_chunks) > 0

    binary_arr = ''.join(unpadded_data_chunks)

    if mode == 'ascii':
        ascii_bin_chunks = tuple(binary_arr[i:i+8]
                                 for i
                                 in range(0, len(binary_arr), 8))
        ascii_codes = tuple(int(chunk, 2) for chunk in ascii_bin_chunks)
        chars = tuple(chr(code) for code in ascii_codes)
    elif mode == 'hex':
        hex_bin_chunks: Tuple[str] = tuple(binary_arr[i:i+4]
                                           for i
                                           in range(0, len(binary_arr), 4))
        ints = tuple(int(chunk, 2) for chunk in hex_bin_chunks)
        chars = tuple(hex(integer)[2:] for integer in ints)

    output = ''.join(chars)

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
            f'{colored(passphrase, "blue")}\n-> {integers}\n-> {binary_chunks_str}\n-> {unpadded_data_chunks_str}\n-> {colored(output, "blue")}')
        print(colored('--------<<<--------', 'yellow'))

    return output


def get_wordlist(wordlist_option: str = 'bip39'):
    path = os.path.join(WORDLISTS_DIR, wordlist_option)
    with open(path) as file:
        words = tuple(stripped_line for stripped_line
                      in (line.strip() for line in file)
                      if stripped_line != '')

        assert len(words) == len(set(words)), \
            'Wordlist contains non-unique words!'

        return words
