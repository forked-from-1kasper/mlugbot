#! /usr/bin/env python3
import random
from sys import stdin
splitter = '\n%\n'


# Это вы не смотрите
def get_random(data):
    while True:
        i = random.randint(0, len(data) - 1)
        if bool(data[i]):
            return data[i]


def get_random_from_file(file):
    f = open(file, 'r')
    data = f.read()
    f.close()

    data = data.split(splitter)

    return get_random(data)


#if __name__ == "__main__":
#    data = stdin.read()
#    data = data.split(splitter)
#    print(get_random(data))