import os, time
from playwright.sync_api import sync_playwright

PBIX_PATH = os.path.abspath(r"..\Lab_QP1_QP2\Visual1.pbix")
print(f"Uploading file: {PBIX_PATH}")

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
    time.sleep(1)

    print("Clicking 'From this computer' with file chooser...")
    from_pc = page.locator("text='From this computer'").first
    with page.expect_file_chooser(timeout=20000) as fc_info:
        from_pc.click()
    
    fc = fc_info.value
    print(f"File chooser intercepted! Submitting {PBIX_PATH}...")
    fc.set_files(PBIX_PATH)
    
    print("File uploaded. Waiting 35 seconds for Fabric ingestion...")
    time.sleep(35)

    page.screenshot(path="screenshots/visual1_in_workspace.png")
    print("Saved screenshots/visual1_in_workspace.png")

    # Check for Visual1 in workspace
    v1_link = page.locator("text='Visual1'").first
    print("Visual1 found in workspace:", v1_link.count())
    if v1_link.count() > 0:
        print("Clicking Visual1 to open the uploaded report in Power BI Service...")
        v1_link.click()
        time.sleep(15)
        print("Opened Visual1! URL:", page.url)
        page.screenshot(path="screenshots/real_visual1_cloud_report_p1.png")
        print("Saved screenshots/real_visual1_cloud_report_p1.png")

        # Open page 2 if present
        p2_tab = page.locator("text='2 Category and Time Analysis', text='Page 2'").first
        if p2_tab.count() > 0:
            p2_tab.click()
            time.sleep(6)
            page.screenshot(path="screenshots/real_visual1_cloud_report_p2.png")
            print("Saved screenshots/real_visual1_cloud_report_p2.png")

    browser.close()
    print("Finished Visual1 upload and capture pipeline successfully.")
