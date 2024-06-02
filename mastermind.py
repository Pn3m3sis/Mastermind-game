import sys
import random

class SecretCode:
    def __init__(self):
        self.code = []

    def generate_code(self):
        self.code = random.sample(range(0, 10), 5)  # Generate 5 unique random numbers

    def get_code(self):
        return self.code

    def hit_and_match(self, guess):
        hit_counter = sum(1 for g, c in zip(guess, self.code) if g == c)
        match_counter = sum(min(guess.count(n), self.code.count(n)) for n in set(guess))
        return hit_counter, match_counter

def scoreboard(counter):
    while True:
        save = input("Do you want to save your score? Y/N ").strip().lower()
        if save == 'y':
            playername = input("Please enter your name: ")
            append_score(playername, counter)
            break
        elif save == 'n':
            print("Exiting without saving the score.")
            restart()
            break
        else:
            print('Invalid input. Please enter Y or N.')

def append_score(playername, counter):
    try:
        with open('scoreboard.txt', 'a') as file:
            file.write(f'{counter},{playername}\n')
        print("Scoreboard updated successfully.\n")
        view_score()
    except Exception as e:
        print(f"An error occurred while updating the scoreboard: {e}")

def restart():
    while True:
        again = input('Do you want to play again? Y/N ').strip().lower()
        if again == 'y':
            main()
            break
        elif again == 'n':
            print('Goodbye.')
            sys.exit()
        else:
            print('Invalid input. Use Y or N.')

def view_score():
    try:
        with open('scoreboard.txt', 'r') as file:
            lines = file.readlines()

        scores = []
        for line in lines:
            line = line.strip()
            if line:
                try:
                    number, name = line.split(',', 1)
                    number = int(number)
                    scores.append((number, name))
                except ValueError:
                    print(f"Invalid line format: {line}")

        scores.sort(key=lambda x: x[0])

        print("Top 10 Scores:")
        for i, (number, name) in enumerate(scores[:10], start=1):
            print(f"{i}. {name} - {number} tries")

        restart()
    except FileNotFoundError:
        print("The file 'scoreboard.txt' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    x = SecretCode()
    x.generate_code()

    print('Hi, welcome to Mastermind.')
    print('Secret code has been generated. \n')
    print('Enter five digits separated by spaces. Enter \'q\' to quit.\n')

    counter = 0

    while True:
        user = input('Guess: ')
        if user.lower() == 'q':
            break

        guess = user.split()
        if len(guess) != 5 or not all(g.isdigit() for g in guess):
            print('Wrong format: Enter five digits separated by spaces. Enter \'q\' to quit.\n')
            continue

        guess = [int(g) for g in guess]
        hits, matches = x.hit_and_match(guess)

        if hits == 5:
            print(f'Congratulations, you are a mastermind! You finished in {counter} tries.')
            scoreboard(counter)
            break
        else:
            print(f'hits={hits} matches={matches}')
            counter += 1

if __name__ == "__main__":
    main()
