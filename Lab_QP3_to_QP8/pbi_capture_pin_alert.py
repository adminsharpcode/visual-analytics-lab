import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Use saved storage state
    context = browser.new_context(
        storage_state="screenshots/pbi_auth_state.json",
        viewport={"width": 1600, "height": 900}
    )
    page = context.new_page()

    print("Opening Slice_N_Dril report directly with saved session...")
    page.goto("https://app.powerbi.com/home?experience=power-bi", timeout=60000)
    page.wait_for_timeout(6000)

    # Click Slice_N_Dril
    report_link = page.locator("text='Slice_N_Dril'").first
    if report_link.count() > 0:
        report_link.click()
    else:
        page.locator("button:has-text('Open')").first.click()

    page.wait_for_timeout(10000)
    print("Report loaded. URL:", page.url)

    # Click 'Set alert' in top action bar or hover over visual to get Pin
    alert_action = page.locator("button:has-text('Set alert'), [aria-label*='Set alert']").first
    if alert_action.count() > 0:
        print("Clicking 'Set alert' in action bar...")
        alert_action.click()
        page.wait_for_timeout(4000)
        page.screenshot(path="screenshots/pbi_cloud_04_data_alert.png")
        print("Saved screenshots/pbi_cloud_04_data_alert.png")

    # Now hover over the first line visual to reveal visual header icons (Pin, etc.)
    visual_box = page.locator(".visualContainer, [aria-label*='Sum of Sales']").first
    if visual_box.count() > 0:
        visual_box.hover()
        page.wait_for_timeout(1000)
        # Look for pin icon
        pin_btn = page.locator("button[aria-label*='Pin'], [data-testid*='pin']").first
        if pin_btn.count() > 0:
            print("Clicking Pin button...")
            pin_btn.click()
            page.wait_for_timeout(3000)
            page.screenshot(path="screenshots/pbi_cloud_05_pin_modal.png")
            print("Saved screenshots/pbi_cloud_05_pin_modal.png")

    browser.close()
    print("Finished pin and alert captures.")
