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


def get_max_fitting_degree_of_two(n):
    assert n >= 2
    i = 1
    while 2**i <= n:
        i += 1
    return i-1


def amount_of_chars_in_beginning(string: str, char: str):
    assert string
    res = 0
    for ch in string:
        if ch == char:
            res += 1
        else:
            break
    return res
