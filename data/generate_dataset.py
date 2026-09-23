"""
Synthetic Superstore Sales Dataset Generator
=============================================
Generates a realistic sales dataset modeled after the Kaggle Superstore Sales dataset.
This synthetic data is created for educational/internship demonstration purposes.

Original dataset reference:
    Kaggle: https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset

The generated data mimics the structure and statistical properties of real
retail superstore data but is entirely computer-generated.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ── Reproducibility ─────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Reference data ───────────────────────────────────────────────────────────
CATEGORIES = {
    "Technology": {
        "sub_categories": ["Phones", "Computers", "Accessories", "Copiers"],
        "products": {
            "Phones": [
                ("Apple iPhone 14 Pro", 999.99),
                ("Samsung Galaxy S23", 799.99),
                ("Google Pixel 7", 599.99),
                ("OnePlus 11", 699.99),
                ("Motorola Edge 40", 449.99),
            ],
            "Computers": [
                ("Dell XPS 15 Laptop", 1499.99),
                ("Apple MacBook Air M2", 1299.99),
                ("HP Spectre x360", 1199.99),
                ("Lenovo ThinkPad X1 Carbon", 1399.99),
                ("Microsoft Surface Pro 9", 1099.99),
            ],
            "Accessories": [
                ("Logitech MX Master 3 Mouse", 99.99),
                ("Sony WH-1000XM5 Headphones", 349.99),
                ("Anker USB-C Hub", 49.99),
                ("Belkin Wireless Charger", 39.99),
                ("SanDisk 1TB External SSD", 129.99),
            ],
            "Copiers": [
                ("Canon imageCLASS MF743Cdw", 599.99),
                ("HP LaserJet Pro M454dw", 449.99),
                ("Brother HL-L2350DW", 249.99),
                ("Epson EcoTank ET-4850", 349.99),
                ("Xerox B215 Multifunction", 299.99),
            ],
        },
    },
    "Furniture": {
        "sub_categories": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "products": {
            "Chairs": [
                ("Herman Miller Aeron Chair", 1499.99),
                ("Steelcase Leap V2 Chair", 1299.99),
                ("IKEA Markus Office Chair", 229.99),
                ("Hon Ignition 2.0 Chair", 499.99),
                ("Serta Big & Tall Chair", 349.99),
            ],
            "Tables": [
                ("IKEA Bekant Sit-Stand Desk", 549.99),
                ("Autonomous SmartDesk Pro", 699.99),
                ("Flexispot E7 Standing Desk", 529.99),
                ("Realspace Magellan Desk", 299.99),
                ("Bush Business Furniture Desk", 349.99),
            ],
            "Bookcases": [
                ("IKEA Billy Bookcase", 149.99),
                ("Bush Business 5-Shelf Bookcase", 249.99),
                ("Sauder Barrister Lane Bookcase", 199.99),
                ("Prepac Elite 6-Shelf Bookcase", 179.99),
                ("Ameriwood Home Logan Bookcase", 159.99),
            ],
            "Furnishings": [
                ("Uplift Monitor Arm", 129.99),
                ("3M Anti-Fatigue Mat", 79.99),
                ("Quartet Magnetic Whiteboard", 89.99),
                ("Rubbermaid Storage Cabinet", 199.99),
                ("Fellowes Shredder", 149.99),
            ],
        },
    },
    "Office Supplies": {
        "sub_categories": ["Binders", "Paper", "Art", "Envelopes", "Labels", "Fasteners", "Supplies", "Storage"],
        "products": {
            "Binders": [
                ("Avery Heavy Duty Binder", 12.99),
                ("Cardinal Slant-D Ring Binder", 9.99),
                ("Wilson Jones Ultra Duty Binder", 14.99),
                ("Mead 3-Ring Binder", 7.99),
                ("Staples Better 3-Ring Binder", 8.99),
            ],
            "Paper": [
                ("Hammermill Copy Plus Paper (500 sheets)", 8.99),
                ("HP Premium24 Copy Paper (500 sheets)", 9.99),
                ("Staples Multiuse Copy Paper (5-ream)", 39.99),
                ("Georgia-Pacific Spectrum Paper", 7.99),
                ("Boise Aspen Multipurpose Paper", 8.49),
            ],
            "Art": [
                ("Prismacolor Premier Colored Pencils 72pk", 39.99),
                ("Crayola Classic Markers 64pk", 14.99),
                ("Faber-Castell Watercolor Set", 24.99),
                ("Sharpie Permanent Markers 36pk", 19.99),
                ("Pilot G2 Pens 20pk", 22.99),
            ],
            "Envelopes": [
                ("Quality Park #10 Envelopes 500ct", 19.99),
                ("Staples Security Envelopes 100ct", 12.99),
                ("Mead Peel & Seal Envelopes 150ct", 16.99),
                ("Columbian Kraft Envelopes 100ct", 14.99),
                ("Avery Printable Envelopes 100ct", 18.99),
            ],
            "Labels": [
                ("Avery Easy Peel Labels 750ct", 29.99),
                ("ULINE Shipping Labels 500ct", 24.99),
                ("Dymo LabelWriter Labels 260ct", 19.99),
                ("Avery Mailing Labels 100ct", 12.99),
                ("Office Depot Name Badge Labels", 14.99),
            ],
            "Fasteners": [
                ("Swingline Stapler Kit", 24.99),
                ("3M Scotch Tape Dispenser 6pk", 14.99),
                ("Acco Binder Clips Assorted 200ct", 12.99),
                ("Swingline Standard Staples 5000ct", 9.99),
                ("Advantus Rubber Bands 100ct", 6.99),
            ],
            "Supplies": [
                ("Post-it Notes 12pk 3x3", 15.99),
                ("Expo Low-Odor Dry Erase Markers", 12.99),
                ("Quartet Cork Bulletin Board", 34.99),
                ("Scotch Thermal Laminator", 39.99),
                ("Fellowes Desktop Organizer", 29.99),
            ],
            "Storage": [
                ("Sterilite 6-Drawer Desktop Storage", 49.99),
                ("mDesign Desk Organizer Set", 34.99),
                ("Bankers Box Strength Storage Box 12pk", 39.99),
                ("AmazonBasics Filing Cabinet", 89.99),
                ("Storex Plastic File Crate", 24.99),
            ],
        },
    },
}

REGIONS = {
    "East": ["New York", "Boston", "Philadelphia", "Baltimore", "Washington DC",
             "Newark", "Hartford", "Providence", "Albany", "Bridgeport"],
    "West": ["Los Angeles", "San Francisco", "Seattle", "Portland", "Las Vegas",
             "Phoenix", "Denver", "Salt Lake City", "Sacramento", "San Diego"],
    "Central": ["Chicago", "Dallas", "Houston", "Minneapolis", "Kansas City",
                "St. Louis", "Milwaukee", "Indianapolis", "Columbus", "Louisville"],
    "South": ["Miami", "Atlanta", "Charlotte", "Nashville", "New Orleans",
              "Tampa", "Orlando", "Jacksonville", "Richmond", "Memphis"],
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "COD", "Online Transfer", "Cheque"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

# ── Helper functions ──────────────────────────────────────────────────────────

def random_date(start_year: int = 2021, end_year: int = 2023) -> datetime:
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def get_seasonal_multiplier(month: int) -> float:
    """Sales are higher in Nov-Dec (holiday) and Mar-Apr (spring)."""
    multipliers = {
        1: 0.75, 2: 0.78, 3: 0.92, 4: 0.95,
        5: 0.88, 6: 0.85, 7: 0.87, 8: 0.90,
        9: 0.93, 10: 0.97, 11: 1.20, 12: 1.35,
    }
    return multipliers.get(month, 1.0)


def generate_record(order_id: int, customer_map: dict) -> dict:
    # ── Order date & shipping ──
    order_date = random_date()
    ship_days = {"Standard Class": random.randint(4, 7),
                 "Second Class": random.randint(2, 4),
                 "First Class": random.randint(1, 2),
                 "Same Day": 0}
    ship_mode = random.choice(SHIP_MODES)
    ship_date = order_date + timedelta(days=ship_days[ship_mode])

    # ── Customer ──
    customer_id = f"CUST-{random.randint(1, 1500):04d}"
    if customer_id not in customer_map:
        first = random.choice(["James", "Mary", "John", "Patricia", "Robert",
                               "Jennifer", "Michael", "Linda", "William", "Barbara",
                               "David", "Susan", "Richard", "Jessica", "Joseph",
                               "Sarah", "Thomas", "Karen", "Charles", "Lisa",
                               "Priya", "Rohan", "Ananya", "Vikram", "Sneha",
                               "Arjun", "Pooja", "Rahul", "Neha", "Amit"])
        last = random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown",
                              "Davis", "Miller", "Wilson", "Moore", "Taylor",
                              "Anderson", "Thomas", "Jackson", "White", "Harris",
                              "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                              "Patel", "Shah", "Kumar", "Singh", "Sharma",
                              "Gupta", "Verma", "Mehta", "Joshi", "Nair"])
        customer_map[customer_id] = f"{first} {last}"
    customer_name = customer_map[customer_id]

    segment = random.choice(SEGMENTS)
    region = random.choice(list(REGIONS.keys()))
    state = random.choice(REGIONS[region])

    # ── Product ──
    category = random.choice(list(CATEGORIES.keys()))
    sub_cat = random.choice(CATEGORIES[category]["sub_categories"])
    available_products = CATEGORIES[category]["products"].get(sub_cat, [])
    product_name, base_price = random.choice(available_products)

    # ── Quantity & discount ──
    quantity = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8],
                                p=[0.38, 0.25, 0.16, 0.09, 0.05, 0.03, 0.02, 0.02])
    discount = random.choice([0.0, 0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50])

    # Seasonal uplift
    month = order_date.month
    seasonal = get_seasonal_multiplier(month)
    price_variation = np.random.uniform(0.92, 1.08)
    unit_price = round(base_price * price_variation, 2)

    sales = round(unit_price * quantity * (1 - discount) * seasonal, 2)

    # ── Profit (category-dependent margins) ──
    base_margins = {
        "Technology": 0.22,
        "Furniture": 0.10,
        "Office Supplies": 0.30,
    }
    margin = base_margins[category] * np.random.uniform(0.6, 1.4)
    # High discounts eat into profit
    profit = round(sales * margin * (1 - discount * 0.8), 2)

    payment = random.choice(PAYMENT_METHODS)

    return {
        "Order_ID": f"ORD-{order_id:05d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Ship_Date": ship_date.strftime("%Y-%m-%d"),
        "Ship_Mode": ship_mode,
        "Customer_ID": customer_id,
        "Customer_Name": customer_name,
        "Segment": segment,
        "Region": region,
        "State": state,
        "Category": category,
        "Sub_Category": sub_cat,
        "Product_Name": product_name,
        "Quantity": int(quantity),
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "Payment_Method": payment,
    }


def generate_dataset(n_records: int = 10000) -> pd.DataFrame:
    print(f"Generating {n_records} synthetic sales records...")
    customer_map = {}
    records = [generate_record(i + 1, customer_map) for i in range(n_records)]
    df = pd.DataFrame(records)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    df.sort_values("Order_Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"Dataset generated: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "sales_data.csv")
    df = generate_dataset(10000)
    df.to_csv(out_path, index=False)
    print(f"Saved to: {out_path}")
    print(df.head())
    print(df.dtypes)
