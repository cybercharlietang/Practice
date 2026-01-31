"""
PS-04: Sliding Window Tests
"""
import unittest
from solution import max_sum_k, longest_unique_substring, min_window_substring, subarray_sum_count, sliding_window_max


class TestSlidingWindow(unittest.TestCase):

    # ===== max_sum_k =====

    def test_max_sum_k_basic(self):
        self.assertEqual(max_sum_k([1, 4, 2, 10, 2, 3, 1, 0, 20], 4), 24)

    def test_max_sum_k_small(self):
        self.assertEqual(max_sum_k([1, 2, 3], 2), 5)

    def test_max_sum_k_not_enough(self):
        self.assertEqual(max_sum_k([5], 2), 0)

    def test_max_sum_k_exact_size(self):
        self.assertEqual(max_sum_k([1, 2, 3], 3), 6)

    def test_max_sum_k_empty(self):
        self.assertEqual(max_sum_k([], 1), 0)

    def test_max_sum_k_negative(self):
        self.assertEqual(max_sum_k([-1, -2, -3, -4], 2), -3)

    # ===== longest_unique_substring =====

    def test_longest_unique_basic(self):
        self.assertEqual(longest_unique_substring("abcabcbb"), 3)

    def test_longest_unique_all_same(self):
        self.assertEqual(longest_unique_substring("bbbbb"), 1)

    def test_longest_unique_middle(self):
        self.assertEqual(longest_unique_substring("pwwkew"), 3)

    def test_longest_unique_empty(self):
        self.assertEqual(longest_unique_substring(""), 0)

    def test_longest_unique_all_unique(self):
        self.assertEqual(longest_unique_substring("abcdef"), 6)

    def test_longest_unique_single(self):
        self.assertEqual(longest_unique_substring("a"), 1)

    # ===== min_window_substring =====

    def test_min_window_basic(self):
        self.assertEqual(min_window_substring("ADOBECODEBANC", "ABC"), "BANC")

    def test_min_window_exact(self):
        self.assertEqual(min_window_substring("a", "a"), "a")

    def test_min_window_not_enough(self):
        self.assertEqual(min_window_substring("a", "aa"), "")

    def test_min_window_no_match(self):
        self.assertEqual(min_window_substring("abc", "xyz"), "")

    def test_min_window_duplicates_in_t(self):
        self.assertEqual(min_window_substring("aaab", "aab"), "aab")

    def test_min_window_empty_t(self):
        self.assertEqual(min_window_substring("abc", ""), "")

    # ===== subarray_sum_count =====

    def test_subarray_sum_basic(self):
        self.assertEqual(subarray_sum_count([1, 1, 1], 2), 2)

    def test_subarray_sum_multiple(self):
        self.assertEqual(subarray_sum_count([1, 2, 3], 3), 2)

    def test_subarray_sum_with_zero(self):
        self.assertEqual(subarray_sum_count([1, -1, 0], 0), 3)

    def test_subarray_sum_single(self):
        self.assertEqual(subarray_sum_count([3], 3), 1)

    def test_subarray_sum_none(self):
        self.assertEqual(subarray_sum_count([1, 2, 3], 10), 0)

    def test_subarray_sum_negative(self):
        self.assertEqual(subarray_sum_count([1, -1, 1, -1], 0), 4)

    # ===== sliding_window_max =====

    def test_sliding_max_basic(self):
        self.assertEqual(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])

    def test_sliding_max_single_window(self):
        self.assertEqual(sliding_window_max([1], 1), [1])

    def test_sliding_max_k2(self):
        self.assertEqual(sliding_window_max([1, 2, 3, 4], 2), [2, 3, 4])

    def test_sliding_max_decreasing(self):
        self.assertEqual(sliding_window_max([5, 4, 3, 2, 1], 3), [5, 4, 3])

    def test_sliding_max_all_same(self):
        self.assertEqual(sliding_window_max([2, 2, 2, 2], 2), [2, 2, 2])

    def test_sliding_max_k_equals_len(self):
        self.assertEqual(sliding_window_max([1, 2, 3], 3), [3])


if __name__ == '__main__':
    unittest.main()
