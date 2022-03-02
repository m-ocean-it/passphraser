# Passphraser

Convert any data to a passphrase and back.

Unique features:
- Several built-in wordlists (and ability to define your own later).
- Accepting input of arbitrary length. No upper limit, no requirement for an even number of characters.

## Use cases

- Make a long code more readable, communicable, and less error-prone by converting it to a passphrase.

## Usage
```bash
$ chmod +x ./passphraser.py

# Encrypt
$ ./passphraser.py --mode hex --wordlist bip39 "afdea69732ce3e1fb46dc8"
[Result] quit vivid place grain token average spider ribbon abandon

# Decrypt (use -d flag)
$ ./passphraser.py -d --mode hex --wordlist bip39 "quit vivid place grain token average spider ribbon abandon"
[Result] afdea69732ce3e1fb46dc8
```


## How does it work?

> You can use the -v flag to see detailed output.

- Select a wordlist and calculate `k` — the required size of binary chunks. (Note: if the length of the list is not a power of 2, then some words won't be used.)
- Input: `ab12` (hexadecimal).
- Decode each symbol into a 4-sized binary chunk and then join them into a single binary array: `1010 1011 0001 0010` -> `1010101100010010`.
- Chop that array to chunks of length `k`: `10101011000 10010`. (Here, `k=11`. The last chunk may be shorter if there's not enough bits. `k` is determined by the length of the selected wordlist.)
- Pad the last chunk if needed: `10101011000 10010000000`. Chunks must be of same size.
- Add helper-chunk to remember the amount of padding. Result: `10101011000 10010000000 [11111100000]`. (6 ones in the helper-chunk represent 6 zeroes added to the last chunk for padding.)
- Convert each chunk to a decimal integer: `1368 1152 2016`.
- Fetch words with corresponding indices from the wordlist: `prison mosquito winter`. (The last word encodes the helper-chunk and, thus, stores information about padding.)

Decoding the passphrase back to the original value is done in reverse.


## TODO
### Now

- [ ] Add optional numbered output like this:
```
1.  19      across
2.  1624    slab
3.  218     brass
4.  139     bacon
```

### Later
- [ ] Allow user-defined wordlists
- [ ] Package for PyPI
- [ ] Compile to standalone executables
