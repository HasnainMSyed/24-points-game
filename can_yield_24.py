from itertools import permutations

def get_possible_values(numbers: list[int | float]) -> set[float]:
    # Accept a fixed order of numbers ranging from 1 to 13 as input

    # Base case for the recursion:
    if len(numbers) == 1:
        return {float(numbers[0])}
    
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
                results.add(L + R)

                # Multiplication
                results.add(L * R)

                # Subtraction
                results.add(R - L)
                results.add(L - R)

                # Division
                if R != 0:
                    results.add(L/R)
                if L != 0:
                    results.add(R/L)
            
    '''
    [1,2,3,4]
    Layer 1 => Case 1: f([1]) | f([2,3,4])
               Case 2: f([1,2]) | f([3,4])
               Case 3: f([1,2,3]) | f([4])

    Case 1 Layer 2 => f([1]) => [1]
                      1.1: f([2]) | f([3,4])
                      1.2: f([2,3]) | f([4])
    
    Case 2 Layer 2 => f([1]) f([2]) f([3]) f([4])
    
    Case 3 Layer 2 => f([4]) => [4]
                      1.1: f([1]) | f([2,3])
                      1.2: f([1,2]) | f([3])

    Therefore:
    1.1.1 => a ? (b ? (c ? d))
    1.1.2 => a ? ((b ? c) ? d)
    2.1 => (a ? b) ? (c ? d)
    3.1.1 => (a ? (b ? c)) ? d
    3.1.2 => ((a ? b) ? c) ? d
    
    '''

    return results

def all_possible_results(numbers: list[int]) -> list[float]:
    all_results = set()
    # Generate all the permutations of the given numbers
    for p in set(permutations(numbers)):
        # Calculate all the outputs for this specific order
        results_for_p = get_possible_values(list(p))

        all_results.update(results_for_p)

    return list(all_results)

def can_yield_X(X: int, outputs: list[float]) -> bool:
    for i in outputs:
        if abs(X - i) < 1e-6:
            return True
        
    return False

if __name__ == "__main__":
    L = [1,6,6,6]
    print(can_yield_X(24, all_possible_results(L)))

'''
def same_numbers(numbers):
    # Accept a list of four numbers from 1 to 13 as input
    # Output the indices of the numbers that have the same values in a list
    final, temp = [], []
    for i in range(3):
        temp = [i]
        for j in range(i+1,4):
            if numbers[i] == numbers[j]:
                temp.append(j)
        if len(temp) == 2:
            final.append(temp)
        elif len(temp) > 2:
            return temp

    return final

def case_divider(L):
    # Takes in the list from the last function and devide them into five cases
    # to make the solution more efficient
    # Cases are ranked by difficulty
    if len(L) == 4:
        return 0 # Case 0: Easiest case, four equal numbers
    elif len(L) == 3:
        return 1 # Case 1: Three equal numbers
    elif len(L) == 0:
        return 5 # Case 5: Four different numbers
    else:
        if (type(L[1]) is int) == True:
            return 4 # Case 4: 1 pair of same numbers
        else:
            return 3 # Case 3: 2 pairs of same numebers
'''