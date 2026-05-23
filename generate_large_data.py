#!/usr/bin/env python3
"""
Generate LARGE SCALE synthetic data (millions of records)
Optimized for real-time analytics
"""

import os
import csv
from datetime import datetime, timedelta
from faker import Faker
import numpy as np
import pandas as pd
import time

# Configuration - LARGE SCALE
CUSTOMERS = 500_000           # 500K customers
ORDERS = 5_000_000            # 5M orders
ORDER_ITEMS = 15_000_000      # 15M line items
PRODUCTS = 50_000             # 50K products
CAMPAIGNS = 10_000            # 10K campaigns
WEB_EVENTS = 50_000_000       # 50M web events

fake = Faker()
Faker.seed(42)
np.random.seed(42)

output_dir = os.path.join(os.path.dirname(__file__), 'dataforge', 'data', 'raw')
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("DATAFORGE LARGE SCALE DATA GENERATOR")
print("=" * 80)
print(f"\nTarget Scale:")
print(f"  Customers:     {CUSTOMERS:>15,}")
print(f"  Orders:        {ORDERS:>15,}")
print(f"  Order Items:   {ORDER_ITEMS:>15,}")
print(f"  Products:      {PRODUCTS:>15,}")
print(f"  Campaigns:     {CAMPAIGNS:>15,}")
print(f"  Web Events:    {WEB_EVENTS:>15,}")
print(f"\nTotal Records: ~{(CUSTOMERS + ORDERS + ORDER_ITEMS + PRODUCTS + CAMPAIGNS + WEB_EVENTS):,}")
print("\n" + "=" * 80 + "\n")

start_time = time.time()

# 1. Generate Customers (batch writing for memory efficiency)
print("[1/6] Generating customers...")
customer_start = time.time()
with open(os.path.join(output_dir, 'customers.csv'), 'w', newline='', buffering=10000) as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'email', 'first_name', 'last_name', 'country', 'tier', 'created_at'])
    writer.writeheader()

    batch_size = 10000
    for batch_start in range(0, CUSTOMERS, batch_size):
        batch_end = min(batch_start + batch_size, CUSTOMERS)
        for i in range(batch_start, batch_end):
            customer_id = i + 1
            tier = np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], p=[0.5, 0.3, 0.15, 0.05])
            created_at = fake.date_time_between(start_date='-5y')
            writer.writerow({
                'customer_id': customer_id,
                'email': fake.email() if np.random.random() > 0.02 else None,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'country': fake.country_code(),
                'tier': tier,
                'created_at': created_at.isoformat(),
            })

        if (batch_end - batch_start) % (batch_size * 5) == 0:
            elapsed = time.time() - customer_start
            rate = batch_end / elapsed
            print(f"  {batch_end:>10,} / {CUSTOMERS:>10,} ({batch_end*100//CUSTOMERS:>3}%) - {rate:>8,.0f} rows/sec")

print(f"  [OK] {CUSTOMERS:,} customers in {time.time() - customer_start:.1f}s\n")

# 2. Generate Products (simpler, smaller)
print("[2/6] Generating products...")
product_start = time.time()
with open(os.path.join(output_dir, 'products.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'category', 'price', 'cost', 'active'])
    writer.writeheader()
    for i in range(PRODUCTS):
        product_id = i + 1
        category = np.random.choice(['Electronics', 'Apparel', 'Books', 'Home', 'Sports', 'Food', 'Beauty', 'Toys'])
        writer.writerow({
            'product_id': product_id,
            'name': fake.word().title() + ' ' + np.random.choice(['Pro', 'Classic', 'Max', 'Lite', '']).strip(),
            'category': category,
            'price': round(np.random.gamma(2, 50) + 5, 2),
            'cost': round(np.random.gamma(2, 25) + 2, 2),
            'active': np.random.choice([True, False], p=[0.9, 0.1]),
        })

        if (i + 1) % 10000 == 0:
            print(f"  {i+1:>10,} / {PRODUCTS:>10,}")

print(f"  [OK] {PRODUCTS:,} products in {time.time() - product_start:.1f}s\n")

# 3. Generate Campaigns
print("[3/6] Generating campaigns...")
campaign_start = time.time()
with open(os.path.join(output_dir, 'campaigns.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['campaign_id', 'name', 'channel', 'budget', 'start_date', 'end_date'])
    writer.writeheader()
    for i in range(CAMPAIGNS):
        campaign_id = i + 1
        start_date = fake.date_between(start_date='-3y')
        writer.writerow({
            'campaign_id': campaign_id,
            'name': f"{np.random.choice(['Summer', 'Winter', 'Spring', 'Fall'])} {np.random.choice(['Sale', 'Promo', 'Launch'])} {fake.year()}",
            'channel': np.random.choice(['Email', 'Social', 'Display', 'Search', 'Organic', 'Paid', 'Affiliate']),
            'budget': round(np.random.gamma(2, 5000), 2),
            'start_date': start_date.isoformat(),
            'end_date': (start_date + timedelta(days=30)).isoformat(),
        })

        if (i + 1) % 2000 == 0:
            print(f"  {i+1:>10,} / {CAMPAIGNS:>10,}")

print(f"  [OK] {CAMPAIGNS:,} campaigns in {time.time() - campaign_start:.1f}s\n")

# 4. Generate Orders (large batch)
print("[4/6] Generating orders...")
order_start = time.time()
with open(os.path.join(output_dir, 'orders.csv'), 'w', newline='', buffering=50000) as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'customer_id', 'order_date', 'total_amount', 'status', 'payment_method'])
    writer.writeheader()

    batch_size = 50000
    for batch_start in range(0, ORDERS, batch_size):
        batch_end = min(batch_start + batch_size, ORDERS)
        for i in range(batch_start, batch_end):
            order_id = i + 1
            customer_id = np.random.randint(1, CUSTOMERS + 1)
            order_date = fake.date_time_between(start_date='-4y', end_date='now')
            writer.writerow({
                'order_id': order_id,
                'customer_id': customer_id,
                'order_date': order_date.isoformat(),
                'total_amount': round(np.random.gamma(2, 100) + 10, 2),
                'status': np.random.choice(['Completed', 'Pending', 'Cancelled', 'Refunded'], p=[0.8, 0.1, 0.05, 0.05]),
                'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Debit Card', 'Apple Pay']),
            })

        if (batch_end - batch_start) % (batch_size * 2) == 0:
            elapsed = time.time() - order_start
            rate = batch_end / elapsed
            print(f"  {batch_end:>15,} / {ORDERS:>15,} ({batch_end*100//ORDERS:>3}%) - {rate:>10,.0f} rows/sec")

