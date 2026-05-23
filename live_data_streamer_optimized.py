#!/usr/bin/env python3
"""
Optimized Live Data Streamer - PRODUCTION READY
Continuous order and event generation with zero downtime
"""
import duckdb
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta, timezone
import time

fake = Faker()
Faker.seed(42)
np.random.seed(42)

db_path = "dataforge/dataforge.duckdb"

print("\n" + "=" * 80)
print("LIVE DATA STREAMER - OPTIMIZED VERSION")
print("=" * 80)
print("Continuous real-time data generation")
print("=" * 80 + "\n")

# Get max IDs from initial connection
conn = duckdb.connect(db_path)
conn.execute("PRAGMA threads=4")
customer_count = conn.execute("SELECT MAX(customer_id) FROM raw.customers").fetchone()[0] or 50000
product_count = conn.execute("SELECT MAX(product_id) FROM raw.products").fetchone()[0] or 1000
campaign_count = conn.execute("SELECT MAX(campaign_id) FROM raw.campaigns").fetchone()[0] or 100

last_order_id = conn.execute("SELECT MAX(order_id) FROM raw.orders").fetchone()[0] or 0
last_item_id = conn.execute("SELECT MAX(order_item_id) FROM raw.order_items").fetchone()[0] or 0
last_event_id = conn.execute("SELECT MAX(event_id) FROM raw.web_events").fetchone()[0] or 0
conn.close()

print(f"Starting from: Orders={last_order_id:,}, Items={last_item_id:,}, Events={last_event_id:,}\n")

cycle = 0
total_orders = 0
total_items = 0
total_events = 0

print("=" * 80)
print("STREAMING ACTIVE - Press Ctrl+C to stop")
print("=" * 80 + "\n")

try:
    while True:
        cycle += 1
        cycle_start = time.time()

        print(f"[CYCLE {cycle}] {datetime.now().strftime('%H:%M:%S')} - ", end="", flush=True)

        # Generate orders (25-40 per cycle for 10-second refresh)
        num_orders = np.random.randint(25, 40)
        orders_list = []
        items_list = []

        for i in range(num_orders):
            last_order_id += 1
            customer_id = np.random.randint(1, customer_count + 1)
            order_date = datetime.now(timezone.utc) - timedelta(seconds=np.random.randint(0, 60))

            orders_list.append({
                'order_id': last_order_id,
                'customer_id': customer_id,
                'order_date': order_date.isoformat(),
                'total_amount': round(np.random.gamma(2, 100) + 10, 2),
                'status': np.random.choice(['Completed', 'Pending', 'Cancelled'], p=[0.85, 0.10, 0.05]),
                'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Debit Card', 'Apple Pay']),
            })

            # Items per order
            num_items = np.random.randint(1, 5)
            for _ in range(num_items):
                last_item_id += 1
                items_list.append({
                    'order_item_id': last_item_id,
                    'order_id': last_order_id,
                    'product_id': np.random.randint(1, product_count + 1),
                    'quantity': np.random.randint(1, 10),
                    'unit_price': round(np.random.gamma(2, 50) + 5, 2),
                    'discount_amount': round(np.random.gamma(1, 2), 2) if np.random.random() > 0.7 else 0,
                })

        # Generate events (80-150 per cycle)
        num_events = np.random.randint(80, 150)
        events_list = []

        for i in range(num_events):
            last_event_id += 1
            event_date = datetime.now(timezone.utc) - timedelta(seconds=np.random.randint(0, 60))
            events_list.append({
                'event_id': last_event_id,
                'customer_id': np.random.randint(1, customer_count + 1),
                'event_type': np.random.choice(['page_view', 'add_to_cart', 'purchase', 'checkout', 'wishlist', 'search', 'filter'],
                                              p=[0.4, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02]),
                'product_id': np.random.randint(1, product_count + 1) if np.random.random() > 0.2 else None,
                'campaign_id': np.random.randint(1, campaign_count + 1) if np.random.random() > 0.85 else None,
                'event_date': event_date.isoformat(),
                'session_duration_seconds': np.random.randint(0, 3600),
            })

        # Open connection with retry (dashboard might be reading)
        conn = None
        for retry in range(5):
            try:
                conn = duckdb.connect(db_path)
                conn.execute("PRAGMA threads=4")
                break
            except:
                if retry < 4:
                    time.sleep(0.5)
                else:
                    raise

        if orders_list:
            orders_df = pd.DataFrame(orders_list)
            conn.execute("INSERT INTO raw.orders SELECT * FROM orders_df")
            total_orders += len(orders_list)

        if items_list:
            items_df = pd.DataFrame(items_list)
            conn.execute("INSERT INTO raw.order_items SELECT * FROM items_df")
            total_items += len(items_list)

        if events_list:
            events_df = pd.DataFrame(events_list)
            conn.execute("INSERT INTO raw.web_events SELECT * FROM events_df")
            total_events += len(events_list)

        conn.close()

        cycle_time = time.time() - cycle_start

        print(f"DONE ({cycle_time:.2f}s)")
        print(f"  Orders: {num_orders:>3} | Items: {len(items_list):>4} | Events: {num_events:>3}")
        print(f"  Totals - Orders: {total_orders:>8,} | Items: {total_items:>8,} | Events: {total_events:>8,}")
        print()

        # 30-second cycle (reduces database lock contention with dashboard reads)
        time.sleep(30)

except KeyboardInterrupt:
    print("\n\n" + "=" * 80)
    print("STREAM STOPPED")
    print("=" * 80)
    print(f"Generated: {total_orders:,} orders, {total_items:,} items, {total_events:,} events")
    print("=" * 80 + "\n")

finally:
    try:
        conn.close()
    except:
        pass
