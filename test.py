from main import from_passphrase, to_passphrase

data = 'ab12'

passphrase = to_passphrase(data)
recovered = from_passphrase(passphrase)

print('Recovered:')
print(recovered)
assert recovered == data
print('All good.')
