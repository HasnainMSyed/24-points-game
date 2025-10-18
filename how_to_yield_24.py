from itertools import permutations

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

if __name__ == "__main__":
    L = [1,6,6,6]
    print(how_to_yield_X(24, all_possible_results(L)))