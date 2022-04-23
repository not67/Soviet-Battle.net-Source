import random


def random_birthdate():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1970, 1998)

    return {'day': day, 'month': month, 'year': year}
