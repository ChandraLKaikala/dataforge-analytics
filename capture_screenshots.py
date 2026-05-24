#!/usr/bin/env python3
"""
Capture DataForge Professional Dashboard screenshots using Playwright

This script captures high-quality screenshots of all dashboard pages for README
documentation and GitHub repository showcase.
"""
import subprocess
import time
import sys
from pathlib import Path

def log_step(step, message):
    """Pretty print progress."""
    print(f"\n[{step}/4] {message}")
    print("=" * 50)

# Step 1: Setup
log_step(1, "Installing and verifying dependencies...")
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("  Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "-q"], check=True)
    from playwright.sync_api import sync_playwright

screenshots_dir = Path("screenshots")
screenshots_dir.mkdir(exist_ok=True)
print(f"  Output directory: {screenshots_dir}")

# Step 2: Start services
log_step(2, "Starting Dashboard (Professional Edition)...")
print("  Port: 8502")

dashboard = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "dashboard/app_professional.py", "--server.port", "8502"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
print("  Dashboard started...")
time.sleep(10)  # Give dashboard time to fully load

# Step 3: Configuration
log_step(3, "Preparing screenshot capture...")
pages_config = [
    ("Dashboard", "01_Dashboard.png", "Home"),
    ("Customers", "02_Customer_360.png", "Customer 360 View"),
    ("Analytics", "03_Analytics.png", "RFM Analytics"),
    ("Funnel", "04_Funnel.png", "Conversion Funnel"),
    ("Retention", "05_Retention.png", "Cohort Retention"),
]

print(f"  Total pages to capture: {len(pages_config)}")
print("  Resolution: 1920x1080 (Full HD)")

# Step 4: Capture
log_step(4, "Capturing screenshots...")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1.0
        )
        page = context.new_page()

        print("  Loading dashboard...")
        page.goto("http://localhost:8502", wait_until="networkidle", timeout=45000)
        time.sleep(4)

        captured = 0
        for idx, (page_name, file_name, display_name) in enumerate(pages_config):
            try:
                print(f"\n  [{idx+1}/{len(pages_config)}] {display_name}...")

                if idx > 0:
                    # Click the page link
                    print(f"      Navigating to {page_name}...")
                    time.sleep(1)
                    try:
                        # Find button/link containing page name
                        page.click(f"text={page_name}", timeout=10000)
                    except:
                        # Try alternative selectors
                        try:
                            buttons = page.locator("button")
                            for i in range(buttons.count()):
                                btn_text = buttons.nth(i).text_content()
                                if page_name.lower() in btn_text.lower():
                                    buttons.nth(i).click()
                                    break
                        except:
                            pass
                    time.sleep(3)

                # Wait for content to render
                print(f"      Rendering content...")
                page.wait_for_load_state("networkidle", timeout=20000)
                time.sleep(2)

                # Capture
                output_path = screenshots_dir / file_name
                print(f"      Saving to {output_path}...")
                page.screenshot(path=str(output_path), full_page=True)
                print(f"      [OK] {output_path}")
                captured += 1

            except Exception as e:
                print(f"      [WARNING] Error on {page_name}: {str(e)[:60]}")

        browser.close()

        print("\n" + "=" * 50)
        print(f"Successfully captured {captured}/{len(pages_config)} screenshots!")
        print("=" * 50)

except Exception as e:
    print(f"\nFatal error during capture: {str(e)[:120]}")
    import traceback
    traceback.print_exc()

finally:
    print("\nCleaning up...")
    try:
        dashboard.terminate()
        time.sleep(2)
        dashboard.kill()
        print("  Dashboard stopped")
    except:
        pass
    print("\nDone! Screenshots are ready for GitHub.")

