import time
from playwright.sync_api import sync_playwright

EMAIL = "vedant.nimkar2026@vitstudent.ac.in"
PASSWORD = "Dvsam@25122003"

print("Starting Playwright automation to log into Power BI Service...")

with sync_playwright() as p:
    # Launch browser with standard viewport
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()

    print("Navigating to https://app.powerbi.com/ ...")
    page.goto("https://app.powerbi.com/home?experience=power-bi", timeout=60000)
    page.wait_for_timeout(3000)
    print("Current URL:", page.url)
    print("Page Title:", page.title())

    # Check for email input
    email_input = page.locator("input[type='email']")
    if email_input.count() > 0:
        print("Entering email...")
        email_input.fill(EMAIL)
        page.wait_for_timeout(500)
        # Click Next / Submit
        page.locator("input[type='submit'], button[type='submit'], button:has-text('Next')").first.click()
        page.wait_for_timeout(3000)

    print("Checking for password field...")
    print("Current URL:", page.url)
    # Check for password input
    password_input = page.locator("input[type='password']")
    if password_input.count() > 0:
        print("Entering password...")
        password_input.fill(PASSWORD)
        page.wait_for_timeout(500)
        page.locator("input[type='submit'], button[type='submit'], button:has-text('Sign in')").first.click()
        page.wait_for_timeout(4000)

    print("Checking for 'Stay signed in?' prompt...")
    print("Current URL:", page.url)
    # Look for "Stay signed in" button (Yes / No)
    stay_btn = page.locator("input[type='submit'][value='Yes'], button:has-text('Yes'), #idSIButton9")
    if stay_btn.count() > 0:
        print("Clicking 'Yes' to stay signed in...")
        stay_btn.first.click()
        page.wait_for_timeout(5000)

    # Wait for Power BI Home navigation
    print("Waiting for Power BI dashboard/home to load...")
    try:
        page.wait_for_url("**/powerbi.com/**", timeout=30000)
    except Exception as e:
        print("Wait for URL timeout, checking current page:", e)

    page.wait_for_timeout(6000)
    print("Final URL:", page.url)
    print("Final Title:", page.title())

    # Take screenshot of whatever page we reached
    page.screenshot(path="screenshots/pbi_real_login_result.png")
    print("Saved screenshot to screenshots/pbi_real_login_result.png")

    # Save storage state so we can reuse cookies without re-logging in
    context.storage_state(path="screenshots/pbi_auth_state.json")
    print("Saved auth session to screenshots/pbi_auth_state.json")

    browser.close()
