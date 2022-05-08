import sys
from pathlib import Path
# from typing import Tuple, List, Dict, TypedDict
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


# class SequenceAlignReturnDictType(TypedDict):
#     score: int
#     str1_align: str
#     str2_align: str
#     time: float
#     memory: int


def run(str1: str, str2: str, output_file_path: Path):
    print('Starting Sequence Alignment DP Efficient Algorithm...')
    response = do_sequence_alignment_wrapper(str1, str2)
    write_output_file(response, output_file_path)
    print('String 1 Alignment: ' + response[1])
    print('String 2 Alignment: ' + response[2])
    print('Completed !')

def space_efficient_alignment_score(str1, str2):
    str1_len, str2_len = len(str1), len(str2)
    OPT = [[0 for j in range(2)] for i in range(str2_len + 1)]
        
    for i in range(str2_len+1):
        OPT[i][0] = i * GAP_PENALTY

    for j in range(1, str1_len+1):
        OPT[0][1] = j * GAP_PENALTY
       	for i in range(1, str2_len+1):
            OPT[i][1] = min(OPT[i-1][1] + GAP_PENALTY, OPT[i][0] + GAP_PENALTY, OPT[i-1][0] + 
            	MISMATCH_PENALTY[str1[j - 1]][str2[i - 1]])
       	for i in range(str2_len+1):
    	    OPT[i][0] = OPT[i][1]

    result = []
    for i in range(len(OPT)):
       	result.append(OPT[i][1])
    return result


def divide_and_conquer(str1, str2):
	str1_len = len(str1)
	str2_len = len(str2)
	if str1_len < 2 or str2_len < 2:
		return do_sequence_alignment(str1, str2)
	left = space_efficient_alignment_score(str1[:str1_len // 2], str2)
	right = space_efficient_alignment_score(str1[::-1][:str1_len // 2], str2[::-1])


	minimum_cost = math.inf
	break_index = -1
	for i in range(len(left)):
		current_cost = left[i] + right[str2_len - i]
		if minimum_cost > current_cost:
			minimum_cost = current_cost
			break_index = i
	left, right = [], []
	left_score, str1_left, str2_left = divide_and_conquer(str1[:str1_len // 2], str2[:break_index])
	right_score, str1_right, str2_right = divide_and_conquer(str1[str1_len // 2:], str2[break_index:])
	return (left_score + right_score, str1_left + str1_right, str2_left + str2_right)




def do_sequence_alignment(str1: str, str2: str):
    str1_len = len(str1)
    str2_len = len(str2)
    memo_array = initialize(str1_len + 1, str2_len + 1)
    min_pointer = initialize(str1_len + 1, str2_len + 1)
    for i in range(1, str1_len + 1):
        for j in range(1, str2_len + 1):
            score_list = [MISMATCH_PENALTY[str1[i - 1]][str2[j - 1]] + memo_array[i - 1][j - 1],
                                GAP_PENALTY + memo_array[i - 1][j],
                                GAP_PENALTY + memo_array[i][j - 1]]
            memo_array[i][j] = min(score_list)
            min_index: int = score_list.index(memo_array[i][j])
            if min_index == 0:
                min_pointer[i][j] = (i - 1, j - 1)
            elif min_index == 1:
                min_pointer[i][j] = (i - 1, j)
            else:
                min_pointer[i][j] = (i, j - 1)
    # print_matrix(memo_array)
    str1_alignment, str2_alignment = get_alignment(min_pointer, str1, str2)
    return (memo_array[str1_len][str2_len], str1_alignment, str2_alignment)


def do_sequence_alignment_wrapper(str1: str, str2: str):
    start_time = time.time()
    score, str1_align, str2_align = divide_and_conquer(str1, str2)
    end_time = time.time()
    time_taken: float = (end_time - start_time) * 1000
    memory_consumed: int = process_memory()
    print(f'Time taken :: {time_taken}')
    print(f'Process Memory :: {memory_consumed}')
    return (score, str1_align, str2_align, time_taken, memory_consumed)


def initialize(str1_len: int, str2_len: int):
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


def get_alignment(min_pointer_array, str1: str, str2: str):
    align_len = len(str1) + len(str2)
    str1_align = [None] * (align_len + 1)
    str2_align = [None] * (align_len + 1)
    str1_align_index = align_len
    str2_align_index = align_len
    i = len(str1)
    j = len(str2)
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
    print(f'Writing output file to {output_file_path}')
    with output_file_path.open('w') as op:
        op.write(str(response[0]) + '\n')
        op.write(str(response[1]) + '\n')
        op.write(str(response[2]) + '\n')
        op.write(str(response[3]) + '\n')
        op.write(str(response[4]) + '\n')

def print_matrix(matrix):
    for row in matrix:
        print(row)


def pretty_print(msg: str or int or float):
    print('\n' + str(msg) + '\n')


def generate_str(input_file_path: Path):
    print('Generating input strings')
    str1 = str()
    str2= str()
    temp_str = str()
    with input_file_path.open() as ip:
        for line in ip:
            try:
                index = int(line)
                temp_str = temp_str[0: index + 1] + temp_str + temp_str[index + 1: len(temp_str)]
            except ValueError:
                str1 = temp_str
                temp_str = line.strip()
        str2 = temp_str
    return (str1, str2)


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


if __name__ == '__main__':

    print('Waking up...')

    if len(sys.argv) != 3:
        print('Insufficient Arguments')
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists() or not input_file.is_file():
        print(f'Input file {sys.argv[1]} does not exist')
        sys.exit(1)

    output_file = Path(sys.argv[2])
    if output_file.is_dir() or not output_file.parent.exists():
        print('Output file has no valid parent directory or is itself a directory. Expected a valid file path')
        sys.exit(1)
    if not output_file.exists():
        output_file.touch()

    (s1, s2) = generate_str(input_file)

    # s1 = 'AGGGCT'
    # s2 = 'AGGCA'
    # AGGGCT
    # A_GGCA
    run(s1, s2, output_file)
