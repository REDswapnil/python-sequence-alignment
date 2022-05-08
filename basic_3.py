import sys
from pathlib import Path
import math
import psutil
import time

GAP_PENALTY = 30

MISMATCH_PENALTY = {
    'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
    'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
}


def run(str1: str, str2: str, output_file_path: Path):
    # print('Starting Sequence Alignment DP Basic Algorithm...')
    response = do_sequence_alignment_wrapper(str1, str2)
    write_output_file(response, output_file_path)
    # print('Completed !')


def do_sequence_alignment(str1, str2):
    # print('Performing Sequence Alignment DP Basic Run')
    str1_len = len(str1)
    str2_len = len(str2)
    # # print(f'String 01: {str1} (length - {str1_len}')
    # print(f'String 02: {str2} (length - {str2_len})')
    # print('Initializing memo array...')
    memo_array = initialize(str1_len + 1, str2_len + 1)
    min_pointer = initialize(str1_len + 1, str2_len + 1)
    # print_matrix(memo_array)
    # print('Building memo array ...')
    for i in range(1, str1_len + 1):
        for j in range(1, str2_len + 1):
            score_list = [MISMATCH_PENALTY[str1[i - 1]][str2[j - 1]] + memo_array[i - 1][j - 1],
                                GAP_PENALTY + memo_array[i - 1][j],
                                GAP_PENALTY + memo_array[i][j - 1]]
            # memo_array[i][j] = min(MISMATCH_PENALTY[str1[i - 1]][str2[j - 1]] + memo_array[i - 1][j - 1],
            #                        GAP_PENALTY + memo_array[i - 1][j],
            #                        GAP_PENALTY + memo_array[i][j - 1])
            memo_array[i][j] = min(score_list)
            min_index: int = score_list.index(memo_array[i][j])
            if min_index == 0:
                min_pointer[i][j] = (i - 1, j - 1)
            elif min_index == 1:
                min_pointer[i][j] = (i - 1, j)
            else:
                min_pointer[i][j] = (i, j - 1)
    # print_matrix(memo_array)
    # print_matrix(min_pointer)
    # print(f'Alignment Score :: {memo_array[str1_len][str2_len]}')
    # str1_alignment, str2_alignment = get_alignment(memo_array, str1, str2)
    str1_alignment, str2_alignment = get_alignment(min_pointer, str1, str2)
    # print(f'Str1 Alignment :: {str1_alignment}')
    # print(f'Str2 Alignment :: {str2_alignment}')
    return memo_array[str1_len][str2_len], str1_alignment, str2_alignment


def do_sequence_alignment_wrapper(str1, str2):
    start_time = time.time()
    score, str1_align, str2_align = do_sequence_alignment(str1, str2)
    end_time = time.time()
    time_taken: float = (end_time - start_time) * 1000
    memory_consumed: int = process_memory()
    # print(f'Time taken :: {time_taken}')
    # print(f'Process Memory :: {memory_consumed}')
    return {'score': score, 'str1_align': str1_align, 'str2_align': str2_align, 'time': time_taken,
            'memory': memory_consumed}


def initialize(str1_len, str2_len):
    memo_array = list()
    for i in range(str1_len):
        col = list()
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


def get_alignment(min_pointer_array, str1, str2):
    # print(f'Getting alignment of the 2 strings from the memo array')
    align_len = len(str1) + len(str2)
    str1_align = [None] * (align_len + 1)
    str2_align = [None] * (align_len + 1)
    str1_align_index = align_len
    str2_align_index = align_len
    i: int = len(str1)
    j: int = len(str2)
    while not (i == 0 or j == 0):
        if min_pointer_array[i][j] == (i-1, j-1):
            str1_align[str1_align_index] = str1[i-1]
            str2_align[str2_align_index] = str2[j - 1]
            str1_align_index -= 1
            str2_align_index -= 1
            i -= 1
            j -= 1
        elif min_pointer_array[i][j] == (i-1, j):
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

    str_align_usable_index = 1
    i = align_len
    while i >= 1:
        if (str1_align[i]) == '_' and str2_align[i] == '_':
            str_align_usable_index = i + 1
            break
        i -= 1

    return ("".join(str1_align[str_align_usable_index: len(str1_align)]),
            "".join(str2_align[str_align_usable_index: len(str2_align)]))


def write_output_file(response, output_file_path: Path):
    # print(f'Writing output file to {output_file_path}')
    with output_file_path.open('w') as op:
        op.write(str(response.get('score')) + '\n')
        op.write(str(response.get('str1_align')) + '\n')
        op.write(str(response.get('str2_align')) + '\n')
        op.write(str(response.get('time')) + '\n')
        op.write(str(response.get('memory')) + '\n')


def print_matrix(matrix):
    for row in matrix:
        print(row)


# def pretty_print(msg: str | int | float):
#     print('\n' + str(msg) + '\n')


def generate_str(input_file_path: Path):
    # print('Generating input strings')
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


def process_memory() -> int:
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


if __name__ == '__main__':

    # print('Waking up...')

    if len(sys.argv) != 3:
        # print('Insufficient Arguments')
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists() or not input_file.is_file():
        # print(f'Input file {sys.argv[1]} does not exist')
        sys.exit(1)

    output_file = Path(sys.argv[2])
    if output_file.is_dir() or not output_file.parent.exists():
        # print('Output file has no valid parent directory or is itself a directory. Expected a valid file path')
        sys.exit(1)
    if not output_file.exists():
        output_file.touch()

    (s1, s2) = generate_str(input_file)

    run(s1, s2, output_file)
