# imports
import random


# ################# Guess Game ##################

# a function to generate a random number depend on the chosen level
def generate_number(n):
    secret_number = random.randint(0, n)
    return secret_number


# a function for the user the guess the number that the pc generated
def get_guess_from_user(n):
    inp = int(input(f"please choose a number between 0 and {n}: "))
    while inp > n or inp < 0:
        inp = int(input(f"please choose a number between 0 and {n}: "))
    return inp


# a function the check if the user guess number and the generated number is equal
def compare_results(gn, ug):
    if gn == ug:
        print("Yes YOU WON")
        print(f"you choose {ug} and the PC choose {gn}")
        return True
    else:
        print(f"OOPS TRY AGAIN (YOU LOST)\nthe real number was {gn} and not {ug}")
        return False
