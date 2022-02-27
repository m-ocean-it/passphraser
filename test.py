from main import from_passphrase, to_passphrase

WORDLIST_OPTIONS = ('BIP39', 'EFF')

data = 'ab12'


def main():
    test_for_symmetry()


def test_for_symmetry():
    print('TESTING FOR SYMMETRY')
    print('====================', end='\n\n')

    for wordlist_option in WORDLIST_OPTIONS:
        print('Wordlist: ', wordlist_option)

        passphrase = to_passphrase(data,
                                   wordlist_option=wordlist_option)
        print('Passphrase:', passphrase)

        recovered = from_passphrase(passphrase,
                                    wordlist_option=wordlist_option)

        print('Recovered: ', recovered)
        assert recovered == data, f'Should have recovered: {data}'
        print('TEST PASSED')
        print('===========', end='\n\n')

    print('HOORRAY! SYMMETRY IS PRESERVED.')


if __name__ == '__main__':
    main()
