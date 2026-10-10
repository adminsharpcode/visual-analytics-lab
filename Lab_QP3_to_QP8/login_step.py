import time
from playwright.sync_api import sync_playwright

EMAIL = "vedant.nimkar2026@vitstudent.ac.in"
PASSWORD = "Dvsam@25122003"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()

    print("Navigating to SSO...")
    page.goto("https://app.powerbi.com/singleSignOn?experience=power-bi", timeout=60000)
    page.wait_for_selector("input")
    page.locator("input").first.fill(EMAIL)
    time.sleep(1)
    
    # Click Submit
    submit_btn = page.locator("button:has-text('Submit'), input[type='submit'], button[type='submit']").first
    submit_btn.click()
    print("Clicked submit, waiting for redirect...")
    
    time.sleep(5)
    print("Redirected URL:", page.url)
    print("Title:", page.title())
    page.screenshot(path="screenshots/pbi_step2_redirect.png")

    # If redirected to Microsoft login
    if "login.microsoftonline.com" in page.url or "vitstudent" in page.url:
        print("At Microsoft login portal. Looking for password...")
        # Sometimes Microsoft asks for password immediately or after username confirmation
        time.sleep(2)
        pwd = page.locator("input[type='password']")
        if pwd.count() > 0:
            print("Entering password...")
            pwd.first.fill(PASSWORD)
            time.sleep(1)
            page.locator("input[type='submit'], button[type='submit']").first.click()
            time.sleep(5)
            print("Post-password URL:", page.url)
            page.screenshot(path="screenshots/pbi_step3_postpwd.png")
            
            # Check for Stay signed in?
            stay = page.locator("input[value='Yes'], button:has-text('Yes'), #idSIButton9")
            if stay.count() > 0:
                print("Clicking Stay signed in (Yes)...")
                stay.first.click()
                time.sleep(6)
                print("Final URL:", page.url)
                page.screenshot(path="screenshots/pbi_step4_final.png")

    browser.close()
    print("Done step test.")
