def to_passphrase(hex_str: str) -> str:
    '''1'''

    binary_str = bin(int(hex_str, 16))[2:]

    binary_chunks = []
    for i in range(0, len(binary_str), 11):
        chunk = binary_str[i:i+11].rjust(11, '0')

        binary_chunks.append(chunk)

    integers = [int(x, 2) for x in binary_chunks]

    wordlist = get_wordlist()

    words = [wordlist[i] for i in integers]

    return ' '.join(words)


def from_passphrase(passphrase: str):
    '''2'''

    words = passphrase.split()

    wordlist = get_wordlist()

    integers = [wordlist.index(word)
                for word in words]

    binary_chunks = [Binary(i).rjust(11, '0') for i in integers]

    binary_str = ''.join(binary_chunks)

    hex_str = binToHex(binary_str)

    return hex_str


def get_wordlist():
    with open('bip39.txt') as file:
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
