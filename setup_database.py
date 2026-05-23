#!/usr/bin/env python3
import duckdb
import os
from pathlib import Path

os.makedirs('dataforge/data/raw', exist_ok=True)
db_path = 'dataforge/dataforge.duckdb'

# Remove old database
if os.path.exists(db_path):
    os.remove(db_path)
    print("Removed old database")

conn = duckdb.connect(db_path)
conn.execute('PRAGMA threads=4')

print('\nSetting up database...')
conn.execute('CREATE SCHEMA IF NOT EXISTS raw')

print('Loading data from CSV files...')
data_dir = Path('dataforge/data/raw')

tables = {
    'customers': 'customer_id',
    'orders': 'order_id',
    'order_items': 'order_item_id',
    'products': 'product_id',
    'campaigns': 'campaign_id',
    'web_events': 'event_id',
}

for table_name in tables:
    csv_path = data_dir / f'{table_name}.csv'
    if csv_path.exists():
        conn.execute(f'CREATE OR REPLACE TABLE raw.{table_name} AS SELECT * FROM read_csv_auto("{str(csv_path)}")')
        count = conn.execute(f'SELECT COUNT(*) FROM raw.{table_name}').fetchone()[0]
        print(f'  OK {table_name:<20} {count:>10,} rows')
    else:
        print(f'  MISSING {table_name:<20}')

print('\nFinalizing...')
conn.close()
print('[OK] Database setup complete!\n')
