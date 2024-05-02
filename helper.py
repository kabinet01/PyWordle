import os


def print_line_break():
    """Print a line break for formatting purpose
    """
    print('=' * 50)


def clear_screen():
    """Helper function to clear screen for formatting
    """
    os.system("clear || cls")


def delay_clear():
    """Clear the screen after receiving user input
    """
    input('Press Enter to continue...')
    clear_screen()
