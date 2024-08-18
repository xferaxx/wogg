# imports
import random
import time
import sys


# ################# MemoryGame ##################

# a function to begin the countdown to remember the list
def begin():
    for remaining in range(5, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining to begin, ".format(remaining))
        sys.stdout.write("Remember the list before disappear.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    return


# a function to show the user the list for duration 0.7
def show(text):
    begin()
    print(f'\r{text}', end='')
    time.sleep(0.7)
    print('\r', end='')


# a function to the user to guess the list
def get_list_from_user(level):
    random_list_user = []
    for i in range(1, level + 1):
        z = 0
        while not 1 <= z <= 101:
            z = int(input(f"please choose your {i}st number from 1 - 101 ONLY: "))
        random_list_user.append(z)
    print(f'your guess {random_list_user}')
    return random_list_user


def generate_sequence(level):
    random_list = [random.randint(1, 101) for _ in range(level)]
    return random_list


# A function to check if the generated list and the user-guessed list are equal
def is_list_equal(user_list, pc_list):
    return user_list == pc_list