print(f"  [OK] {ORDERS:,} orders in {time.time() - order_start:.1f}s\n")

# 5. Generate Order Items (very large)
print("[5/6] Generating order items...")
order_item_start = time.time()
with open(os.path.join(output_dir, 'order_items.csv'), 'w', newline='', buffering=100000) as f:
    writer = csv.DictWriter(f, fieldnames=['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'discount_amount'])
    writer.writeheader()

    item_id = 1
    batch_size = 100000
    items_in_batch = 0
    batch_start_time = time.time()

    for order_id in range(1, min(ORDERS + 1, ORDERS // 3) + 1):  # avg 3 items per order
        num_items = np.random.randint(1, 6)
        for _ in range(num_items):
            if item_id > ORDER_ITEMS:
                break
            writer.writerow({
                'order_item_id': item_id,
                'order_id': order_id,
                'product_id': np.random.randint(1, PRODUCTS + 1),
                'quantity': np.random.randint(1, 10),
                'unit_price': round(np.random.gamma(2, 50) + 5, 2),
                'discount_amount': round(np.random.gamma(1, 2), 2) if np.random.random() > 0.7 else 0,
            })
            item_id += 1
            items_in_batch += 1

        if items_in_batch >= batch_size:
            elapsed = time.time() - batch_start_time
            rate = items_in_batch / elapsed
            print(f"  {item_id-1:>15,} / {ORDER_ITEMS:>15,} ({(item_id-1)*100//ORDER_ITEMS:>3}%) - {rate:>10,.0f} rows/sec")
            items_in_batch = 0
            batch_start_time = time.time()

        if item_id > ORDER_ITEMS:
            break

print(f"  [OK] {item_id-1:,} order items in {time.time() - order_item_start:.1f}s\n")

# 6. Generate Web Events (massive scale, sampled)
print("[6/6] Generating web events...")
event_start = time.time()
with open(os.path.join(output_dir, 'web_events.csv'), 'w', newline='', buffering=100000) as f:
    writer = csv.DictWriter(f, fieldnames=['event_id', 'customer_id', 'event_type', 'product_id', 'campaign_id', 'event_date', 'session_duration_seconds'])
    writer.writeheader()

    batch_size = 100000
    for i in range(min(WEB_EVENTS, 100_000_000)):  # Cap at 100M for speed
        event_date = fake.date_time_between(start_date='-2y', end_date='now')
        writer.writerow({
            'event_id': i + 1,
            'customer_id': np.random.randint(1, CUSTOMERS + 1),
            'event_type': np.random.choice(['page_view', 'add_to_cart', 'purchase', 'checkout', 'wishlist', 'search', 'filter'], p=[0.4, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02]),
            'product_id': np.random.randint(1, PRODUCTS + 1) if np.random.random() > 0.2 else None,
            'campaign_id': np.random.randint(1, CAMPAIGNS + 1) if np.random.random() > 0.8 else None,
            'event_date': event_date.isoformat(),
            'session_duration_seconds': np.random.randint(0, 3600),
        })

        if (i + 1) % batch_size == 0:
            elapsed = time.time() - event_start
            rate = (i + 1) / elapsed
            print(f"  {i+1:>15,} / 100,000,000 ({(i+1)*100//100_000_000:>3}%) - {rate:>10,.0f} rows/sec")

final_events = min(WEB_EVENTS, 100_000_000)
print(f"  [OK] {final_events:,} web events in {time.time() - event_start:.1f}s\n")

total_time = time.time() - start_time
total_records = CUSTOMERS + PRODUCTS + CAMPAIGNS + ORDERS + (item_id - 1) + final_events

print("=" * 80)
print("DATA GENERATION COMPLETE!")
print("=" * 80)
print(f"\nTotal Records Generated: {total_records:,}")
print(f"Total Time: {total_time:.1f}s ({total_records/total_time:,.0f} rows/sec)")
print(f"\nData Location: {output_dir}")
print("\nFiles created:")
print(f"  - customers.csv        ({CUSTOMERS:>12,} rows)")
print(f"  - products.csv         ({PRODUCTS:>12,} rows)")
print(f"  - campaigns.csv        ({CAMPAIGNS:>12,} rows)")
print(f"  - orders.csv           ({ORDERS:>12,} rows)")
print(f"  - order_items.csv      ({item_id-1:>12,} rows)")
print(f"  - web_events.csv       ({final_events:>12,} rows)")
print("\n" + "=" * 80)
