import numpy as np
import re

evaluation_array = np.array([
    [300, 400, 500, 700, 500, 400, 300],
    [400, 600, 800, 1000, 800, 600, 400],
    [500, 800, 1100, 1300, 1100, 800, 500],
    [500, 800, 1100, 1300, 1100, 800, 500],
    [400, 600, 800, 1000, 800, 600, 400],
    [300, 400, 500, 700, 500, 400, 300]
])


def compare_evaluation(array):
    rows, cols = np.where(array == 2)
    sum = evaluation_array[rows, cols].sum()
    return sum

def count_pattern_in_string(text, pattern):
    return len(re.findall(pattern, text))

def count_pattern_in_array(array, pattern):
    count = 0
    
    # Count patterns in rows
    for row in array:
        row_str = ''.join(map(str, row))
        count += sum(1 for _ in re.finditer(f'(?=({pattern}))', row_str))

    # Count patterns in columns
    for col in array.T:
        col_str = ''.join(map(str, col))
        count += sum(1 for _ in re.finditer(f'(?=({pattern}))', col_str))

    # Count patterns in diagonals
    for diag in [array.diagonal(i) for i in range(-(array.shape[0] - 1), array.shape[1])]:
        diag_str = ''.join(map(str, diag))
        count += sum(1 for _ in re.finditer(f'(?=({pattern}))', diag_str))

    for diag in [np.flipud(array).diagonal(i) for i in range(-(array.shape[0] - 1), array.shape[1])]:
        diag_str = ''.join(map(str, diag))
        count += sum(1 for _ in re.finditer(f'(?=({pattern}))', diag_str))

    return count

def find_score(array):
    patterns_2222 = ['2222']
    patterns_1111 = ['1111']
    score = [0, 0]
    for pattern in patterns_2222:
        score[0] += count_pattern_in_array(array, pattern)
    for pattern in patterns_1111:
        score[1] += count_pattern_in_array(array, pattern)
    return score

def find_fours(array):
    pattern_2222 = '2222'
    return 1000000 * count_pattern_in_array(array, pattern_2222)

def find_threes(array):
    patterns = ['0222', '2220', '2202', '2022']
    sum = 0
    for pattern in patterns:
        sum += 40000 * count_pattern_in_array(array, pattern)
    return sum

def find_twos(array):
    patterns = ['0022', '0220', '2200', '2002', '2020', '0202']
    sum = 0
    for pattern in patterns:
        sum += 10000 * count_pattern_in_array(array, pattern)
    return sum

def calculate_heuristic(array):
    sum = 0
    sum += compare_evaluation(array)
    sum += find_fours(array)
    sum += find_threes(array)
    sum += find_twos(array)
    return sum