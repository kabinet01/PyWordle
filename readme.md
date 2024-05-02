# PyWordle

## What is Wordle

Wordle is a word puzzle game where players try to guess a secret five-letter word within a certain number of attempts. After each guess, the game provides feedback, indicating which letters are correct and in the right position, which letters are correct but in the wrong position, and which letters are not in the word at all. To improve upon the game, we used the PyDictionary library to help explain what is the meaning of the word, and a leaderboard to foster competition amongst the player.

Color Feedback:

- Green: Right letter in the RIGHT position
- Yellow: Right letter in the WRONG position
- Red: Letter DOES NOT EXIST in the word

Note:

- The ANSI color coding is tested to work on WSL Ubuntu 22.04.3 LTS and Windows 11.
- The PyDictionary module requires internet access, if there is no internet access, it will just print the meaning of the word is not in the library.

## Running the application

```bash
pip3 install -r requirements.txt
python3 main.py
```

Test Credential

```text
test:test
```
