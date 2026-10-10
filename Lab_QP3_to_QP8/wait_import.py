import os, time
from playwright.sync_api import sync_playwright

PBIX_PATH = os.path.abspath(r"..\Lab_QP1_QP2\Visual1.pbix")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(storage_state="screenshots/pbi_auth_state.json", viewport={"width": 1600, "height": 900})
    page = context = ctx.new_page()
    page.goto("https://app.powerbi.com/groups/me/list?experience=power-bi", timeout=60000)
    
    print("Waiting for workspace action buttons...")
    page.wait_for_selector("button:has-text('New item'), button:has-text('Import')", timeout=30000)
    time.sleep(3)
    page.screenshot(path="screenshots/workspace_loaded_ready.png")

    import_btn = page.locator("button:has-text('Import')").first
    print("Import button count:", import_btn.count())
    if import_btn.count() > 0:
        import_btn.click()
        time.sleep(2)
        page.screenshot(path="screenshots/import_opened_menu.png")
        print("Captured import dropdown.")

        # In Fabric/Power BI, options are often 'Power BI report', 'Local file', 'Browse'
        # Let's see what text is in the popup
        menus = page.locator("[role='menu'] button, [role='menuitem'], .ms-ContextualMenu-item")
        print("Menu items count:", menus.count())
        for i in range(menus.count()):
            txt = menus.nth(i).text_content()
            print(f"  Option {i}: {txt}")

        # Click the file upload option
        upload_opt = page.locator("button:has-text('Power BI'), button:has-text('File'), button:has-text('Browse'), [role='menuitem']").first
        if upload_opt.count() > 0:
            print("Clicking upload option with file chooser...")
            with page.expect_file_chooser() as fc_info:
                upload_opt.click()
            fc = fc_info.value
            fc.set_files(PBIX_PATH)
            print("Set Visual1.pbix! Waiting 25s for ingestion and report rendering...")
            time.sleep(25)
            page.screenshot(path="screenshots/uploaded_visual1_workspace.png")

    browser.close()
    print("Done wait import test.")
