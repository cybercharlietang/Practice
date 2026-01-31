"""
PS-03: Hash Tables & Counting Tests
"""
import unittest
from solution import two_sum, group_anagrams, first_unique_char, most_frequent, is_anagram


class TestHashTables(unittest.TestCase):

    # ===== two_sum =====

    def test_two_sum_basic(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_two_sum_middle(self):
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])

    def test_two_sum_duplicates(self):
        self.assertEqual(two_sum([3, 3], 6), [0, 1])

    def test_two_sum_negative(self):
        self.assertEqual(two_sum([-1, -2, -3, -4, -5], -8), [2, 4])

    def test_two_sum_mixed(self):
        self.assertEqual(two_sum([1, -2, 3, 4], 2), [1, 3])

    # ===== group_anagrams =====

    def test_group_anagrams_basic(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Convert to sets of frozensets for order-independent comparison
        result_sets = set(frozenset(group) for group in result)
        expected_sets = {frozenset(["eat", "tea", "ate"]), frozenset(["tan", "nat"]), frozenset(["bat"])}
        self.assertEqual(result_sets, expected_sets)

    def test_group_anagrams_empty_string(self):
        result = group_anagrams([""])
        self.assertEqual(result, [[""]])

    def test_group_anagrams_single(self):
        result = group_anagrams(["a"])
        self.assertEqual(result, [["a"]])

    def test_group_anagrams_no_anagrams(self):
        result = group_anagrams(["abc", "def", "ghi"])
        result_sets = set(frozenset(group) for group in result)
        expected_sets = {frozenset(["abc"]), frozenset(["def"]), frozenset(["ghi"])}
        self.assertEqual(result_sets, expected_sets)

    def test_group_anagrams_all_same(self):
        result = group_anagrams(["ab", "ba", "ab"])
        result_sets = set(frozenset(group) for group in result)
        # All are anagrams of each other
        self.assertEqual(len(result), 1)
        self.assertEqual(sorted(result[0]), ["ab", "ab", "ba"])

    # ===== first_unique_char =====

    def test_first_unique_basic(self):
        self.assertEqual(first_unique_char("leetcode"), 0)

    def test_first_unique_middle(self):
        self.assertEqual(first_unique_char("loveleetcode"), 2)

    def test_first_unique_none(self):
        self.assertEqual(first_unique_char("aabb"), -1)

    def test_first_unique_empty(self):
        self.assertEqual(first_unique_char(""), -1)

    def test_first_unique_single(self):
        self.assertEqual(first_unique_char("a"), 0)

    def test_first_unique_last(self):
        self.assertEqual(first_unique_char("aabbccd"), 6)

    # ===== most_frequent =====

    def test_most_frequent_basic(self):
        self.assertEqual(most_frequent([1, 3, 2, 1, 4, 1]), 1)

    def test_most_frequent_tie(self):
        result = most_frequent([1, 2, 2, 3, 3])
        self.assertIn(result, [2, 3])

    def test_most_frequent_single(self):
        self.assertEqual(most_frequent([5]), 5)

    def test_most_frequent_all_same(self):
        self.assertEqual(most_frequent([7, 7, 7]), 7)

    def test_most_frequent_negative(self):
        self.assertEqual(most_frequent([-1, -1, 2, 3]), -1)

    # ===== is_anagram =====

    def test_is_anagram_true(self):
        self.assertTrue(is_anagram("anagram", "nagaram"))

    def test_is_anagram_false(self):
        self.assertFalse(is_anagram("rat", "car"))

    def test_is_anagram_listen_silent(self):
        self.assertTrue(is_anagram("listen", "silent"))

    def test_is_anagram_empty(self):
        self.assertTrue(is_anagram("", ""))

    def test_is_anagram_different_lengths(self):
        self.assertFalse(is_anagram("abc", "abcd"))

    def test_is_anagram_same_letters_different_counts(self):
        self.assertFalse(is_anagram("aaab", "aab"))


if __name__ == '__main__':
    unittest.main()
