import string
from random import randint
import random
import names


def random_name() -> list:
    f_name = names.get_first_name()
    l_name = names.get_last_name()

    return [f_name, l_name]


def random_email():
    f_name = names.get_first_name()
    l_name = names.get_last_name()
    email = f_name + l_name + str(randint(1000, 99999)) + "@gmail.com"
    return (email).lower()


def random_password():
    return ''.join(
        [
            random.choice(string.ascii_letters + string.digits)
            for n in range(16)
        ]
    )
