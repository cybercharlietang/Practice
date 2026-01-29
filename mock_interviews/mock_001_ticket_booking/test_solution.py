"""
Unit tests for Mock Assessment 001: Ticket Booking System

Run with: python -m pytest test_solution.py -v
Run single level: python -m pytest test_solution.py -v -k "Level1"
"""

import pytest
from solution import TicketSystem


# ==================== LEVEL 1 TESTS ====================

class TestLevel1:
    """Basic booking operations"""

    def test_book_simple(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 2) == True

    def test_book_multiple_customers(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 2) == True
        assert system.book("2024-03-15", "bob", 50) == True

    def test_book_same_customer_multiple_times(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 2) == True
        assert system.book("2024-03-15", "alice", 3) == True

    def test_book_exceeds_capacity(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 60) == True
        assert system.book("2024-03-15", "bob", 50) == False

    def test_book_exact_capacity(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 100) == True
        assert system.book("2024-03-15", "bob", 1) == False

    def test_book_different_dates_independent(self):
        system = TicketSystem(50)
        assert system.book("2024-03-15", "alice", 40) == True
        assert system.book("2024-03-16", "bob", 40) == True  # different date

    def test_cancel_existing_booking(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 5)
        assert system.cancel("2024-03-15", "alice") == 5

    def test_cancel_multiple_bookings_same_customer(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 2)
        system.book("2024-03-15", "alice", 3)
        assert system.cancel("2024-03-15", "alice") == 5

    def test_cancel_nonexistent_booking(self):
        system = TicketSystem(100)
        assert system.cancel("2024-03-15", "alice") == 0

    def test_cancel_already_cancelled(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 5)
        system.cancel("2024-03-15", "alice")
        assert system.cancel("2024-03-15", "alice") == 0

    def test_cancel_frees_seats(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 60)
        assert system.book("2024-03-15", "bob", 50) == False
        system.cancel("2024-03-15", "alice")
        assert system.book("2024-03-15", "bob", 50) == True

    def test_book_zero_tickets(self):
        system = TicketSystem(100)
        assert system.book("2024-03-15", "alice", 0) == True


# ==================== LEVEL 2 TESTS ====================

