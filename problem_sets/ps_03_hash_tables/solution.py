# PS-03: Hash Tables & Counting
# Target: 30-45 minutes for all 5 problems
from collections import defaultdict
from collections import Counter

def two_sum(nums: list, target: int) -> list:
    seen = {}  # value -> index                                                                                                 
                                                                                                                                  
    for i, num in enumerate(nums):                                                                                              
        complement = target - num                                                                                               
                                                                                                                                  
        if complement in seen:                                                                                                  
              # Found it! Return the earlier index first                                                                          
            return [seen[complement], i]                                                                                        
                                                                                                                                  
        # Haven't found pair yet, store this number                                                                             
        seen[num] = i 


def group_anagrams(strs: list) -> list:
    """
    Group strings that are anagrams of each other.
    Return list of groups (order doesn't matter).
    """
    d = defaultdict(list)
    for str in strs:
        d[''.join(sorted(str))].append(str)
    return list(d.values())


def first_unique_char(s: str) -> int:
    """
    Return index of first non-repeating character.
    Return -1 if none exists.
    """
    count = Counter(s)
    if not s:
        return -1
    if min(count.values())>1:
        return -1
    for ix, char in enumerate(list(s)):
        if count[char]==1:
            return ix


def most_frequent(nums: list) -> int:
    """
    Return the element that appears most frequently.
    If tie, return any of them.
    """
    count = Counter(nums)
    max_freq = max(count.values())
    for k, v in count.items():
        if v==max_freq:
            return k
    return None


def is_anagram(s1: str, s2: str) -> bool:
    """
    Check if two strings are anagrams (same characters, same counts).
    """
    if Counter(s1)==Counter(s2):
        return True
    else:
        return False
