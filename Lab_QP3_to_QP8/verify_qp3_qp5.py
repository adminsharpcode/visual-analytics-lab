import os
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

WORKSPACE = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8"
os.chdir(WORKSPACE)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

PORT = 8089
httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP server running on http://127.0.0.1:{PORT}")

errors_detected = []

def test_qp3(browser):
    print("\n--- TESTING QP3 (HTML/CSS Dashboard) ---")
    
    # 1. Desktop Test
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    
    def on_console(msg):
        if msg.type in ['error']:
            print(f"  [QP3 Console ERROR]: {msg.text}")
            errors_detected.append(f"QP3 Console Error: {msg.text}")
    page.on('console', on_console)
    page.on('pageerror', lambda err: errors_detected.append(f"QP3 Page Error: {err}"))

    url = f"http://127.0.0.1:{PORT}/code/qp3_html_css/index.html"
    page.goto(url)
    page.wait_for_load_state('networkidle')
    print("  QP3 Loaded successfully on desktop.")

    # Check Initial KPIs
    rev_init = page.inner_text('#valRevenue')
    print(f"  Initial Revenue: {rev_init}")
    assert rev_init == "$8,955,541", f"Expected $8,955,541 but got {rev_init}"

    # Test View Switching
    views = ['categories', 'trends', 'territories', 'drilldown', 'export', 'overview']
    for v in views:
        link = page.locator(f'a[href="#{v}"]')
        link.click()
        time.sleep(0.1)
        panel = page.locator(f'#view-{v}')
        is_active = "active" in panel.get_attribute("class")
        print(f"  Navigating to #{v}: Active panel status = {is_active}")
        assert is_active, f"View #{v} failed to activate!"

    # Test Filter Interactivity
    cat_select = page.locator('#categoryFilter')
    cat_select.select_option('Bikes')
    time.sleep(0.2)
    rev_bikes = page.inner_text('#valRevenue')
    print(f"  Filtered by Bikes: Revenue = {rev_bikes}")
    assert rev_bikes == "$6,420,110", f"Expected $6,420,110 but got {rev_bikes}"

    # Test Refresh Button
    refresh_btn = page.locator('#refreshBtn')
    refresh_btn.click()
    time.sleep(0.3)
    toast = page.locator('#dashboardToast')
    toast_visible = toast.is_visible()
    toast_text = toast.inner_text()
    print(f"  Refresh clicked: Toast visible={toast_visible}, text='{toast_text.strip()}'")
    assert toast_visible, "Toast notification did not appear on refresh!"

    # Test Reset Button
    page.locator('#resetFilters').click()
    time.sleep(0.2)
    rev_reset = page.inner_text('#valRevenue')
    print(f"  Reset filters: Revenue = {rev_reset}")
    assert rev_reset == "$8,955,541", f"Expected $8,955,541 after reset"

    page.screenshot(path="qp3_desktop_verified.png")
    print("  Saved qp3_desktop_verified.png")
    context.close()

    # 2. Android Mobile Viewport Test (Pixel 7: 393 x 851)
    print("  Testing QP3 on Android Mobile (393 x 851)...")
    mobile_context = browser.new_context(
        viewport={'width': 393, 'height': 851},
        user_agent="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        is_mobile=True,
        has_touch=True
    )
    m_page = mobile_context.new_page()
    m_page.goto(url)
    m_page.wait_for_load_state('networkidle')
    
    # Click categories on mobile
    m_page.locator('a[href="#categories"]').click()
    time.sleep(0.2)
    m_page.screenshot(path="qp3_android_verified.png")
    print("  Saved qp3_android_verified.png")
    mobile_context.close()


def test_qp5(browser):
    print("\n--- TESTING QP5 (Integrated Streamlit Dashboard) ---")
    
    # 1. Desktop Test
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    
    def on_console(msg):
        if msg.type in ['error']:
            print(f"  [QP5 Console ERROR]: {msg.text}")
            errors_detected.append(f"QP5 Console Error: {msg.text}")
    page.on('console', on_console)
    page.on('pageerror', lambda err: errors_detected.append(f"QP5 Page Error: {err}"))

    url = f"http://127.0.0.1:{PORT}/code/qp5_integrated_streamlit/index.html"
    page.goto(url)
    page.wait_for_load_state('networkidle')
    time.sleep(1.0) # Allow ECharts to render
    print("  QP5 Loaded successfully on desktop.")

    # Check Initial KPIs
    rev_init = page.inner_text('#kpiRevenue')
    print(f"  Initial Revenue: {rev_init}")
    assert "$8,955,541" in rev_init, f"Expected $8,955,541 but got {rev_init}"

    # Test View Tab Switching
    tabs = [
        ('kpis', 'Executive KPIs & Trends'),
        ('drilldown', 'Category Drilldown'),
        ('territory', 'Territory Share & Matrix'),
        ('ledger', 'Product Ledger'),
        ('architecture', 'Streamlit Architecture'),
        ('all', 'All Views (Overview)')
    ]
    for tab_id, tab_label in tabs:
        tab_btn = page.locator(f'.view-tab:has-text("{tab_label}")')
        tab_btn.click()
        time.sleep(0.2)
        is_active = "active" in tab_btn.get_attribute("class")
        print(f"  Switched to tab '{tab_label}': Active status = {is_active}")
        assert is_active, f"Tab {tab_label} failed to activate!"

    # Test Category Slicer Buttons
    bikes_btn = page.locator('.filter-pill[data-filter="category"][data-val="Bikes"]')
    bikes_btn.click()
    time.sleep(0.3)
    rev_bikes = page.inner_text('#kpiRevenue')
    print(f"  Selected Bikes Slicer: Revenue = {rev_bikes}")
    assert "$6,420,110" in rev_bikes, f"Expected Bikes revenue $6,420,110 but got {rev_bikes}"

    # Test Refresh Button & Toast
    refresh_btn = page.locator('#refreshBtn')
    refresh_btn.click()
    time.sleep(0.3)
    toast = page.locator('#dashboardToast')
    toast_visible = toast.is_visible()
    toast_text = toast.inner_text()
    print(f"  Refresh clicked: Toast visible={toast_visible}, text='{toast_text.strip()}'")
    assert toast_visible, "Toast notification did not appear on refresh in QP5!"

    page.screenshot(path="qp5_desktop_verified.png")
    print("  Saved qp5_desktop_verified.png")
    context.close()

    # 2. Android Mobile Viewport Test (Pixel 7: 393 x 851)
    print("  Testing QP5 on Android Mobile (393 x 851)...")
    mobile_context = browser.new_context(
        viewport={'width': 393, 'height': 851},
        user_agent="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        is_mobile=True,
        has_touch=True
    )
    m_page = mobile_context.new_page()
    m_page.goto(url)
    m_page.wait_for_load_state('networkidle')
    time.sleep(1.0)
    
    # Test Category Drilldown tab on mobile
    drill_tab = m_page.locator('.view-tab:has-text("Category Drilldown")')
    drill_tab.click()
    time.sleep(0.3)
    m_page.screenshot(path="qp5_android_verified.png")
    print("  Saved qp5_android_verified.png")
    mobile_context.close()


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            test_qp3(browser)
            test_qp5(browser)
        finally:
            browser.close()
            httpd.shutdown()

    if errors_detected:
        print(f"\n[FAIL] Detected {len(errors_detected)} errors:")
        for err in errors_detected:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] ALL QP3 & QP5 TESTS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    main()