class TestLevel2:
    """Query operations"""

    def test_get_available_seats_full_capacity(self):
        system = TicketSystem(100)
        assert system.get_available_seats("2024-03-15") == 100

    def test_get_available_seats_after_bookings(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 30)
        system.book("2024-03-15", "bob", 20)
        assert system.get_available_seats("2024-03-15") == 50

    def test_get_available_seats_after_cancel(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 30)
        system.cancel("2024-03-15", "alice")
        assert system.get_available_seats("2024-03-15") == 100

    def test_get_customer_bookings_single_event(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        assert system.get_customer_bookings("alice") == {"2024-03-15": 10}

    def test_get_customer_bookings_multiple_events(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        system.book("2024-03-20", "alice", 5)
        assert system.get_customer_bookings("alice") == {"2024-03-15": 10, "2024-03-20": 5}

    def test_get_customer_bookings_accumulates(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        system.book("2024-03-15", "alice", 5)
        assert system.get_customer_bookings("alice") == {"2024-03-15": 15}

    def test_get_customer_bookings_after_cancel(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        system.book("2024-03-20", "alice", 5)
        system.cancel("2024-03-15", "alice")
        assert system.get_customer_bookings("alice") == {"2024-03-20": 5}

    def test_get_customer_bookings_unknown_customer(self):
        system = TicketSystem(100)
        assert system.get_customer_bookings("unknown") == {}

    def test_get_top_customers_basic(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        system.book("2024-03-15", "bob", 20)
        result = system.get_top_customers("2024-03-15", 2)
        assert result == [("bob", 20), ("alice", 10)]

    def test_get_top_customers_fewer_than_n(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 10)
        result = system.get_top_customers("2024-03-15", 5)
        assert result == [("alice", 10)]

    def test_get_top_customers_tie_breaker(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "charlie", 10)
        system.book("2024-03-15", "alice", 10)
        system.book("2024-03-15", "bob", 10)
        result = system.get_top_customers("2024-03-15", 3)
        assert result == [("alice", 10), ("bob", 10), ("charlie", 10)]

    def test_get_top_customers_no_bookings(self):
        system = TicketSystem(100)
        result = system.get_top_customers("2024-03-15", 5)
        assert result == []

    def test_get_top_customers_limit(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 30)
        system.book("2024-03-15", "bob", 20)
        system.book("2024-03-15", "charlie", 10)
        result = system.get_top_customers("2024-03-15", 2)
        assert result == [("alice", 30), ("bob", 20)]


# ==================== LEVEL 3 TESTS ====================

class TestLevel3:
    """Waitlist system"""

    def test_waitlist_basic(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 40)
        assert system.book("2024-03-15", "bob", 20, waitlist=True) == False
        assert system.get_waitlist("2024-03-15") == [("bob", 20)]

    def test_waitlist_fifo_order(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 40)
        system.book("2024-03-15", "bob", 20, waitlist=True)
        system.book("2024-03-15", "charlie", 15, waitlist=True)
        assert system.get_waitlist("2024-03-15") == [("bob", 20), ("charlie", 15)]

    def test_waitlist_replace_existing(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 40)
        system.book("2024-03-15", "bob", 20, waitlist=True)
        system.book("2024-03-15", "bob", 5, waitlist=True)  # replaces
        assert system.get_waitlist("2024-03-15") == [("bob", 5)]

    def test_waitlist_no_waitlist_flag(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 40)
        assert system.book("2024-03-15", "bob", 20, waitlist=False) == False
        assert system.get_waitlist("2024-03-15") == []

    def test_waitlist_auto_process_on_cancel(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 30)
        system.book("2024-03-15", "bob", 15, waitlist=True)
        cancelled = system.cancel("2024-03-15", "alice")
        assert cancelled == 30
        assert system.get_waitlist("2024-03-15") == []
        assert system.get_available_seats("2024-03-15") == 35  # 50 - 15

    def test_waitlist_skip_too_large(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 30)
        system.book("2024-03-15", "bob", 25, waitlist=True)
        system.book("2024-03-15", "charlie", 15, waitlist=True)
        system.cancel("2024-03-15", "alice")  # 30 seats freed
        # bob(25) skipped, charlie(15) fulfilled
        assert system.get_waitlist("2024-03-15") == [("bob", 25)]
        assert system.get_available_seats("2024-03-15") == 35

    def test_waitlist_process_multiple(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 80)
        system.book("2024-03-15", "bob", 10, waitlist=True)
        system.book("2024-03-15", "charlie", 5, waitlist=True)
        system.book("2024-03-15", "diana", 3, waitlist=True)
        system.cancel("2024-03-15", "alice")  # 80 freed
        # bob(10), charlie(5), diana(3) all fulfilled = 18
        assert system.get_waitlist("2024-03-15") == []
        assert system.get_available_seats("2024-03-15") == 82

    def test_remove_from_waitlist_exists(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "alice", 40)
        system.book("2024-03-15", "bob", 20, waitlist=True)
        assert system.remove_from_waitlist("2024-03-15", "bob") == True
        assert system.get_waitlist("2024-03-15") == []

    def test_remove_from_waitlist_not_exists(self):
        system = TicketSystem(50)
        assert system.remove_from_waitlist("2024-03-15", "bob") == False

    def test_waitlist_empty_date(self):
        system = TicketSystem(100)
        assert system.get_waitlist("2024-03-15") == []

    def test_book_success_no_waitlist(self):
        system = TicketSystem(100)
        # Even with waitlist=True, successful booking should NOT add to waitlist
        assert system.book("2024-03-15", "alice", 10, waitlist=True) == True
        assert system.get_waitlist("2024-03-15") == []


# ==================== LEVEL 4 TESTS ====================

class TestLevel4:
    """Revenue optimization"""

    def test_optimize_basic(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "existing", 80)
        system.book("2024-03-15", "alice", 15, waitlist=True)
        system.book("2024-03-15", "bob", 8, waitlist=True)
        system.book("2024-03-15", "charlie", 12, waitlist=True)
        system.book("2024-03-15", "diana", 7, waitlist=True)
        # Available: 20, options: alice(15), bob(8)+diana(7)=15, charlie(12)+diana(7)=19, charlie(12)+bob(8)=20 exceeds
        result = system.optimize_waitlist("2024-03-15", 50)
        total = sum(t for c, t in system.get_waitlist("2024-03-15") if c in result)
        assert total == 19  # charlie + diana

    def test_optimize_single_best(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "existing", 40)
        system.book("2024-03-15", "alice", 10, waitlist=True)
        system.book("2024-03-15", "bob", 5, waitlist=True)
        # Available: 10, alice(10) is optimal
        result = system.optimize_waitlist("2024-03-15", 100)
        assert result == ["alice"]

    def test_optimize_combine_small(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "existing", 40)
        system.book("2024-03-15", "alice", 8, waitlist=True)
        system.book("2024-03-15", "bob", 3, waitlist=True)
        system.book("2024-03-15", "charlie", 4, waitlist=True)
        # Available: 10, alice(8) = 8, bob(3)+charlie(4)=7, alice+bob=11>10, best = alice(8) or bob+charlie=7
        # Wait, alice(8) < bob+charlie=7? No 8 > 7. Best is alice
        # But alice+bob = 11 > 10, alice + charlie = 12 > 10
        result = system.optimize_waitlist("2024-03-15", 10)
        assert "alice" in result
        assert len(result) == 1

    def test_optimize_empty_waitlist(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "alice", 50)
        result = system.optimize_waitlist("2024-03-15", 100)
        assert result == []

    def test_optimize_none_fit(self):
        system = TicketSystem(50)
        system.book("2024-03-15", "existing", 48)
        system.book("2024-03-15", "alice", 10, waitlist=True)
        system.book("2024-03-15", "bob", 5, waitlist=True)
        # Available: 2, neither fits
        result = system.optimize_waitlist("2024-03-15", 100)
        assert result == []

    def test_optimize_does_not_modify_state(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "existing", 80)
        system.book("2024-03-15", "alice", 10, waitlist=True)
        system.optimize_waitlist("2024-03-15", 50)
        # Waitlist should be unchanged
        assert system.get_waitlist("2024-03-15") == [("alice", 10)]
        assert system.get_available_seats("2024-03-15") == 20

    def test_optimize_all_fit(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "existing", 50)
        system.book("2024-03-15", "alice", 10, waitlist=True)
        system.book("2024-03-15", "bob", 15, waitlist=True)
        system.book("2024-03-15", "charlie", 20, waitlist=True)
        # Available: 50, all fit (10+15+20=45)
        result = system.optimize_waitlist("2024-03-15", 100)
        assert set(result) == {"alice", "bob", "charlie"}

    def test_optimize_exact_capacity(self):
        system = TicketSystem(100)
        system.book("2024-03-15", "existing", 80)
        system.book("2024-03-15", "alice", 10, waitlist=True)
        system.book("2024-03-15", "bob", 10, waitlist=True)
        # Available: 20, both fit exactly
        result = system.optimize_waitlist("2024-03-15", 50)
        assert set(result) == {"alice", "bob"}
