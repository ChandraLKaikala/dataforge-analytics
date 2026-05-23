#!/usr/bin/env python3
"""
Capture DataForge dashboard screenshots using Playwright
"""
import subprocess
import time
import sys
from pathlib import Path

print("[1/4] Installing playwright if needed...")
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "-q"], check=True)
    from playwright.sync_api import sync_playwright

screenshots_dir = Path("screenshots")
screenshots_dir.mkdir(exist_ok=True)

print("[2/4] Starting dashboard services...")
streamer = subprocess.Popen(
    [sys.executable, "live_data_streamer_optimized.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

dashboard = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "dashboard/app_simple.py", "--server.port", "8501"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(8)

print("[3/4] Waiting for dashboard to be ready...")
time.sleep(5)

pages_config = [
    ("Dashboard", "01_Dashboard"),
    ("Customer 360", "02_Customer_360"),
    ("Analytics", "03_Analytics"),
    ("Funnel", "04_Funnel"),
    ("Retention", "05_Retention")
]

try:
    print("[4/4] Capturing screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("  - Loading dashboard...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        for idx, (page_name, file_name) in enumerate(pages_config):
            try:
                print(f"  - Capturing {page_name}...")

                if idx > 0:
                    # Click the page name in the radio button
                    time.sleep(1)
                    radio_buttons = page.locator("label")
                    for i in range(radio_buttons.count()):
                        btn = radio_buttons.nth(i)
                        if page_name in btn.text_content():
                            btn.click()
                            break
                    time.sleep(3)

                # Wait for page to load
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)

                # Take screenshot
                output_path = screenshots_dir / f"{file_name}.png"
                page.screenshot(path=str(output_path), full_page=False)
                print(f"    Saved: {output_path}")

            except Exception as e:
                print(f"    Error on {page_name}: {str(e)[:50]}")

        browser.close()
        print("\nAll screenshots captured!")

except Exception as e:
    print(f"Fatal error: {str(e)[:100]}")

finally:
    print("\nCleaning up processes...")
    try:
        dashboard.terminate()
        streamer.terminate()
        time.sleep(2)
        dashboard.kill()
        streamer.kill()
    except:
        pass
    print("Done!")
