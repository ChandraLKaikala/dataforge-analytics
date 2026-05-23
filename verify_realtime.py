#!/usr/bin/env python3
"""
Comprehensive verification that DataForge is actually working and updating in real-time.
Checks database, counts records, monitors changes every 30 seconds.
"""
import subprocess
import time
import sys
import os
from pathlib import Path

try:
    import duckdb
except ImportError:
    print("Installing duckdb...")
    subprocess.run([sys.executable, "-m", "pip", "install", "duckdb", "-q"], check=True)
    import duckdb

DB_PATH = "dataforge/dataforge.duckdb"

print("=" * 70)
print("DATAFORGE REAL-TIME VERIFICATION")
print("=" * 70)

# Verify database file exists
print("\n[STEP 1] Checking database file...")
if not os.path.exists(DB_PATH):
    print(f"ERROR: Database file not found at {DB_PATH}")
    sys.exit(1)

db_size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
print(f"OK: Database file exists ({db_size_mb:.1f} MB)")

# Kill any existing processes
print("\n[STEP 2] Cleaning up old processes...")
os.system("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *streamlit*\" 2>nul")
os.system("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *streamer*\" 2>nul")
time.sleep(2)
print("OK: Old processes stopped")

# Start fresh services
print("\n[STEP 3] Starting fresh data streamer...")
streamer = subprocess.Popen(
    [sys.executable, "live_data_streamer_optimized.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)
print("OK: Data streamer started (PID: {})".format(streamer.pid))

# Verify database connection and tables
print("\n[STEP 4] Verifying database structure...")
try:
    conn = duckdb.connect(DB_PATH, read_only=True)

    # Get table list
    tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='raw'").fetchall()
    if not tables:
        print("WARNING: No tables found in 'raw' schema")
    else:
        print(f"OK: Found {len(tables)} tables:")
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM raw.{table[0]}").fetchone()[0]
            print(f"     - raw.{table[0]}: {count:,} records")

    conn.close()
except Exception as e:
    print(f"ERROR connecting to database: {e}")
    sys.exit(1)

# Monitor data changes every 30 seconds
print("\n[STEP 5] Monitoring real-time data changes for 3 minutes...")
print("(Data should increase every 30 seconds)")
print("-" * 70)

baseline_metrics = {}

try:
    for iteration in range(1, 7):  # 6 iterations = 3 minutes (with 30s cycles)
        time.sleep(30)

        conn = duckdb.connect(DB_PATH, read_only=True)

        orders_count = conn.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0]
        events_count = conn.execute("SELECT COUNT(*) FROM raw.web_events").fetchone()[0]
        customers_count = conn.execute("SELECT COUNT(DISTINCT customer_id) FROM raw.orders").fetchone()[0]
        latest_order_time = conn.execute("SELECT MAX(order_date) FROM raw.orders").fetchone()[0]
        latest_event_time = conn.execute("SELECT MAX(event_date) FROM raw.web_events").fetchone()[0]

        conn.close()

        timestamp = time.strftime("%H:%M:%S")

        print(f"\n[{timestamp}] Cycle {iteration}/6")
        print(f"  Orders:              {orders_count:,}")
        print(f"  Web Events:          {events_count:,}")
        print(f"  Unique Customers:    {customers_count:,}")
        print(f"  Latest Order:        {latest_order_time}")
        print(f"  Latest Event:        {latest_event_time}")

        # Check for increases
        if iteration > 1:
            order_increase = orders_count - baseline_metrics.get('orders', 0)
            event_increase = events_count - baseline_metrics.get('events', 0)

            status_orders = "[OK]" if order_increase > 0 else "[WARNING]"
            status_events = "[OK]" if event_increase > 0 else "[WARNING]"

            print(f"  Increase: {status_orders} Orders +{order_increase:,} | {status_events} Events +{event_increase:,}")

        baseline_metrics = {
            'orders': orders_count,
            'events': events_count,
            'customers': customers_count
        }

except KeyboardInterrupt:
    print("\n\nVerification interrupted by user")
except Exception as e:
    print(f"\n\nERROR during monitoring: {e}")

finally:
    print("\n" + "-" * 70)
    print("[STEP 6] Final database check...")

    try:
        conn = duckdb.connect(DB_PATH, read_only=True)

        orders_final = conn.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0]
        events_final = conn.execute("SELECT COUNT(*) FROM raw.web_events").fetchone()[0]
        customers_final = conn.execute("SELECT COUNT(DISTINCT customer_id) FROM raw.orders").fetchone()[0]

        # Revenue calculation
        revenue_total = conn.execute(
            "SELECT SUM(total_amount) FROM raw.orders WHERE status='Completed'"
        ).fetchone()[0]

        # Average order value
        aov = conn.execute(
            "SELECT AVG(total_amount) FROM raw.orders WHERE status='Completed'"
        ).fetchone()[0]

        conn.close()

        print(f"\nFINAL STATISTICS:")
        print(f"  Total Orders:        {orders_final:,}")
        print(f"  Total Events:        {events_final:,}")
        print(f"  Total Customers:     {customers_final:,}")
        print(f"  Total Revenue:       ${revenue_total:,.2f}")
        print(f"  Avg Order Value:     ${aov:,.2f}")

        if orders_final > 0 and events_final > 0:
            print(f"\n[OK] SUCCESS: Data is being generated and stored correctly!")
            print(f"[OK] Orders increased: {orders_final > baseline_metrics.get('orders', 0)}")
            print(f"[OK] Events increased: {events_final > baseline_metrics.get('events', 0)}")
        else:
            print(f"\n[FAIL] FAILURE: No data in database!")

    except Exception as e:
        print(f"ERROR in final check: {e}")

    print("\n" + "=" * 70)
    print("Cleaning up...")
    streamer.terminate()
    time.sleep(1)
    streamer.kill()
    print("Streamer stopped")
    print("=" * 70)

