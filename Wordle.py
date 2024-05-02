from helper import clear_screen, print_line_break
from PyDictionary import PyDictionary


def make_green(text):
    """Transform the text color to green using ANSI encoding

    Args:
        text (text): text

    Returns:
        text: color encoded text
    """
    return f"\033[38;2;0;128;0m{text}\033[0m"


def make_yellow(text):
    """Transform the text color to yellow using ANSI encoding

    Args:
        text (text): text

    Returns:
        text: color encoded text
    """
    return f"\033[33m{text}\033[0m"


def make_red(text):
    """Transform the text color to red using ANSI encoding

    Args:
        text (text): text

    Returns:
        text: color encoded text
    """
    return f"\033[31m{text}\033[0m"


def get_user_guess():
    """Get the user guesses

    Returns:
        text: guess
    """
    return input("Enter a word that is 5 letters long: ")


def verify_length(text):
    """Verify the length of text

    Args:
        text (string): user guess

    Returns:
        bool: return true if length is 5, else return false
    """
    return len(text) == 5


def explain_word(word):
    """Calls the PyDictionary library to print the meaning of words

    Args:
        word (string): word
    """
    try:
        dictionary = PyDictionary()
        meaning = dictionary.meaning(word)

        # Print the meaning
        print(f"The meaning of '{word}' is:")
        for part_of_speech, definitions in meaning.items():
            print(f"{part_of_speech}:")
            for definition in definitions:
                print(f"- {definition}")
    except AttributeError:
        print(f'The meaning of {word} is not in the library')
        

class Wordle_Game:
    """Class for the Game
    """
    def __init__(self, random_word):
        self.random_word = random_word
        self.guesses = []
        self.attempts = 6
    
    def print_instruction(self):
        """Print the instruction of the game
        """
        clear_screen()
        print_line_break()
        print('You will have 6 attempts to guess the secret word successfully')
        print("After each guess, the game will provide feedback in the form of colored letters")
        print(f"{make_green('Green')}: Correct letter in the correct position.")
        print(f"{make_yellow('Yellow')}: Correct letter but in the wrong position.")
        print(f"{make_red('Red')}: Letter not in the secret word.")
        print_line_break()

    def display_all(self):
        """Helper function to display all user guesses
        """
        for i in self.guesses:
            print(i)

    def change_color(self, guess, correct_pos, incorrect_pos, wrong_pos):
        """Function to change color based on the three position list

        Args:
            guess (string): User guess
            correct_pos (list): list of positions of correct letters in the correct position 
            incorrect_pos (list): list of positions of correct letters in the incorrect position 
            wrong_pos (list): list of positions of incorrect letters
        """
        guess = list(guess)
        for i in correct_pos:
            guess[i] = make_green(guess[i])
        for i in incorrect_pos:
            guess[i] = make_yellow(guess[i])
        for i in wrong_pos:
            guess[i] = make_red(guess[i])
        guess = ''.join(guess)
        self.guesses.append(guess)

    def check_letters(self, guess):
        """compare a guess with a target word and 
        categorize the letters based on whether they are in the 
        correct position, in the word but in the wrong position, or not in the word at all.

        Args:
            guess (_type_): user guess

        Returns:
            list: list of positions of correct letters in the correct position
            list: list of positions of correct letters in the incorrect position 
            list: list of positions of incorrect letters
        """
        correct_pos, incorrect_pos, wrong_pos = [], [], []
        guess, word = list(guess), list(self.random_word)
        for i in range(5):
            if guess[i] == word[i]:
                correct_pos.append(i)
                word[i] = " "

        for i in range(5):
            if guess[i] in word:
                idx = word.index(guess[i])
                word[idx] = " "
                incorrect_pos.append(i)
            else:
                wrong_pos.append(i)
        return correct_pos, incorrect_pos, wrong_pos

    def check_input(self, guess):
        """Check if the user guess is the random word

        Args:
            guess (string): User guess

        Returns:
            boolean: return true
        """
        if guess == self.random_word:
            print('Correct!')
            correct_pos, incorrect_pos, wrong_pos = self.check_letters(guess)
            print_line_break()
            self.change_color(guess, correct_pos, incorrect_pos, wrong_pos)
            self.display_all()
            print_line_break()
            return True

    def is_valid_word(self, guess):
        """Check if the user input is within the word list

        Args:
            guess (string): User guess

        Returns:
            boolean: Return true if the user input is valid
        """
        with open('valid-word.txt', 'r') as f:
            return guess.lower() in f.read()

    def play(self):
        """
        Main Function for the game.
        Starts the Game
        """
        self.print_instruction()
        # While the user still have at least 1 attempts
        while self.attempts > 0:
            print(f'You have {self.attempts} guesses remaining')
            print_line_break()
            
            # Get the user input, and make it upper case
            user_input = get_user_guess().upper()
            clear_screen()
            print_line_break()
            print(f'You guessed: {user_input}')
            
            # Guard clause to ensure that user input is proper
            # Only 5 char long
            if not verify_length(user_input):
                print('Your word must be 5 character long')
                self.display_all()
            # Check if user input is a valid word
            elif not self.is_valid_word(user_input):
                print('Your word is invalid')
                self.display_all()
                
            # If passes all checks, proceed to verify the user input against the randomly generated word
            else:
                # Minus one attempt since there is a valid guess
                self.attempts -= 1
                
                # Do a check if its the same word, if so, return true
                if self.check_input(user_input):
                    explain_word(self.random_word)
                    return True
                
                # If it didnt return from the previous if statement, proceed to check the letters
                # Returns the output of check letters to the three list
                correct_pos, incorrect_pos, wrong_pos = self.check_letters(
                    user_input)
                
                # ANSI encode the color and display
                self.change_color(user_input, correct_pos,
                                  incorrect_pos, wrong_pos)
                self.display_all()

        print("=" * 50)
        print('You lose :(')
        print(f'The word is {self.random_word}')
        print("=" * 50)
        explain_word(self.random_word)
        return False