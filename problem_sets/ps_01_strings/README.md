# PS-01: String Manipulation

**Target Time:** 30-45 minutes for all 5 problems
**Goal:** Speed and accuracy on basic string operations

---

## Problems

### 1. reverse_words(s: str) -> str
Reverse the order of words in a sentence. Words are separated by single spaces.

```
"hello world" → "world hello"
"the sky is blue" → "blue is sky the"
"  " → ""
```

---

### 2. is_palindrome(s: str) -> bool
Check if string is a palindrome, ignoring case and non-alphanumeric characters.

```
"A man, a plan, a canal: Panama" → True
"race a car" → False
"" → True
```

---

### 3. count_vowels(s: str) -> dict
Count occurrences of each vowel (a, e, i, o, u). Case-insensitive, return lowercase keys.

```
"Hello World" → {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}
"AEIOU aeiou" → {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}
```

---

### 4. interleave(s1: str, s2: str) -> str
Interleave two strings character by character. If one is longer, append the remaining characters.

```
"abc", "123" → "a1b2c3"
"ab", "1234" → "a1b234"
"hello", "" → "hello"
```

---

### 5. compress(s: str) -> str
Compress string using counts of consecutive repeated characters. Only compress if it saves space.

```
"aabbbcccc" → "a2b3c4"
"abcd" → "abcd"  (compressed "a1b1c1d1" is longer)
"aaa" → "a3"
"" → ""
```

---

## Running Tests

```bash
cd problem_sets/ps_01_strings
python -m pytest test_strings.py -v
```

Or run a single test:
```bash
python -m pytest test_strings.py::TestStrings::test_reverse_words -v
```
