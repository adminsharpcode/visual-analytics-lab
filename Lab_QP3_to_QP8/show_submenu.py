import os, time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(storage_state="screenshots/pbi_auth_state.json", viewport={"width": 1600, "height": 900})
    page = ctx.new_page()
    page.goto("https://app.powerbi.com/groups/me/list?experience=power-bi", timeout=60000)
    page.wait_for_selector("button:has-text('Import')", timeout=30000)
    time.sleep(2)
    page.locator("button:has-text('Import')").first.click()
    time.sleep(1)
    page.locator("text='Report, Paginated Report or Workbook'").first.click()
    time.sleep(2)
    page.screenshot(path="screenshots/import_submenu.png")
    print("Submenu captured!")
    items = page.locator("[role='menuitem'], button").all_text_contents()
    print("Items:", [it.strip() for it in items if it.strip()])
    browser.close()
