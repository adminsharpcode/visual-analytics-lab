import time
import json
from playwright.sync_api import sync_playwright

EMAIL = "vedant.nimkar2026@vitstudent.ac.in"
PASSWORD = "Dvsam@25122003"

print("Starting full authenticated Power BI session...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()

    # Step 1: Login
    print("Navigating to SSO...")
    page.goto("https://app.powerbi.com/singleSignOn?experience=power-bi", timeout=60000)
    page.wait_for_selector("input")
    page.locator("input").first.fill(EMAIL)
    time.sleep(1)
    
    page.locator("button:has-text('Submit'), input[type='submit'], button[type='submit']").first.click()
    time.sleep(4)
    
    # Enter password
    pwd = page.locator("input[type='password']")
    if pwd.count() > 0:
        print("Entering password...")
        pwd.first.fill(PASSWORD)
        time.sleep(1)
        page.locator("input[type='submit'], button[type='submit']").first.click()
        time.sleep(4)

    # Stay signed in
    stay = page.locator("input[value='Yes'], button:has-text('Yes'), #idSIButton9")
    if stay.count() > 0:
        print("Clicking Stay signed in...")
        stay.first.click()

    # Wait for Power BI Home to completely load (wait until URL has /home or title has Power BI)
    print("Waiting for Power BI Home to complete loading...")
    for i in range(25):
        time.sleep(2)
        print(f"[{i*2}s] Current URL: {page.url} | Title: {page.title()}")
        if "home" in page.url or page.locator("nav, .pbi-home, [aria-label='Home']").count() > 0:
            print("Home detected!")
            break

    time.sleep(8)
    context.storage_state(path="screenshots/pbi_auth_state.json")
    print("Saved auth session state.")

    # Screenshot 1: Power BI Service Home Portal
    page.screenshot(path="screenshots/pbi_cloud_01_home.png", full_page=False)
    print("Saved screenshots/pbi_cloud_01_home.png")

    # Look for Slice_N_Dril report link or button
    print("Looking for Slice_N_Dril report...")
    report_link = page.locator("text='Slice_N_Dril'").first
    if report_link.count() > 0:
        print("Found Slice_N_Dril! Clicking to open report...")
        report_link.click()
    else:
        print("Looking for Open button on recommended cards...")
        open_btns = page.locator("button:has-text('Open')")
        if open_btns.count() > 1:
            open_btns.nth(1).click()
        elif open_btns.count() == 1:
            open_btns.first.click()

    # Wait for Report Canvas to load
    print("Waiting for report canvas to render...")
    time.sleep(12)
    print(f"Report URL: {page.url} | Title: {page.title()}")
    page.screenshot(path="screenshots/pbi_cloud_02_report.png")
    print("Saved screenshots/pbi_cloud_02_report.png")

    # Try opening Comments flyout
    comments_btn = page.locator("button[aria-label*='Comment'], button:has-text('Comment'), [data-testid*='comment']").first
    if comments_btn.count() > 0:
        print("Clicking Comments button...")
        comments_btn.click()
        time.sleep(4)
        page.screenshot(path="screenshots/pbi_cloud_03_comments.png")
        print("Saved screenshots/pbi_cloud_03_comments.png")

    browser.close()
    print("Finished Power BI capture session successfully.")
