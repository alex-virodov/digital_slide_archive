# DSA still allows password login for ldap users (not sure if can be disabled & restricted to ldap only).
# Generate a long random password that will not be actually used, but will prevent a password login.

# Adjusted from https://geekflare.com/password-generator-python-code/
import secrets
import string


def generate_random_password(password_length):
    # define the alphabet
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    pwd = ''
    for i in range(password_length):
        pwd += ''.join(secrets.choice(alphabet))

    # generate password meeting constraints
    while True:
        pwd = ''
        for i in range(password_length):
            pwd += ''.join(secrets.choice(alphabet))

        if (any(char in special_chars for char in pwd) and
                sum(char in digits for char in pwd) >= 2):
            break
    return pwd


if __name__ == '__main__':
    print(generate_random_password(password_length=24))
