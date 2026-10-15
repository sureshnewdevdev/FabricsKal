import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from src.sales_loader import load_sales


class SalesLoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "sales.csv"

    def write_csv(self, text):
        self.path.write_text(text, encoding="utf-8")
        return self.path

    def test_valid_records_keep_order_and_exact_total(self):
        self.write_csv("order_id,order_date,amount\nO1,2026-10-01,0.10\nO2,2026-10-02,0.20\n")
        records = load_sales(self.path)
        self.assertEqual([r["order_id"] for r in records], ["O1", "O2"])
        self.assertEqual(records[0]["order_date"], date(2026, 10, 1))
        self.assertEqual(sum((r["amount"] for r in records), Decimal("0")), Decimal("0.30"))
        self.assertIsInstance(records[0]["amount"], Decimal)

    def test_utf8_bom(self):
        self.write_csv("\ufefforder_id,order_date,amount\nO1,2026-10-01,100\n")
        self.assertEqual(len(load_sales(self.path)), 1)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_sales(self.path)

    def test_missing_headers(self):
        self.write_csv("order_id,order_date\nO1,2026-10-01\n")
        with self.assertRaisesRegex(ValueError, "Missing required"):
            load_sales(self.path)

    def test_duplicate_headers(self):
        self.write_csv("order_id,order_date,amount,amount\nO1,2026-10-01,1,1\n")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            load_sales(self.path)

    def test_incorrect_field_count(self):
        for row in ["O1,2026-10-01,100,extra", "O1,2026-10-01"]:
            with self.subTest(row=row):
                self.write_csv("order_id,order_date,amount\n" + row + "\n")
                with self.assertRaisesRegex(ValueError, "Line 2: incorrect field count"):
                    load_sales(self.path)

    def test_blank_order_id(self):
        self.write_csv("order_id,order_date,amount\n ,2026-10-01,100\n")
        with self.assertRaisesRegex(ValueError, "Line 2: blank order_id"):
            load_sales(self.path)

    def test_invalid_dates(self):
        for value in ["01/10/2026", "2026-1-01", "2026-02-30", ""]:
            with self.subTest(value=value):
                self.write_csv(f"order_id,order_date,amount\nO1,{value},100\n")
                with self.assertRaisesRegex(ValueError, "Line 2:"):
                    load_sales(self.path)

    def test_invalid_amounts(self):
        for value in ["0", "-10", "abc", "NaN", "Infinity", "-Infinity", ""]:
            with self.subTest(value=value):
                self.write_csv(f"order_id,order_date,amount\nO1,2026-10-01,{value}\n")
                with self.assertRaisesRegex(ValueError, "Line 2:"):
                    load_sales(self.path)

    def test_input_is_not_modified(self):
        self.write_csv("order_id,order_date,amount\nO1,2026-10-01,100\n")
        before = self.path.read_bytes()
        load_sales(self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_bad_later_row_fails_instead_of_skipping(self):
        self.write_csv("order_id,order_date,amount\nO1,2026-10-01,100\nO2,2026-10-02,-1\n")
        with self.assertRaisesRegex(ValueError, "Line 3:"):
            load_sales(self.path)


if __name__ == "__main__":
    unittest.main()
