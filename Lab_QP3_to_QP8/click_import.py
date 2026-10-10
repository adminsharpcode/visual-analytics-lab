import os, time
from playwright.sync_api import sync_playwright

PBIX_PATH = os.path.abspath(r"..\Lab_QP1_QP2\Visual1.pbix")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(storage_state="screenshots/pbi_auth_state.json", viewport={"width": 1600, "height": 900})
    page = ctx.new_page()
    page.goto("https://app.powerbi.com/groups/me/list?experience=power-bi", timeout=60000)
    page.wait_for_timeout(8000)

    import_btn = page.locator("button:has-text('Import'), [aria-label*='Import']").first
    print("Import button count:", import_btn.count())
    if import_btn.count() > 0:
        import_btn.click()
        time.sleep(2)
        page.screenshot(path="screenshots/import_dropdown.png")
        print("Captured import dropdown.")

        # Look for options in dropdown
        items = page.locator(".ms-ContextualMenu-item, button, [role='menuitem']")
        print("Menu items count:", items.count())
        for i in range(min(10, items.count())):
            print(f"Item {i}:", items.nth(i).text_content())

        # Select file / Browse
        file_opt = page.locator("text='Browse', text='File', text='Upload', text='From this device', [role='menuitem']").first
        if file_opt.count() > 0:
            print("Found file upload option, uploading PBIX...")
            with page.expect_file_chooser() as fc_info:
                file_opt.click()
            fc = fc_info.value
            fc.set_files(PBIX_PATH)
            print("PBIX selected! Waiting 20s for upload processing...")
            time.sleep(20)
            page.screenshot(path="screenshots/post_import_upload.png")
            print("Saved screenshots/post_import_upload.png")

    browser.close()
