import os
import time
from playwright.sync_api import sync_playwright

PBIX_PATH = os.path.abspath(r"..\Lab_QP1_QP2\Visual1.pbix")
print(f"Target PBIX to upload: {PBIX_PATH} (exists: {os.path.exists(PBIX_PATH)})")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state="screenshots/pbi_auth_state.json",
        viewport={"width": 1600, "height": 900}
    )
    page = context.new_page()

    print("Navigating to My Workspace...")
    page.goto("https://app.powerbi.com/groups/me/list?experience=power-bi", timeout=60000)
    page.wait_for_timeout(8000)
    print("Workspace URL:", page.url)
    print("Page Title:", page.title())
    page.screenshot(path="screenshots/workspace_before_upload.png")

    # Look for Upload button
    upload_btn = page.locator("button:has-text('Upload'), [aria-label*='Upload'], button[name*='Upload']").first
    print("Upload button found count:", upload_btn.count())

    if upload_btn.count() > 0:
        print("Clicking Upload button...")
        upload_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path="screenshots/upload_menu.png")

        # In Power BI Service, Upload menu shows 'Browse' or 'OneDrive and SharePoint'
        browse_opt = page.locator("button:has-text('Browse'), span:has-text('Browse'), text='Browse'").first
        if browse_opt.count() > 0:
            print("Found Browse option, triggering file chooser...")
            with page.expect_file_chooser() as fc_info:
                browse_opt.click()
            file_chooser = fc_info.value
            file_chooser.set_files(PBIX_PATH)
            print("File set! Waiting for upload to complete...")
            page.wait_for_timeout(15000)
        else:
            print("Looking for file input directly...")
            file_input = page.locator("input[type='file']")
            if file_input.count() > 0:
                file_input.set_input_files(PBIX_PATH)
                print("Uploaded via input element.")
                page.wait_for_timeout(15000)
    else:
        # Check if there is an input[type='file'] on page
        file_input = page.locator("input[type='file']")
        if file_input.count() > 0:
            file_input.set_input_files(PBIX_PATH)
            print("Uploaded via hidden input.")
            page.wait_for_timeout(15000)

    page.screenshot(path="screenshots/workspace_after_upload.png")
    print("Workspace state captured after upload.")

    browser.close()
