from itertools import permutations
import random
import csv
import os

list_of_numbers = list(range(1,14))

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


# Outputs all the possible solutions for a specific set of cards to yield a specific target
def all_possible_results(numbers: list[int]) -> set[tuple[float, str]]:
    all_results = set()
    # Generate all the permutations of the given numbers
    for p in set(permutations(numbers)):
        # Calculate all the outputs for this specific order
        results_for_p = get_possible_values(list(p))

        all_results.update(results_for_p)

    return all_results

def get_a_solution_string_for_target(target: int, outputs: set[tuple[float, str]]) -> str | None:
    target_float = float(target)
    for value, expression in outputs:
        if abs(value - target_float) < 1e-6:
            # Found one! Return it immediately and stop searching.
            return expression
    # Return None if no solution
    return None

def random_four_cards():
    # Draws 4 random numbers from 1-13 (with replacement)
    return random.choices(list(range(1, 14)), k=4)

def save_data(data, mode): # Default to writing mode
    file_path = os.path.join("24_NN", "24_game_data.csv")
    
    # 'w' mode (write/overwrite) is only for the first call (to write the header)
    # 'a' mode (append) is for subsequent calls
    with open(file_path, mode, newline='') as f:
        writer = csv.writer(f)
        
        if mode == "w": # Only writes the header in writing mode
            writer.writerow(['input_numbers', 'target', 'solution_expression'])

        writer.writerows(data) 
    
    print(f"Data saved successfully to {file_path}")

def generate_data(target: int, num_of_samples: int, mode: str):
    data = []
    print(f"Starting data generation for {num_of_samples} samples...")

    for i in range(num_of_samples):
        numbers = random_four_cards()

        all_results = all_possible_results(numbers)
        solution_str = get_a_solution_string_for_target(target, all_results)

        if solution_str:
            # after the comma, we join the list of elements in numbers after converting them to string individually
            input_str = ",".join(map(str, numbers))
            data.append((input_str, str(target), solution_str)) 
            # data appends a tuple of string-ed version of input digits, target and solution
        
        if (i + 1) % 1000 == 0:
            # Tells me how much data is processed by a certain point
            print(f"For target {target}, {i + 1} attempts processed. Collected {len(data)} solvable puzzles.")

    save_data(data, mode)

if __name__ == "__main__":
    num_of_targets, num_of_samples_per_target = 40, 2000
    
    # Generating and priortizing 24
    generate_data(target=24, num_of_samples=num_of_samples_per_target, mode="w")

    # Generalizing for other targets that's not 24
    for target in range(1, num_of_targets + 1):
        if target != 24: # Skip 24 since we just ran it
            # Call the generator, specifying append mode
            generate_data(target, num_of_samples_per_target, mode='a')

    print("All data generated and saved.")