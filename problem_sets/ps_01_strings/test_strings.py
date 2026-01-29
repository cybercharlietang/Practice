"""
PS-01: String Manipulation Tests
"""
import unittest
from solution import reverse_words, is_palindrome, count_vowels, interleave, compress


class TestStrings(unittest.TestCase):

    # ===== reverse_words =====

    def test_reverse_words_basic(self):
        self.assertEqual(reverse_words("hello world"), "world hello")

    def test_reverse_words_multiple(self):
        self.assertEqual(reverse_words("the sky is blue"), "blue is sky the")

    def test_reverse_words_single(self):
        self.assertEqual(reverse_words("hello"), "hello")

    def test_reverse_words_empty(self):
        self.assertEqual(reverse_words(""), "")

    def test_reverse_words_spaces_only(self):
        # Edge case: how to handle? Assuming return empty or stripped
        result = reverse_words("   ")
        self.assertIn(result, ["", "   "])  # Accept either

    # ===== is_palindrome =====

    def test_palindrome_classic(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))

    def test_palindrome_false(self):
        self.assertFalse(is_palindrome("race a car"))

    def test_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))

    def test_palindrome_single_char(self):
        self.assertTrue(is_palindrome("a"))

    def test_palindrome_with_numbers(self):
        self.assertTrue(is_palindrome("A1B2B1a"))

    def test_palindrome_simple(self):
        self.assertTrue(is_palindrome("racecar"))

    # ===== count_vowels =====

    def test_count_vowels_basic(self):
        result = count_vowels("Hello World")
        self.assertEqual(result, {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0})

    def test_count_vowels_all(self):
        result = count_vowels("AEIOU aeiou")
        self.assertEqual(result, {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2})

    def test_count_vowels_none(self):
        result = count_vowels("xyz")
        self.assertEqual(result, {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0})

    def test_count_vowels_empty(self):
        result = count_vowels("")
        self.assertEqual(result, {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0})

    # ===== interleave =====

    def test_interleave_equal(self):
        self.assertEqual(interleave("abc", "123"), "a1b2c3")

    def test_interleave_first_longer(self):
        self.assertEqual(interleave("abcd", "12"), "a1b2cd")

    def test_interleave_second_longer(self):
        self.assertEqual(interleave("ab", "1234"), "a1b234")

    def test_interleave_first_empty(self):
        self.assertEqual(interleave("", "123"), "123")

    def test_interleave_second_empty(self):
        self.assertEqual(interleave("abc", ""), "abc")

    def test_interleave_both_empty(self):
        self.assertEqual(interleave("", ""), "")

    # ===== compress =====

    def test_compress_basic(self):
        self.assertEqual(compress("aabbbcccc"), "a2b3c4")

    def test_compress_no_benefit(self):
        # "abcd" compressed is "a1b1c1d1" which is longer
        self.assertEqual(compress("abcd"), "abcd")

    def test_compress_single_run(self):
        self.assertEqual(compress("aaa"), "a3")

    def test_compress_empty(self):
        self.assertEqual(compress(""), "")

    def test_compress_single_char(self):
        self.assertEqual(compress("a"), "a")  # "a1" is same length, return original

    def test_compress_no_benefit_mixed(self):
        # "aabba" (5) vs "a2b2a1" (6) -> return original
        self.assertEqual(compress("aabba"), "aabba")

    def test_compress_long_runs(self):
        self.assertEqual(compress("aaaaaaaaaa"), "a10")  # 10 chars -> 3 chars


if __name__ == '__main__':
    unittest.main()
