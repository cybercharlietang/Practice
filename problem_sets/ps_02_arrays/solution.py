# PS-02: Array Fundamentals
# Target: 30-45 minutes for all 5 problems


def remove_duplicates(arr: list) -> list:
    """
    Remove duplicate elements while preserving original order.
    Return a new list.
    """
    s=set()
    new_list=[]
    for el in arr:
        if el not in s:
            new_list.append(el)
            s.add(el)
    return new_list


def rotate_array(arr: list, k: int) -> list:
    """
    Rotate array to the right by k positions.
    Return a new list.
    """
    if not arr:
        return []
    n=k % len(arr)
    return arr[len(arr)-n:]+arr[:len(arr)-n]


def find_missing(arr: list) -> int:
    """
    Given array containing n distinct numbers from range [0, n],
    find the one that is missing.
    """
    s1=set(range(len(arr)+1))
    s2=set(arr)
    return (s1-s2).pop()


def merge_sorted(arr1: list, arr2: list) -> list:
    """
    Merge two sorted arrays into one sorted array.
    """
    comb=arr1+arr2
    return sorted(comb)


def move_zeros(arr: list) -> list:
    """
    Move all zeros to the end while maintaining relative order
    of non-zero elements. Return a new list.
    """
    l=arr
    for i in l:
        if i == 0:
            l.remove(i)
            l.append(0)
    return l
