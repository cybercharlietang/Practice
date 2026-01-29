# Mock Assessment 001: Ticket Booking System

**Time Limit: 90 minutes**
**Format: Progressive levels (ICA-style)**
**All levels build on the same class**

---

## Overview

You are implementing a ticket booking system for a small venue. The venue has a fixed number of seats, and customers can book tickets for events on specific dates.

Solving this task consists of several levels. Subsequent levels build on previous ones. You must maintain backward compatibility — all previous level tests must still pass.

**You are not required to provide the most efficient implementation. Any code that passes the unit tests is sufficient.**

---

## Level 1: Basic Booking Operations
*Target: 10-15 minutes*

Implement a `TicketSystem` class with the following:

### Constructor
`__init__(self, venue_capacity: int)` — Initialize the system with the venue's total seat capacity.

### Methods

`book(self, event_date: str, customer_id: str, num_tickets: int) -> bool`
- Attempt to book `num_tickets` for `customer_id` on `event_date`
- `event_date` is in format "YYYY-MM-DD"
- Return `True` if booking succeeds (enough seats available for that date)
- Return `False` if not enough seats available
- A customer can have multiple bookings for the same event

`cancel(self, event_date: str, customer_id: str) -> int`
- Cancel ALL bookings for `customer_id` on `event_date`
- Return the total number of tickets that were cancelled
- Return `0` if no bookings found

### Examples

```
system = TicketSystem(100)
system.book("2024-03-15", "alice", 2)    # returns True (98 seats left)
system.book("2024-03-15", "bob", 50)     # returns True (48 seats left)
system.book("2024-03-15", "alice", 3)    # returns True (45 seats left, alice now has 5)
system.book("2024-03-15", "charlie", 50) # returns False (only 45 available)
system.cancel("2024-03-15", "alice")     # returns 5 (alice's 2 + 3)
system.cancel("2024-03-15", "alice")     # returns 0 (no bookings)
```

---

## Level 2: Query Operations
*Target: 20-30 minutes*

Add the following query methods:

`get_available_seats(self, event_date: str) -> int`
- Return the number of available seats for `event_date`
- If no bookings exist for that date, return full capacity

`get_customer_bookings(self, customer_id: str) -> dict[str, int]`
- Return a dictionary mapping `event_date` to total tickets booked by this customer
- Only include dates where the customer has active bookings
- Return empty dict if customer has no bookings

`get_top_customers(self, event_date: str, n: int) -> list[tuple[str, int]]`
- Return the top `n` customers by tickets booked for `event_date`
- Return as list of tuples: `[(customer_id, ticket_count), ...]`
- Sort by ticket count descending, then by customer_id ascending for ties
- If fewer than `n` customers, return all of them

### Examples

```
system = TicketSystem(100)
system.book("2024-03-15", "alice", 10)
system.book("2024-03-15", "bob", 20)
system.book("2024-03-15", "alice", 5)
system.book("2024-03-20", "alice", 8)

system.get_available_seats("2024-03-15")      # returns 65
system.get_available_seats("2024-03-25")      # returns 100 (no bookings)

system.get_customer_bookings("alice")         # returns {"2024-03-15": 15, "2024-03-20": 8}
system.get_customer_bookings("unknown")       # returns {}

system.get_top_customers("2024-03-15", 2)     # returns [("bob", 20), ("alice", 15)]
system.get_top_customers("2024-03-15", 10)    # returns [("bob", 20), ("alice", 15)]
```

---

## Level 3: Waitlist System
*Target: 30-45 minutes*

When a booking fails due to insufficient seats, the customer can be added to a waitlist. When cancellations occur, waitlisted requests should be processed automatically.

Modify `book` and `cancel` behavior and add new methods:

### Modified Methods

`book(self, event_date: str, customer_id: str, num_tickets: int, waitlist: bool = False) -> bool`
- If `waitlist=False`: behave as before
- If `waitlist=True` and booking fails: add to waitlist, return `False`
- A customer can only have ONE waitlist entry per event (subsequent waitlist requests replace the previous one)
- Waitlisted requests are processed FIFO when seats become available

