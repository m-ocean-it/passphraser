def get_max_fitting_degree_of_two(n):
    assert n >= 2
    i = 1
    while 2**i <= n:
        i += 1
    return i-1
