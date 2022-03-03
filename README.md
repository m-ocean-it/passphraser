# Passphraser

*Encode any data as a passphrase and decode it back.*

My initial motivation was to simplify putting codes, resulted from applying Shamir Secret Sharing Scheme to my secret, on paper. I used the `ssss` utility to get the codes. The problem was that it spit out long hexadecimal values that are not easy to write down. QR encoding and printing them was not an option since I didn't want the secret (even in its Shamir-split form) to leave the memory of the machine (running Tails OS) and I wasn't at all confident that using a printer would be safe. So I decided the best way was to encode those hex values as passphrases and carefully write them down. That's how this repo came to life. Welcome!

Unique features:
- Several built-in wordlists (and ability to define your own later).
- Accepting input of arbitrary length. No upper limit, no requirement for an even number of characters.
- Accepting not only hexadecimal values but also any ASCII strings (use `--mode ascii`).


## Usage
> Use the --help flag.

```bash
$ chmod +x ./passphraser.py

# Encode:
$ ./passphraser.py --mode hex --wordlist bip39 "afdea69732ce3e1fb46dc8"
[Result] quit vivid place grain token average spider ribbon abandon

# Decode: (use the -d flag)
$ ./passphraser.py -d --mode hex --wordlist bip39 "quit vivid place grain token average spider ribbon abandon"
[Result] afdea69732ce3e1fb46dc8
```


## What happens under the hood

> You can use the -v flag to see detailed output.

- Calculate `k` — the required size of binary chunks. It depends on the the length of the selected wordlist. (Note: if the length of the list is not a power of 2, then some words won't be used.)
- Input: `ab12` (hexadecimal).
- Decode each symbol into a 4-sized binary chunk and then join them into a single binary array: `1010 1011 0001 0010` -> `1010101100010010`.
- Chop that array to chunks of length `k`: `10101011000 10010`. (Here, `k=11`. The last chunk may be shorter if there's not enough bits. That gets fixed next.)
- Pad the last chunk with zeroes if needed: `10101011000 10010000000`. Chunks must be of same size.
- Add helper-chunk to remember the amount of padding. Result: `10101011000 10010000000 [11111100000]`. (6 ones in the helper-chunk represent 6 zeroes added to the last chunk for padding.)
- Decode each chunk to a decimal integer: `1368 1152 2016`.
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
- [ ] Add test for CLI (`passphrase.py`)
- [ ] Allow user-defined wordlists
- [ ] Package for PyPI
- [ ] Compile to standalone executables
