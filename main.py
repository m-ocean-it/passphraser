def main(hex_str: str) -> str:
    '''1'''

    binary_str = bin(int(hex_str, 16))

    binary_chunks = []
    for i in range(2, len(binary_str), 11):
        chunk = binary_str[i:i+11]

        if len(chunk) < 11:
            chunk = chunk.rjust(11, '0')

        binary_chunks.append(chunk)

    integers = map(lambda x: int(x, 2),
                   binary_chunks)

    with open('bip39.txt') as file:
        wordlist = [line.rstrip() for line in file]

    words = [wordlist[i] for i in integers]

    return ' '.join(words)
