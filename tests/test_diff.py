import os
import json
import shutil
import unittest
import xdiff


class TestCompareContent(unittest.TestCase):
    """ tests for core function: compare_content
    """
    def setUp(self):
        sample_string = 'a'
        sample_digit = 1
        sample_float = 1.23
        sample_list = [1]
        sample_dict = {'a': 1}
        sample_tuple = (1,)

        self.all_type_value = [
            sample_string, sample_digit, sample_float, sample_list, sample_dict, sample_tuple
        ]

    def test_equal_value(self):
        """ when the two given values are equal, return None.
        """
        for value1 in self.all_type_value:
            for value2 in self.all_type_value:
                if value1 == value2:
                    self.assertIsNone(xdiff.compare_content(value1, value2))

    def test_different_type(self):
        """ when the two given values are not in the same type, return [origin_data, new_data]
        """
        for value1 in self.all_type_value:
            for value2 in self.all_type_value:
                if value1 != value2:
                    self.assertEqual(xdiff.compare_content(value1, value2), [value1, value2])

    def test_same_type_different_value(self):
        self.assertEqual(
            xdiff.compare_content('a', 'b'),
            ['a', 'b']
        )
        self.assertEqual(
            xdiff.compare_content(1, 3),
            [1, 3]
        )

    def test_two_list(self):
        sample_list_1 = [1, 2, 3]
        sample_list_2 = [1, 2, 4]
        sample_list_3 = [1, 2, 3, 4]
        self.assertEqual(
            xdiff.compare_content(sample_list_1, sample_list_2),
            [[3, 4]]
        )
        self.assertEqual(
            xdiff.compare_content(sample_list_1, sample_list_3),
            [[None, 4]]
        )
        self.assertEqual(
            xdiff.compare_content(sample_list_3, sample_list_2),
            [[3, 4], [4, None]]
        )

    def test_two_dict(self):
        sample_dict_1 = {'a': 1, 'b': 2}
        sample_dict_2 = {'a': 1, 'b': 3}
        sample_dict_3 = {'a': 1, 'b': 2, 'c': 3}
        sample_dict_4 = {'a': 1, 'c': 3}
        self.assertEqual(
            xdiff.compare_content(sample_dict_1, sample_dict_2),
            {'b': [2, 3]}
        )
        self.assertEqual(
            xdiff.compare_content(sample_dict_1, sample_dict_3),
            {'c': [None, 3]}
        )
        self.assertEqual(
            xdiff.compare_content(sample_dict_1, sample_dict_4),
            {'b': [2, None], 'c': [None, 3]}
        )

class TestCompareFiles(unittest.TestCase):
    """ tests for core function: compare_files
    """

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        self.json_file1 = os.path.join(self.data_dir, 'file1.json')
        sample_dict_1 = {'a': 1, 'b': 2}
        with open(self.json_file1, 'w+') as f:
            f.write(json.dumps(sample_dict_1))

        self.json_file2 = os.path.join(self.data_dir, 'file2.json')
        sample_dict_2 = {"a": 1, "b": 2}
        with open(self.json_file2, 'w+') as f:
            f.write(json.dumps(sample_dict_2))

        self.json_file3 = os.path.join(self.data_dir, 'file3.json')
        sample_dict_3 = {"a": 1, "c": 3}
        with open(self.json_file3, 'w+') as f:
            f.write(json.dumps(sample_dict_3))

    def tearDown(self):
        shutil.rmtree(self.data_dir, ignore_errors=True)

    def test_json_files_same(self):
        self.assertIsNone(xdiff.compare_files(self.json_file1, self.json_file2))

    def test_json_files_different(self):
        self.assertEqual(
            xdiff.compare_files(self.json_file1, self.json_file3),
            {'b': [2, None], 'c': [None, 3]}
        )