`cancel(self, event_date: str, customer_id: str) -> int`
- After cancellation, automatically process waitlist for that date
- Process waitlist entries in FIFO order
- Only fulfill a waitlist entry if ALL requested tickets can be satisfied
- Skip entries that cannot be fully satisfied (they remain on waitlist)
- Return the number of tickets cancelled (not including auto-fulfilled)

### New Methods

`get_waitlist(self, event_date: str) -> list[tuple[str, int]]`
- Return waitlist entries for `event_date` in FIFO order
- Format: `[(customer_id, num_tickets), ...]`
- Return empty list if no waitlist

`remove_from_waitlist(self, event_date: str, customer_id: str) -> bool`
- Remove customer from waitlist for that date
- Return `True` if removed, `False` if not on waitlist

### Examples

```
system = TicketSystem(50)
system.book("2024-03-15", "alice", 30)                      # True
system.book("2024-03-15", "bob", 25)                        # False (only 20 left)
system.book("2024-03-15", "bob", 25, waitlist=True)         # False (added to waitlist)
system.book("2024-03-15", "charlie", 15, waitlist=True)     # False (added to waitlist)

system.get_waitlist("2024-03-15")    # [("bob", 25), ("charlie", 15)]

system.cancel("2024-03-15", "alice") # returns 30, charlie auto-booked (15 <= 30)
                                      # bob skipped (25 > 30), charlie processed (15 <= 30 remaining after skip)

system.get_waitlist("2024-03-15")    # [("bob", 25)] - charlie fulfilled, bob still waiting
system.get_available_seats("2024-03-15")  # 35 (50 - 15 charlie)
```

---

## Level 4: Revenue Optimization
*Target: 20-30 minutes*

Add a method to find the optimal subset of waitlisted customers to maximize revenue.

`optimize_waitlist(self, event_date: str, ticket_price: int) -> list[str]`
- Given the current available seats and waitlist, find which waitlisted customers to accept to maximize total revenue
- Revenue = number of tickets × ticket_price
- You cannot exceed available seats
- Return list of customer_ids to accept, in any order
- If multiple solutions give same revenue, return any valid one
- This method should NOT modify the system state (simulation only)

### Examples

```
system = TicketSystem(100)
system.book("2024-03-15", "existing", 80)                   # True, 20 seats left
system.book("2024-03-15", "alice", 15, waitlist=True)       # waitlist
system.book("2024-03-15", "bob", 8, waitlist=True)          # waitlist
system.book("2024-03-15", "charlie", 12, waitlist=True)     # waitlist
system.book("2024-03-15", "diana", 7, waitlist=True)        # waitlist

# Available: 20 seats
# Waitlist: alice(15), bob(8), charlie(12), diana(7)
# Options:
#   - alice(15) alone = 15 tickets
#   - bob(8) + charlie(12) = 20 tickets (exceeds capacity - invalid)
#   - bob(8) + diana(7) = 15 tickets
#   - charlie(12) + diana(7) = 19 tickets
#   - charlie(12) + bob(8) > 20 (invalid)
#   - bob(8) + diana(7) = 15 tickets
# Best: charlie(12) + diana(7) = 19 tickets

system.optimize_waitlist("2024-03-15", 50)  # returns ["charlie", "diana"] (or ["diana", "charlie"])
                                             # revenue = 19 * 50 = 950
```

### Constraints
- Waitlist size ≤ 20 entries per event
- Any solution with time complexity not worse than O(2^n) for n waitlist entries will pass

---

## Scoring

- Level 1: 25%
- Level 2: 25%
- Level 3: 30%
- Level 4: 20%

Partial credit is awarded per level based on tests passed.

---

## Hints (read only if stuck)

<details>
<summary>Level 1 Hint</summary>
A dict mapping event_date to another dict of customer_id -> ticket_count works well.
</details>

<details>
<summary>Level 3 Hint</summary>
Use collections.deque for the waitlist. Remember to process it after every cancellation.
</details>

<details>
<summary>Level 4 Hint</summary>
This is the 0/1 knapsack problem. With n ≤ 20, brute force O(2^n) is acceptable, or use DP with O(n × capacity).
</details>
