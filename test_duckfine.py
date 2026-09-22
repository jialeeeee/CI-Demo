import unittest

from duckfine import DuckFine


class TestDuckFineCharge(unittest.TestCase):
    def setUp(self):
        self.duck = DuckFine(member_id="member-1")

    def test_zero_days_late_charges_nothing(self):
        fee = self.duck.charge(0)
        self.assertEqual(fee, 0.0)

    def test_days_within_grace_period_charges_nothing(self):
        fee = self.duck.charge(2)
        self.assertEqual(fee, 0.0)

    def test_one_day_late_is_still_within_grace(self):
        fee = self.duck.charge(1)
        self.assertEqual(fee, 0.0)

    def test_charges_daily_fee_for_days_past_grace(self):
        fee = self.duck.charge(3)
        self.assertAlmostEqual(fee, 0.50)

    def test_charges_accumulate_over_multiple_chargeable_days(self):
        fee = self.duck.charge(6)
        self.assertAlmostEqual(fee, 2.00)

    def test_deluxe_doubles_the_fee(self):
        fee = self.duck.charge(3, deluxe=True)
        self.assertAlmostEqual(fee, 1.00)

    def test_deluxe_with_no_chargeable_days_is_still_zero(self):
        fee = self.duck.charge(2, deluxe=True)
        self.assertEqual(fee, 0.0)

    def test_fee_is_capped_at_max_fee(self):
        fee = self.duck.charge(100)
        self.assertAlmostEqual(fee, DuckFine.MAX_FEE)

    def test_deluxe_fee_is_capped_at_max_fee(self):
        fee = self.duck.charge(8, deluxe=True)
        self.assertAlmostEqual(fee, DuckFine.MAX_FEE)

    def test_fee_exactly_at_cap_is_not_reduced(self):
        fee = self.duck.charge(7, deluxe=True)
        self.assertAlmostEqual(fee, DuckFine.MAX_FEE)

    def test_negative_days_late_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.duck.charge(-1)

    def test_negative_days_late_does_not_change_total_owed(self):
        try:
            self.duck.charge(-1)
        except ValueError:
            pass
        self.assertEqual(self.duck.total_owed, 0.0)

    def test_total_owed_starts_at_zero(self):
        self.assertEqual(self.duck.total_owed, 0.0)

    def test_total_owed_accumulates_across_charges(self):
        self.duck.charge(3)
        self.duck.charge(4)
        self.assertAlmostEqual(self.duck.total_owed, 1.50)

    def test_returned_fee_matches_total_owed_after_single_charge(self):
        fee = self.duck.charge(3)
        self.assertAlmostEqual(self.duck.total_owed, fee)

    def test_member_id_is_stored(self):
        self.assertEqual(self.duck.member_id, "member-1")


if __name__ == "__main__":
    unittest.main()
