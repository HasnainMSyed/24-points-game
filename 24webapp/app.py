from flask import Flask, request, jsonify
from itertools import permutations
import random

# Core Logic of the 24 Games
def get_possible_values(numbers: list[int | float]) -> set[tuple[float, str]]:
    # Accept a fixed order of numbers ranging from 1 to 13 as input

    # Base case for the recursion:
    if len(numbers) == 1:
        return {(float(numbers[0]), f"{numbers[0]}")}
    
    # Sets up the result as a function of set
    results = set()

    # Split the string into left and right to conduct recursion
    for i in range(1, len(numbers)):
        left_numbers = numbers[:i]
        right_numbers = numbers[i:]

        left_results = get_possible_values(left_numbers)
        right_results = get_possible_values(right_numbers)
    
        for L in left_results:
            for R in right_results:
                # Addition
                results.add((L[0] + R[0], f"({L[1]} + {R[1]})"))

                # Multiplication
                results.add((L[0] * R[0], f"({L[1]} * {R[1]})"))

                # Subtraction
                results.add((L[0] - R[0], f"({L[1]} - {R[1]})"))
                results.add((R[0] - L[0], f"({R[1]} - {L[1]})"))

                # Division
                if R[0] != 0:
                    results.add((L[0] / R[0], f"({L[1]} / {R[1]})"))
                if L[0] != 0:
                    results.add((R[0] / L[0], f"({R[1]} / {L[1]})"))

    return results

def all_possible_results(numbers: list[int]) -> set[tuple[float, str]]:
    all_results = set()
    # Generate all the permutations of the given numbers
    for p in set(permutations(numbers)):
        # Calculate all the outputs for this specific order
        results_for_p = get_possible_values(list(p))

        all_results.update(results_for_p)

    return all_results

def how_to_yield_X(X: int, outputs: set[tuple[float, str]]) -> str:
    add_on_string = f"To return {X}, the following solutions exist:\n"
    counter = 0
    for i in outputs:
        if abs(i[0] - X) < 1e-6:
            counter += 1
            add_on_string += f"{counter}. {i[1]}\n"
    
    if counter > 0:
        return add_on_string
        
    return "Impossible"

# Core Game Logic
class Cards:
    # Define the traits of a card
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

def create_deck():
    suits = ["H", "S", "C", "D"] # All poker suits
    ranks = list(range(1,14))
    deck = [] # Start with an empty list

    for s in suits:
        for r in ranks:
            deck.append(Cards(s, r)) # use append
    return deck

# shuffle games from a standard 52-card set
# This function is run once for every game in mode 1
def mode_1():
    Deck = create_deck()

    # Shuffle the deck so the order becomes random
    random.shuffle(Deck)

    all_card_sets = []

    # Go through the cards in step of four to extract a set every step
    for i in range(0, 52, 4):
        # Get the first game
        game = Deck[i:i+4]

        # Get the ranks of the same game
        # This can be put in the core logic functions to output an answer
        game_ranks = [card.rank for card in game]

        # Fetch all the data about this game
        game_data = [{"suits": c.suit, "rank": c.rank} for c in game]

        all_card_sets.append({"cards": game_data, "numbers": game_ranks})
    
    return all_card_sets

# shuffle a random game for the player
# This function is run every time the player solves or fails to solve a game
def mode_2():
    Deck = create_deck()
    
    # Randomly extract four unique cards with random.sample
    drawn_cards = random.sample(Deck, 4)

    # We need to get the game_numbers to put the core 24 points function logic
    game_numbers = [card.rank for card in drawn_cards]

    # return a dictionary / JSON object to be flask-friendly
    return {
        "cards": [{"suit": c.suit, "rank": c.rank} for c in drawn_cards],
        "numbers": game_numbers
    }



app = Flask(__name__)

@app.route('/solve', method=['POST'])

def solve_24():
    # 1. Get the numbers from incoming JSON request
    data = request.get_json()
    numbers = data.get('numbers')