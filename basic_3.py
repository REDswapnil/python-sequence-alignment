import sys
from pathlib import Path
from typing import Tuple, List
import math
import psutil
import time


def run(str1: str, str2: str):
    pretty_print('Performing Sequence Alignment DP Basic Run')
    pretty_print(f'String 01: {str1} (length - {len(str1)}) and String 02: {str2} (length - {len(str2)})')
    memo_array: List = initialize(len(str1), len(str2))
    pretty_print_matrix(memo_array)
    pretty_print('Building memo array ...')
    for i in range(1, len(str1)):
        for j in range(1, len(str2)):
            memo_array[i][j] = min(MISMATCH_PENALTY[str1[i-1]][str2[j-1]] + memo_array[i-1][j-1],
                                   GAP_PENALTY + memo_array[i-1][j],
                                   GAP_PENALTY + memo_array[i][j-1])

    pretty_print_matrix(memo_array)


def run_wrapper(str1: str, str2: str):
    start_time = time.time()
    run(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    pretty_print(time_taken)


def initialize(str1_len: int, str2_len: int) -> List:
    pretty_print('Initializing memo array...')
    memo_array: List = list()
    for i in range(str1_len):
        col: List = list()
        for j in range(str2_len):
            if i == 0 and j == 0:
                col.append(0)
            elif j == 0:
                col.append(i * GAP_PENALTY)
            elif i == 0:
                col.append(j * GAP_PENALTY)
            else:
                col.append(math.inf)
        memo_array.append(col)
    return memo_array


def pretty_print_matrix(matrix):
    for row in matrix:
        print(row)


def pretty_print(msg: str | int | float):
    print('\n' + str(msg) + '\n')


def generate_str(input_file_path: Path) -> Tuple[str, str]:
    print('Generating input strings')
    str1: str = str()
    str2: str = str()
    temp_str: str = str()
    with input_file_path.open() as ip:
        for line in ip:
            try:
                index = int(line)
                temp_str = temp_str[0: index + 1] + temp_str + temp_str[index + 1: len(temp_str)]
            except ValueError:
                str1 = temp_str
                temp_str = line.strip()
        str2 = temp_str
    return str1, str2


# def process_memory():
# process = psutil.Process()
# memory_info = process.memory_info()
# memory_consumed = int(memory_info.rss/1024)
# return memory_consumed


if __name__ == '__main__':

    GAP_PENALTY = 30
    MISMATCH_PENALTY = {
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }

    pretty_print('Starting Sequence Alignment DP Basic Algorithm...')

    if len(sys.argv) != 3:
        pretty_print('Insufficient Arguments')
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists() or not input_file.is_file():
        pretty_print(f'Input file {sys.argv[1]} does not exist')
        sys.exit(1)

    output_file = Path(sys.argv[2])
    if output_file.is_dir() or not output_file.parent.exists():
        pretty_print('Output file has no valid parent directory or is itself a directory. Expected a valid file path')
        sys.exit(1)
    if not output_file.exists():
        output_file.touch()

    (s1, s2) = generate_str(input_file)

    run_wrapper(s1, s2)
