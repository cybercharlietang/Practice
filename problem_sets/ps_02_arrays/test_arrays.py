"""
PS-02: Array Fundamentals Tests
"""
import unittest
from solution import remove_duplicates, rotate_array, find_missing, merge_sorted, move_zeros


class TestArrays(unittest.TestCase):

    # ===== remove_duplicates =====

    def test_remove_duplicates_basic(self):
        self.assertEqual(remove_duplicates([1, 2, 2, 3, 1, 4]), [1, 2, 3, 4])

    def test_remove_duplicates_all_same(self):
        self.assertEqual(remove_duplicates([1, 1, 1]), [1])

    def test_remove_duplicates_no_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 3]), [1, 2, 3])

    def test_remove_duplicates_empty(self):
        self.assertEqual(remove_duplicates([]), [])

    def test_remove_duplicates_preserves_order(self):
        self.assertEqual(remove_duplicates([3, 1, 2, 1, 3, 2]), [3, 1, 2])

    def test_remove_duplicates_strings(self):
        self.assertEqual(remove_duplicates(['a', 'b', 'a', 'c']), ['a', 'b', 'c'])

    # ===== rotate_array =====

    def test_rotate_basic(self):
        self.assertEqual(rotate_array([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])

    def test_rotate_k_greater_than_length(self):
        self.assertEqual(rotate_array([1, 2, 3], 4), [3, 1, 2])

    def test_rotate_k_zero(self):
        self.assertEqual(rotate_array([1, 2, 3], 0), [1, 2, 3])

    def test_rotate_k_equals_length(self):
        self.assertEqual(rotate_array([1, 2, 3], 3), [1, 2, 3])

    def test_rotate_single_element(self):
        self.assertEqual(rotate_array([1], 100), [1])

    def test_rotate_empty(self):
        self.assertEqual(rotate_array([], 5), [])

    # ===== find_missing =====

    def test_find_missing_middle(self):
        self.assertEqual(find_missing([3, 0, 1]), 2)

    def test_find_missing_end(self):
        self.assertEqual(find_missing([0, 1]), 2)

    def test_find_missing_start(self):
        self.assertEqual(find_missing([1, 2]), 0)

    def test_find_missing_large(self):
        self.assertEqual(find_missing([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)

    def test_find_missing_single(self):
        self.assertEqual(find_missing([0]), 1)

    def test_find_missing_single_alt(self):
        self.assertEqual(find_missing([1]), 0)

    # ===== merge_sorted =====

    def test_merge_sorted_basic(self):
        self.assertEqual(merge_sorted([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])

    def test_merge_sorted_first_empty(self):
        self.assertEqual(merge_sorted([], [1, 2, 3]), [1, 2, 3])

    def test_merge_sorted_second_empty(self):
        self.assertEqual(merge_sorted([1, 2, 3], []), [1, 2, 3])

    def test_merge_sorted_both_empty(self):
        self.assertEqual(merge_sorted([], []), [])

    def test_merge_sorted_with_duplicates(self):
        self.assertEqual(merge_sorted([1, 1, 1], [1, 1]), [1, 1, 1, 1, 1])

    def test_merge_sorted_no_overlap(self):
        self.assertEqual(merge_sorted([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])

    def test_merge_sorted_interleaved(self):
        self.assertEqual(merge_sorted([1, 4, 7], [2, 3, 5, 6, 8]), [1, 2, 3, 4, 5, 6, 7, 8])

    # ===== move_zeros =====

    def test_move_zeros_basic(self):
        self.assertEqual(move_zeros([0, 1, 0, 3, 12]), [1, 3, 12, 0, 0])

    def test_move_zeros_start(self):
        self.assertEqual(move_zeros([0, 0, 1]), [1, 0, 0])

    def test_move_zeros_no_zeros(self):
        self.assertEqual(move_zeros([1, 2, 3]), [1, 2, 3])

    def test_move_zeros_all_zeros(self):
        self.assertEqual(move_zeros([0, 0, 0]), [0, 0, 0])

    def test_move_zeros_empty(self):
        self.assertEqual(move_zeros([]), [])

    def test_move_zeros_single_zero(self):
        self.assertEqual(move_zeros([0]), [0])

    def test_move_zeros_single_nonzero(self):
        self.assertEqual(move_zeros([5]), [5])


if __name__ == '__main__':
    unittest.main()
