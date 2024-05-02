import random
import requests
import os
from time import sleep
from getpass import getpass
from hashlib import sha256

# Import Classes
from Wordle import Wordle_Game, clear_screen
from Player import Player
from db import initialize_database, get_leaderboard
from helper import clear_screen, delay_clear, print_line_break



def encrypt_password(input_string):
    """Encryption of User Password. I was lazy in implementing salting/bcrypt.

    Args:
        input_string (strings): Plain Text Password

    Returns:
        strings: Hashed Password
    """
    sha256_hash = sha256(input_string.encode()).hexdigest()
    return sha256_hash


def download_word_list():
    """Download the pre requisite word list
    """
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, 'valid-word.txt')
    if not os.path.exists(file_path):
        print('Word List not installed, please wait a few second while we are installing')
        response = requests.get(
            "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt")
        sleep(2)
        with open('words.txt', 'w') as f:
            f.write(response.text)

    file_path = os.path.join(current_directory, 'common-word.txt')
    if not os.path.exists(file_path):
        print('Word List not installed, please wait a few second while we are installing')
        response = requests.get(
            "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-La.txt")
        sleep(2)
        with open('common-word.txt', 'w') as f:
            f.write(response.text)

def get_random_word():
    """Choose a random word from the word list

    Returns:
        strings: Return the chosen word
    """
    with open('common-word.txt', 'r') as f:
        word = f.read().split()
        random_word = random.choice(word)
    return random_word.upper()


def get_inputs():
    """Get the user input for username and password. 
    Uses getpass for secure password Input

    Returns:
        strings: username, password
    """
    name = input('Enter Username: ')
    password = getpass('Enter Your Password: ')
    # password = input('Enter Your Password: ')
    password = encrypt_password(password)
    return name, password


def authentication():
    """Authentication Login. Returns player objects if authenticated successfully.
    Might need to decouple this into more functions if possible

    Returns:
        object: Player
    """
    while True:
        print_line_break()
        print('''Welcome to Wordle
    1. Login User
    2. Register New User''')
        print_line_break()
        res = input('Choose your option (1-2): ')
        clear_screen()

        if res == '1':
            print('Login User Option Selected')
            print_line_break()

            name, password = get_inputs()
            player = Player(name, password)
            res = player.calls_login_user()
            clear_screen()

            if res:
                print('You have login successfully')
                print(player)
                delay_clear()
                return player

            else:
                print('Invalid credentials, please try again')

        elif res == '2':
            print('Register User Option Selected')
            print_line_break()

            name, password = get_inputs()
            player = Player(name, password)
            res = player.calls_register_user()

            if res:
                print('User registered Successfully')
                delay_clear()
                return player

            else:
                print(
                    'Your user existed in the database, please login or create a new user.')
                delay_clear()

        else:
            delay_clear()


def display_options():
    """Display the options for the main game
    """
    print_line_break()
    print('''1. Play Game
2. Print Leaderboard
3. Quit''')
    print_line_break()

    res = input("Choose your option (1-3): ")
    return res


def initialize_pre_req():
    """Runs function to initialize the pre requisite functions
    """
    download_word_list()
    initialize_database()


def main():
    """Main Function of the Application
    """
    clear_screen()
    initialize_pre_req()
    player = authentication()
    while True:
        print_line_break()
        print(player)
        options = display_options()
        clear_screen()
        if options == '1':
            word = get_random_word()
            game = Wordle_Game(word)
            res = game.play()
            if res:
                player.score += 1
                player.calls_change_score()
            delay_clear()
        elif options == '2':
            print_line_break()
            scores = get_leaderboard()
            for i in range(len(scores)):
                print(
                    f"{i+1} Place: Name: {scores[i][0]}, Scores: {scores[i][1]}")
        elif options == '3':
            quit()
        else:
            print('You have selected an invalid options')
            continue


if __name__ == '__main__':
    main()
