import unittest
from pathlib import Path

from basic_3 import do_sequence_alignment_wrapper as basic_seq_align_wrapper, generate_str
from efficient_3 import do_sequence_alignment_wrapper as efficient_seq_align_wrapper


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.input_file_path = 'SampleTestCases/input{}.txt'
        self.output_file_path = 'SampleTestCases/output{}.txt'
        self.datapoints_input_file_path = 'datapoints/in{}.txt'

    def test_basic_algo_sample_testcases(self):
        print('Running testcases for basic sequence alignment code')
        counter: int = 1
        input_file_formatted_path = self.input_file_path.format(counter)
        input_file_path = Path(input_file_formatted_path)
        while input_file_path.exists():
            print(f'Running testcase #{counter}')
            (s1, s2) = generate_str(input_file_path)
            response = basic_seq_align_wrapper(s1, s2)
            output_file_formatted_path = self.output_file_path.format(counter)
            output_file_path = Path(output_file_formatted_path)
            with output_file_path.open() as op:
                self.assertEqual(op.readline().strip(), str(response.get('score')))
                # self.assertEqual(op.readline().strip(), response.get('str1_align'))
                # self.assertEqual(op.readline().strip(), response.get('str2_align'))
            counter += 1
            input_file_formatted_path = self.input_file_path.format(counter)
            input_file_path = Path(input_file_formatted_path)

    def test_efficient_algo_sample_testcases(self):
        print('Running testcases for efficient sequence alignment code')
        counter: int = 1
        input_file_formatted_path = self.input_file_path.format(counter)
        input_file_path = Path(input_file_formatted_path)
        while input_file_path.exists():
            print(f'Running testcase #{counter}')
            (s1, s2) = generate_str(input_file_path)
            response = efficient_seq_align_wrapper(s1, s2)
            output_file_formatted_path = self.output_file_path.format(counter)
            output_file_path = Path(output_file_formatted_path)
            with output_file_path.open() as op:
                self.assertEqual(op.readline().strip(), str(response[0]))
                # self.assertEqual(op.readline().strip(), response.get('str1_align'))
                # self.assertEqual(op.readline().strip(), response.get('str2_align'))
            counter += 1
            input_file_formatted_path = self.input_file_path.format(counter)
            input_file_path = Path(input_file_formatted_path)

    def test_basic_efficient_same_output_datapoints(self):
        print('Running testcases for datapoints to match basic and efficient algorithm outputs')
        counter: int = 1
        input_file_formatted_path = self.datapoints_input_file_path.format(counter)
        input_file_path = Path(input_file_formatted_path)
        while input_file_path.exists():
            print(f'Running testcase #{counter}')
            (s1, s2) = generate_str(input_file_path)
            basic_response = basic_seq_align_wrapper(s1, s2)
            efficient_response = efficient_seq_align_wrapper(s1, s2)
            self.assertEqual(str(basic_response.get('score')), str(efficient_response[0]))
            counter += 1
            input_file_formatted_path = self.datapoints_input_file_path.format(counter)
            input_file_path = Path(input_file_formatted_path)


if __name__ == '__main__':

    unittest.main()
