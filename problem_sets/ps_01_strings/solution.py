# PS-01: String Manipulation
# Target: 30-45 minutes for all 5 problems

from re import S


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
    new_s=''.join(c for c in s if c.isalnum())
    if new_s.lower() == new_s.lower()[::-1]:
        return True
    else:
        return False


def count_vowels(s: str) -> dict:
    """
    Count occurrences of each vowel (a, e, i, o, u).
    Case-insensitive, return lowercase keys.
    Always return all 5 vowels in the dict.
    """
    d = dict()
    vowels = list("aeiou")
    for v in vowels:
        d[v]=0
    for c in s.lower():
        if c in d.keys():
            d[c]=d[c]+1
    return d


def interleave(s1: str, s2: str) -> str:
    """
    Interleave two strings character by character.
    If one is longer, append the remaining characters.
    """
    len1=len(s1)
    len2=len(s2)
    min_len=min(len1,len2)
    s=""
    for i in range(min_len):
        s=s+s1[i]+s2[i]
    s=s+s1[min_len:]
    s=s+s2[min_len:]
    return s


def compress(s: str) -> str:
    """
    Compress string using counts of consecutive repeated characters.
    Only compress if it saves space (return original if compressed is longer or equal).
    """
                            
    if not s:                                                                                                                                           
        return s                                                                                                                                        
                                                                                                                                                          
    result = []                                                                                                                                         
    count = 1                                                                                                                                           
                                                                                                                                                          
    for i in range(1, len(s)):                                                                                                                          
        if s[i] == s[i-1]:                                                                                                                              
            count += 1                                                                                                                                  
        else:                                                                                                                                           
            result.append(s[i-1] + str(count))                                                                                                          
            count = 1                                                                                                                                   
                                                                                                                                                          
    # Don't forget the last run                                                                                                                         
    result.append(s[-1] + str(count))                                                                                                                   
                                                                                                                                                          
    compressed = ''.join(result)
    return compressed if len(compressed)<len(s) else s

