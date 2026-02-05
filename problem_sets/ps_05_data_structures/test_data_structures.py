"""
PS-05: Data Structures Tests
"""
import unittest
from solution import valid_parentheses, MinStack, reverse_linked_list, ListNode, SortedList, RecentCounter


# Helper to create linked list from array
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head


# Helper to convert linked list to array
def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


class TestDataStructures(unittest.TestCase):

    # ===== valid_parentheses =====

    def test_parentheses_simple(self):
        self.assertTrue(valid_parentheses("()"))

    def test_parentheses_multiple(self):
        self.assertTrue(valid_parentheses("()[]{}"))

    def test_parentheses_mismatch(self):
        self.assertFalse(valid_parentheses("(]"))

    def test_parentheses_interleaved_bad(self):
        self.assertFalse(valid_parentheses("([)]"))

    def test_parentheses_nested(self):
        self.assertTrue(valid_parentheses("{[]}"))

    def test_parentheses_empty(self):
        self.assertTrue(valid_parentheses(""))

    def test_parentheses_unclosed(self):
        self.assertFalse(valid_parentheses("("))

    # ===== MinStack =====

    def test_minstack_basic(self):
        ms = MinStack()
        ms.push(-2)
        ms.push(0)
        ms.push(-3)
        self.assertEqual(ms.get_min(), -3)
        ms.pop()
        self.assertEqual(ms.top(), 0)
        self.assertEqual(ms.get_min(), -2)

    def test_minstack_single(self):
        ms = MinStack()
        ms.push(5)
        self.assertEqual(ms.top(), 5)
        self.assertEqual(ms.get_min(), 5)

    def test_minstack_decreasing(self):
        ms = MinStack()
        ms.push(3)
        ms.push(2)
        ms.push(1)
        self.assertEqual(ms.get_min(), 1)
        ms.pop()
        self.assertEqual(ms.get_min(), 2)
        ms.pop()
        self.assertEqual(ms.get_min(), 3)

    # ===== reverse_linked_list =====

    def test_reverse_basic(self):
        head = create_list([1, 2, 3])
        new_head = reverse_linked_list(head)
        self.assertEqual(list_to_array(new_head), [3, 2, 1])

    def test_reverse_single(self):
        head = create_list([1])
        new_head = reverse_linked_list(head)
        self.assertEqual(list_to_array(new_head), [1])

    def test_reverse_empty(self):
        new_head = reverse_linked_list(None)
        self.assertIsNone(new_head)

    def test_reverse_two(self):
        head = create_list([1, 2])
        new_head = reverse_linked_list(head)
        self.assertEqual(list_to_array(new_head), [2, 1])

    # ===== SortedList =====

    def test_sorted_list_insert(self):
        sl = SortedList()
        sl.insert(5)
        sl.insert(2)
        sl.insert(8)
        self.assertEqual(sl.get_all(), [2, 5, 8])

    def test_sorted_list_remove(self):
        sl = SortedList()
        sl.insert(5)
        sl.insert(2)
        sl.insert(8)
        self.assertTrue(sl.remove(5))
        self.assertEqual(sl.get_all(), [2, 8])

    def test_sorted_list_remove_not_found(self):
        sl = SortedList()
        sl.insert(1)
        self.assertFalse(sl.remove(5))

    def test_sorted_list_range(self):
        sl = SortedList()
        sl.insert(1)
        sl.insert(3)
        sl.insert(5)
        sl.insert(7)
        self.assertEqual(sl.count_range(2, 6), 2)  # 3 and 5

    def test_sorted_list_range_empty(self):
        sl = SortedList()
        sl.insert(1)
        sl.insert(10)
        self.assertEqual(sl.count_range(3, 5), 0)

    def test_sorted_list_duplicates(self):
        sl = SortedList()
        sl.insert(3)
        sl.insert(3)
        sl.insert(3)
        self.assertEqual(sl.get_all(), [3, 3, 3])
        self.assertEqual(sl.count_range(3, 3), 3)

    # ===== RecentCounter =====

    def test_recent_counter_basic(self):
        rc = RecentCounter()
        self.assertEqual(rc.ping(1), 1)
        self.assertEqual(rc.ping(100), 2)
        self.assertEqual(rc.ping(3001), 3)
        self.assertEqual(rc.ping(3002), 3)

    def test_recent_counter_spaced(self):
        rc = RecentCounter()
        self.assertEqual(rc.ping(1), 1)
        self.assertEqual(rc.ping(4000), 1)  # t=1 is outside [1000, 4000]
        self.assertEqual(rc.ping(7000), 2)  # t=4000 is inside [4000, 7000] (inclusive)

    def test_recent_counter_dense(self):
        rc = RecentCounter()
        self.assertEqual(rc.ping(1), 1)
        self.assertEqual(rc.ping(2), 2)
        self.assertEqual(rc.ping(3), 3)
        self.assertEqual(rc.ping(3000), 4)
        self.assertEqual(rc.ping(3001), 5)  # t=1 is inside [1, 3001] (inclusive)


if __name__ == '__main__':
    unittest.main()
