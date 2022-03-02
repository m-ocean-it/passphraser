import random
from termcolor import colored

from lib import from_passphrase, to_passphrase

TEST_LOG_PATH = 'test.log'

WORDLIST_OPTIONS = ('BIP39', 'EFF', 'Norvig')


def main():
    test_for_symmetry()


def test_for_symmetry():
    for i in range(50):

        mode = ('ascii', 'hex')[i % 2]
        if mode == 'ascii':
            test_data = get_random_ascii_str()
        elif mode == 'hex':
            test_data = get_random_hex_str()

        print('TESTING FOR SYMMETRY')
        print('====================', end='\n\n')

        for j, wordlist_option in enumerate(WORDLIST_OPTIONS):
            print(f'TEST {j+1} ===>')
            passphrase = to_passphrase(test_data,
                                       mode=mode,
                                       wordlist_option=wordlist_option,
                                       verbose=True)

            recovered = from_passphrase(passphrase,
                                        mode=mode,
                                        wordlist_option=wordlist_option,
                                        verbose=True)

            error_msg = f'Should have recovered:\n{test_data}\ninstead of\n{recovered}\n'
            if recovered != test_data:
                with open(TEST_LOG_PATH, 'a') as f:
                    f.write(f'{error_msg}\n')
                raise AssertionError(
                    f'\n\n{error_msg}\nLogged to {TEST_LOG_PATH}')
            print(f'<=== TEST {i} PASSED', end='\n\n')

        print(colored('HOORRAY! SYMMETRY IS PRESERVED.', 'green'))


def get_random_ascii_str():
    length = random.randint(1, 100)
    chars = tuple(chr(i) for i in range(256))

    arr = []
    for _ in range(length):
        random_char = random.choice(chars)
        arr.append(random_char)

    return ''.join(arr)


def get_random_hex_str():
    length = random.randint(1, 100)
    chars = '0123456789abcdef'

    arr = []
    for _ in range(length):
        random_char = random.choice(chars)
        arr.append(random_char)

    return ''.join(arr)


if __name__ == '__main__':
    main()
