# PS-01: String Manipulation
# Target: 30-45 minutes for all 5 problems


from audioop import reverse


def reverse_words(s: str) -> str:
    """
    Reverse the order of words in a sentence.
    Words are separated by single spaces.
    """
    s_reverse=s.split(" ")[::-1]
    return ' '.join(s_reverse)

def is_palindrome(s: str) -> bool:
    """
    Check if string is a palindrome.
    Ignore case and non-alphanumeric characters.
    """
    print(s[::-1])


def count_vowels(s: str) -> dict:
    """
    Count occurrences of each vowel (a, e, i, o, u).
    Case-insensitive, return lowercase keys.
    Always return all 5 vowels in the dict.
    """
    # TODO: Implement
    pass


def interleave(s1: str, s2: str) -> str:
    """
    Interleave two strings character by character.
    If one is longer, append the remaining characters.
    """
    # TODO: Implement
    pass


def compress(s: str) -> str:
    """
    Compress string using counts of consecutive repeated characters.
    Only compress if it saves space (return original if compressed is longer or equal).
    """
    # TODO: Implement
    pass
