import sys
from pathlib import Path
from typing import Tuple, List
import math
import psutil
import time


def run(str1: str, str2: str):
    pretty_print('Performing Sequence Alignment DP Basic Run')
    pretty_print(f'String 01: {str1} (length - {len(str1)}) and String 02: {str2} (length - {len(str2)})')
    str1_alignment: str = str()
    str2_alignment: str = str()
    min_index: int = int()
    memo_array: List = initialize(len(str1) + 1, len(str2) + 1)
    min_pointer: List[List[Tuple | None]] = initialize(len(str1) + 1, len(str2) + 1)
    pretty_print_matrix(memo_array)
    pretty_print('Building memo array ...')
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # score_list: List = [MISMATCH_PENALTY[str1[i-1]][str2[j-1]] + memo_array[i-1][j-1],
            #                     GAP_PENALTY + memo_array[i-1][j],
            #                     GAP_PENALTY + memo_array[i][j-1]]
            memo_array[i][j] = min(MISMATCH_PENALTY[str1[i - 1]][str2[j - 1]] + memo_array[i - 1][j - 1],
                                   GAP_PENALTY + memo_array[i - 1][j],
                                   GAP_PENALTY + memo_array[i][j - 1])
            # memo_array[i][j] = min(score_list)
            # min_index = score_list.index(memo_array[i][j])
            # if min_index == 0:
            #     min_pointer[i][j] = (i-1, j-1)
            # elif min_index == 1:
            #     min_pointer[i][j] = (i-1, j)
            # else:
            #     min_pointer[i][j] = (i, j-1)
    pretty_print_matrix(memo_array)
    pretty_print(f'Alignment Score :: {memo_array[len(str1)][len(str2)]}')
    # pretty_print(f'Str1 Alignment :: {str1_alignment}')
    # pretty_print(f'Str2 Alignment :: {str2_alignment}')
    get_alignment(memo_array, str1, str2)
    # get_alignment(min_pointer, str1, str2)


def run_wrapper(str1: str, str2: str):
    start_time = time.time()
    run(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    pretty_print(time_taken)
    pretty_print(process_memory())


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


# def get_alignment(min_pointer_array: List, str1: str, str2: str):
#     pretty_print(f'Getting alignment of the 2 strings from the memo array')
#     align_len = len(str1) + len(str2)
#     str1_align: List = [None] * (align_len + 1)
#     str2_align: List = [None] * (align_len + 1)
#     str1_align_index: int = align_len
#     str2_align_index: int = align_len
#     for i in range(len(str1), 1, -1):
#         for j in range(len(str2), 1, -1):
#             if min_pointer_array[i][j] == (i-1, j-1):
#                 str1_align[str1_align_index] = str1[i-1]
#                 str2_align[str2_align_index] = str2[j - 1]
#                 str1_align_index -= 1
#                 str2_align_index -= 1
#             elif min_pointer_array[i][j] == (i-1, j):
#                 str1_align[str1_align_index] = str1[i - 1]
#                 str2_align[str2_align_index] = '_'
#                 str1_align_index -= 1
#                 str2_align_index -= 1
#             else:
#                 str1_align[str1_align_index] = '_'
#                 str2_align[str2_align_index] = str2[j - 1]
#                 str1_align_index -= 1
#                 str2_align_index -= 1
#     print(str1_align)
#     print(str2_align)


def get_alignment(memo_array: List, str1: str, str2: str):
    pretty_print(f'Getting alignment of the 2 strings from the memo array')
    align_len = len(str1) + len(str2)
    str1_align: List = [None] * (align_len + 1)
    str2_align: List = [None] * (align_len + 1)
    str1_align_index: int = align_len
    str2_align_index: int = align_len
    i = len(str1)
    j = len(str2)
    while not (i == 0 or j == 0):
        if memo_array[i][j] == MISMATCH_PENALTY[str1[i - 1]][str2[j - 1]] + memo_array[i - 1][j - 1]:
            str1_align[str1_align_index] = str1[i-1]
            str2_align[str2_align_index] = str2[j-1]
            str1_align_index -= 1
            str2_align_index -= 1
            i -= 1
            j -= 1
        elif memo_array[i][j] == GAP_PENALTY + memo_array[i - 1][j]:
            str1_align[str1_align_index] = str1[i - 1]
            str2_align[str2_align_index] = '_'
            str1_align_index -= 1
            str2_align_index -= 1
            i -= 1
        else:
            str1_align[str1_align_index] = '_'
            str2_align[str2_align_index] = str2[j - 1]
            str1_align_index -= 1
            str2_align_index -= 1
            j -= 1

    while str1_align_index > 0:
        if i > 0:
            i -= 1
            str1_align[str1_align_index] = str1[i]
            str1_align_index -= 1
        else:
            str1_align[str1_align_index] = '_'
            str1_align_index -= 1

    while str2_align_index > 0:
        if j > 0:
            j -= 1
            str2_align[str2_align_index] = str2[j]
            str2_align_index -= 1
        else:
            str2_align[str2_align_index] = '_'
            str2_align_index -= 1

    id = 1
    i = align_len
    while i >= 1:
        if (str1_align[i]) == '_' and str2_align[i] == '_':
            id = i + 1
            break
        i -= 1

    print("".join(str1_align[id: len(str1_align)]))
    print("".join(str2_align[id: len(str2_align)]))


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


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


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

    s1 = 'AGGGCT'
    s2 = 'AGGCA'
    # AGGGCT
    # A_GGCA
    run_wrapper(s1, s2)
