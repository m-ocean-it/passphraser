import random
from termcolor import colored

from main import from_passphrase, to_passphrase

WORDLIST_OPTIONS = ('BIP39', 'EFF')


def main():
    test_for_symmetry()


def test_for_symmetry():
    for _ in range(50):

        test_data = get_random_hex_str()

        print('TESTING FOR SYMMETRY')
        print('====================', end='\n\n')

        for i, wordlist_option in enumerate(WORDLIST_OPTIONS):
            print(f'TEST {i} ===>')
            passphrase = to_passphrase(test_data,
                                       wordlist_option=wordlist_option,
                                       verbose=True)

            recovered = from_passphrase(passphrase,
                                        wordlist_option=wordlist_option,
                                        verbose=True)

            assert recovered == test_data, colored(
                f'Should have recovered: {test_data}', 'red')
            print(f'<=== TEST {i} PASSED', end='\n\n')

        print(colored('HOORRAY! SYMMETRY IS PRESERVED.', 'green'))


def get_random_hex_str():
    length = random.randint(1, 80)
    chars = '0123456789abcdef'

    arr = []
    for _ in range(length):
        random_char = random.choice(chars)
        arr.append(random_char)

    return ''.join(arr)


if __name__ == '__main__':
    main()
