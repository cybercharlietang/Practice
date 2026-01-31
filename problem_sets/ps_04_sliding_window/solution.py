# PS-04: Sliding Window
# Target: 30-45 minutes for all 5 problems
from collections import Counter
from collections import deque

def max_sum_k(nums: list, k: int) -> int:
    """
    Find maximum sum of k consecutive elements.
    Return 0 if array has fewer than k elements.
    """
    l=len(nums)
    if l < k:
        return 0
    window=nums[:k]
    max_sum=sum(window)
    for i in range(k,l):
        window.pop(0)
        window.append(nums[i])
        value=sum(window)
        max_sum=max(max_sum,value)
    return max_sum


def longest_unique_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    """
    if not s:
        return 0
    l=len(list(s))
    max_length=0
    for i in range(l):
        if i==l:
            print("hello")
            return max(1, max_length)
        unique = set()
        for j in range(i,l):
            if s[j] in unique:
                max_length=max(max_length, len(unique))
                break
            unique.add(s[j])
        max_length=max(max_length, len(unique))
    return max_length
            



def min_window_substring(s: str, t: str) -> str:
    """
    Find minimum window in s that contains all characters of t.
    Return "" if no such window exists.
    """
    all_char = Counter(t)
    l=len(s)
    answer=""
    if t=="":
        return ""
    for right in range(l):
        window=list(s[:right+1])
        while not (all_char-Counter(window)):
            answer="".join(window)
            window.pop(0)
    return answer
        


def subarray_sum_count(nums: list, k: int) -> int:
    """
    Count number of contiguous subarrays that sum to exactly k.
    """
    subarray=[]
    l=len(nums)
    number=0
    for i in range(l):
        subarray=nums[:i+1]
        while subarray:
            if sum(subarray)==k:
                number+=1
            subarray.pop(0)
    return number


def sliding_window_max(nums: list, k: int) -> list:
    """
    Return max element in each window of size k.
    Use deque for O(n) solution.
    """
    max_elems=[]
    window=deque(nums[:k])
    max_elems.append(max(window))
    for i in range(len(nums)-k):
        window.append(nums[k+i])
        window.popleft()
        max_elems.append(max(window))
        print(window)
    return max_elems
