from random import random
import random
import string


def clear_file(filename):
    with open(filename, 'w'):
        pass


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def my_sorted(iterable, *, key=lambda x: x, reverse=False):
    if not reverse:
        for i in range(len(iterable) - 1):
            for j in range(i + 1, len(iterable)):
                if key(iterable[i]) > key(iterable[j]):
                    aux = iterable[j]
                    iterable[j] = iterable[i]
                    iterable[i] = aux
    else:
        for i in range(len(iterable) - 1):
            for j in range(i + 1, len(iterable)):
                if key(iterable[i]) < key(iterable[j]):
                    aux = iterable[j]
                    iterable[j] = iterable[i]
                    iterable[i] = aux
    return iterable
