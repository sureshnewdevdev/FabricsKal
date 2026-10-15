import csv
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED_COLUMNS = {"order_id", "order_date", "amount"}


def load_sales(csv_path: Path) -> list[dict]:
    csv_path = Path(csv_path)
    records = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate CSV headers")
        if not REQUIRED_COLUMNS.issubset(headers):
            raise ValueError("Missing required CSV headers")
        for row in reader:
            line_number = reader.line_num
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Line {line_number}: incorrect field count")
            order_id = row["order_id"].strip()
            order_date = row["order_date"].strip()
            amount_text = row["amount"].strip()
            if not order_id:
                raise ValueError(f"Line {line_number}: blank order_id")
            if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", order_date) is None:
                raise ValueError(f"Line {line_number}: date must use YYYY-MM-DD")
            try:
                parsed_date = date.fromisoformat(order_date)
            except ValueError:
                raise ValueError(f"Line {line_number}: invalid calendar date") from None
            try:
                amount = Decimal(amount_text)
            except InvalidOperation:
                raise ValueError(f"Line {line_number}: invalid amount") from None
            if not amount.is_finite() or amount <= 0:
                raise ValueError(f"Line {line_number}: amount must be finite and positive")
            records.append({
                "order_id": order_id,
                "order_date": parsed_date,
                "amount": amount,
            })
    return records


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    sales = load_sales(project_root / "data" / "sales.csv")
    total_amount = sum((row["amount"] for row in sales), Decimal("0"))
    print(f"Loaded records: {len(sales)}")
    print(f"Total amount (INR): {total_amount:.2f}")
