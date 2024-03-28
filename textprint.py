import os
import random
import lass

DIRECTORY = 'prints/survey'


def all_files(directory):
    files = os.listdir(directory)
    ret = []
    for file in files:
        ret.append(directory + "/" + file)
    return ret

def choose_random_print(directory):
    files = os.listdir(directory)
    chosen = random.choice(files)
    return random.choice(lass.break_file_into_paragraphs(directory + "/" + chosen)), lass.get_file_author(directory + "/" + chosen)

if __name__ == '__main__':
    print(choose_random_print(DIRECTORY))