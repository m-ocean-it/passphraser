from termcolor import colored

from main import from_passphrase, to_passphrase

WORDLIST_OPTIONS = ('BIP39', 'EFF')

data = 'ab12'


def main():
    test_for_symmetry()


def test_for_symmetry():
    print('TESTING FOR SYMMETRY')
    print('====================', end='\n\n')

    for i, wordlist_option in enumerate(WORDLIST_OPTIONS):
        print(f'TEST {i} ===>')
        passphrase = to_passphrase(data,
                                   wordlist_option=wordlist_option,
                                   verbose=True)

        recovered = from_passphrase(passphrase,
                                    wordlist_option=wordlist_option,
                                    verbose=True)

        assert recovered == data, colored(
            f'Should have recovered: {data}', 'red')
        print(f'<=== TEST {i} PASSED', end='\n\n')

    print(colored('HOORRAY! SYMMETRY IS PRESERVED.', 'green'))


if __name__ == '__main__':
    main()
