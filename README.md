# Passphraser

Convert any data to a passphrase and back.

## Use cases

- Make a long code more readable, communicable, and less error-prone by converting it to a passphrase.

## How does it work?
- Select a wordlist and calculate `k` — the required size of binary chunks.
- Input: `ab12` (hexadecimal).
- Convert to binary: `1010101100010010`.
- Chop to chunks of length `k`: `10101011000 10010`. (Here, `k=11`. The last chunk may be shorter due to insufficient binary places.)
- Pad the last chunk if needed: `10101011000 10010000000`. Chunks must be of same size.
- Add helper-chunk to remember the amount of padding. Result: `10101011000 10010000000 [11111100000]`. (6 ones in the helper-chunk represent 6 zeroes added to the last chunk for padding.)
- Convert each chunk to a decimal integer: `1368 1152 2016`.
- Fetch corresponding words from the wordlist: `prison mosquito winter`.

Decoding the passphrase back to the original value is done in reverse.


## TODO
### Now

- [ ] Add input modes: "hex", "bin", "str". Currently only hex input is supported.
- [ ] Add optional numbered output like this:
```
19      across
1624    slab
218     brass
139     bacon
```

### Later
- [ ] Add options for wordlists: built-in and user-defined
- [ ] Add CLI
- [ ] Package for PyPI
- [ ] Compile to standalone executables