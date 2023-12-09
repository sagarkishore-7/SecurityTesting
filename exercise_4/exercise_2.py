"""
Use this file to implement your solution for exercise 4-2
"""


import random
import string

from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from fuzzingbook.Grammars import srange, opts


def generate_country_code():
    return random.choice(iban_cc_len)


def generate_valid_iban(Country_code, check_digit, b_ban):
    selected_country = generate_country_code()
    country_code = selected_country[0]
    iban_length = selected_country[1]

    bban_length = iban_length - len(country_code) - 2
    bban = generate_random_bban(bban_length)

    iban = f"{country_code}{check_digit}{bban}"

    return iban

def generate_random_bban(length):
    return ''.join(random.choice('0123456789') for _ in range(length))

def calculate_check_digits(iban):
    country_code = iban[:2]

    for t in iban_cc_len:
        if t[0] == country_code:
            expected_length = t[1]

    if len(iban) != expected_length:
        raise ValueError("Invalid IBAN length for country {}".format(country_code))

    modified_iban = iban[:2] + '00' + iban[4:]

    modified_iban = modified_iban[4:] + modified_iban[:4]

    digit_iban = ""
    for char in modified_iban:
        if char.isalpha():
            digit_iban += str(ord(char.upper()) - ord('A') + 10)
        else:
            digit_iban += char


    new_number = int(digit_iban)
    remainder = new_number % 97
    check_digits = 98 - remainder

    if len(str(check_digits)) < 2:
        check_digits = '0' + str(check_digits)
    else:
        check_digits = str(check_digits)

    return country_code + check_digits + iban[4:]

iban_cc_len = [("AL", 28), ("AD", 24), ("AT", 20), ("AZ", 28), ("BH", 22), ("BY", 28), ("BE", 16),
               ("BA", 20), ("BR", 29), ("BG", 22), ("CR", 22), ("HR", 21), ("CY", 28), ("CZ", 24),
               ("DK", 18), ("DO", 28), ("SV", 28), ("EE", 20), ("FO", 18), ("FI", 18), ("FR", 27),
               ("GE", 22), ("DE", 22), ("GI", 23), ("GR", 27), ("GL", 18), ("GT", 28), ("HU", 28),
               ("IS", 26), ("IQ", 23), ("IE", 22), ("IL", 23), ("IT", 27), ("JO", 30), ("KZ", 20),
               ("XK", 20), ("KW", 30), ("LV", 21), ("LB", 28), ("LI", 21), ("LT", 20), ("LU", 20),
               ("MK", 19), ("MT", 31), ("MR", 27), ("MU", 30), ("MD", 24), ("MC", 27), ("ME", 22),
               ("NL", 18), ("NO", 15), ("PK", 24), ("PS", 29), ("PL", 28), ("PT", 25), ("QA", 29),
               ("RO", 24), ("LC", 32), ("SM", 27), ("ST", 25), ("SA", 24), ("RS", 22), ("SC", 31),
               ("SK", 24), ("SI", 19), ("ES", 24), ("SE", 24), ("CH", 21), ("TL", 23), ("TN", 24),
               ("TR", 26), ("UA", 29), ("AE", 23), ("GB", 22), ("VA", 22), ("VG", 24)]

IBAN_GRAMMAR = {
    "<start>": [("<iban>", opts(post=calculate_check_digits))],
    "<iban>": [("<country_code><check_digits><bban>", opts(post=generate_valid_iban))],
    "<country_code>": ["<letter><letter>"],
    "<check_digits>": ["<digit><digit>"],
    "<bban>": ["<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<letter>": srange(string.ascii_uppercase),
    "<digit>": srange(string.digits),
}


if __name__ == '__main__':
    fuzzer = GeneratorGrammarFuzzer(IBAN_GRAMMAR)
    for _ in range(20):
        print(fuzzer.fuzz())
