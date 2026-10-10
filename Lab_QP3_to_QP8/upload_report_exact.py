import os, time
from playwright.sync_api import sync_playwright

PBIX_PATH = os.path.abspath(r"..\Lab_QP1_QP2\Visual1.pbix")

print(f"Target PBIX: {PBIX_PATH}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(storage_state="screenshots/pbi_auth_state.json", viewport={"width": 1600, "height": 900})
    page = ctx.new_page()
    page.goto("https://app.powerbi.com/groups/me/list?experience=power-bi", timeout=60000)
    
    page.wait_for_selector("button:has-text('Import')", timeout=30000)
    time.sleep(3)

    import_btn = page.locator("button:has-text('Import')").first
    import_btn.click()
    time.sleep(1)

    # Click 'Report, Paginated Report or Workbook'
    report_opt = page.locator("text='Report, Paginated Report or Workbook'").first
    print("Found Report option. Setting file chooser listener...")
    
    with page.expect_file_chooser(timeout=20000) as fc_info:
        report_opt.click()
    
    fc = fc_info.value
    print(f"File chooser opened! Uploading {PBIX_PATH}...")
    fc.set_files(PBIX_PATH)
    
    print("File submitted. Waiting 30 seconds for Fabric/Power BI ingestion...")
    time.sleep(30)
    page.screenshot(path="screenshots/visual1_uploaded_success.png")
    print("Saved screenshots/visual1_uploaded_success.png")

    # Now let's see what is listed in My workspace
    items = page.locator(".mat-row, .row, [role='row']").all_text_contents()
    print("Workspace items after upload:", [it.strip().replace('\n', ' ') for it in items if it.strip()])

    browser.close()
    print("Done upload script.")
