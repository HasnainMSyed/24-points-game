from flask import Flask, request, jsonify, render_template
from itertools import permutations
from operator import add, sub, mul, truediv
import random
import ast

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
def generate_campaign_names():
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
def random_mode():
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


# Confused: Operations and safe_eval func

OPERATORS = {
    ast.Add: add,
    ast.Sub: sub,
    ast.Mult: mul,
    ast.Div: truediv
}

def safe_eval(node, allowed_numbers):

    if isinstance(node, ast.Constant):
        if node.value in allowed_numbers:

            allowed_numbers.remove(node.value)
            return node.value
        else:
            raise ValueError("Unauthorized number used for the game!")
    
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left, allowed_numbers)
        right = safe_eval(node.right, allowed_numbers)
        operator = OPERATORS[type(node.op)]

        if operator == truediv and right == 0:
            raise ZeroDivisionError("Cannot Divide by Zero.")
        
        return operator(left, right)
    
    elif isinstance(node, ast.Expression):
        return safe_eval(node.body, allowed_numbers)
    
    else:
        raise TypeError(f"Operation Type {type(node)} not allowed.")

# Backend Flask

app = Flask(__name__)

# Route 1: Serving the Game Interface
@app.route('/', methods=['GET'])
def index():
    # Serve the main game html page

    return render_template('24_game.html')


# Route 2: Starting the game interface

# Global states variables:
CAMPAIGN_GAMES = []
CURRENT_GAME_INDEX = 0

@app.route('/api/new_game/<mode>', methods=['GET'])
def new_game(mode: str):
    global CAMPAIGN_GAMES, CURRENT_GAME_INDEX

    if mode == 'campaign':
        if not CAMPAIGN_GAMES or CURRENT_GAME_INDEX >= len(CAMPAIGN_GAMES):
            CAMPAIGN_GAMES = generate_campaign_names()
            CURRENT_GAME_INDEX = 0

        hand = CAMPAIGN_GAMES[CURRENT_GAME_INDEX]
        CURRENT_GAME_INDEX += 1

        hand['mode'] = 'campaign'
        hand['hand_index'] = CURRENT_GAME_INDEX - 1

        return jsonify(hand)

    elif mode == 'random':
        hand =  random_mode()
        hand['mode'] = 'random'
        return jsonify(hand)

    return jsonify({"error": "Invalid Game Mode"}), 400


# Route 3: Show Solutions

@app.route('/api/solve', methods=['POST'])
def solve_24():
    # 1. Get the numbers from incoming JSON request
    data = request.get_json()
    numbers = data.get('numbers')

    if not numbers or len(numbers) != 4:
        return jsonify({'error': "Please provide exactly four numbers."}), 400
    
    all_results_tuples = all_possible_results(numbers)

    target = 24.0
    solutions = []

    for value, expression in all_results_tuples:
        if abs(target - value) < 1e06:
            solutions.append(expression)

    return jsonify({
        "solvable": len(solutions) > 0,
        "solutions": solutions
    })

# Route 4: Check User's Answer


@app.route('/api/check_answer')
def check_player_answer():
    data = request.get_json()
    expression = data.get('expression', '')
    numbers = data.get('numbers', [])

    try:
        parsed_ast = ast.parse(expression.strip(), mode='eval')


        result = safe_eval(parsed_ast, numbers.copy())

        if len(numbers) != 0:
            #
            #
            pass

        if abs(result - 24.0) < 1e-6:
            return jsonify({
                "status": "success"
                "message": "Correct! You solved the puzzle!"
                "is_correct": True
            })
        else:
            return jsonify({
                "status": "failure",
                "message": f"Incorrect. The result is {result}.",
                "is_correct": False
            })

    except (ValueError, TypeError, ZeroDivisionError) as e:
        return jsonify({
            "status": "error", 
            "message": f"Invalid expression: {str(e)}", 
            "is_correct": False
        }), 400

    
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Invalid expression structure.",
            "is_correct": False,
        }), 400



if __name__ == "__main__":
    app.run(debug=True)