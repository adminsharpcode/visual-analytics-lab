from PIL import Image
import os

SHOTS_DIR = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8\screenshots"

# 1. Update real_brave_service.png using the maximized live capture
max_brave_path = os.path.join(SHOTS_DIR, "real_brave_maximized.png")
if os.path.exists(max_brave_path):
    img_brave = Image.open(max_brave_path)
    img_brave.save(os.path.join(SHOTS_DIR, "real_brave_service.png"))
    print("Updated real_brave_service.png")

    # 2. qp3_05_service_dashboard.png -> High-res crop of the live visuals in Power BI Service
    # Visuals area: x from 195 to 1540, y from 300 to 820
    crop_dash = img_brave.crop((195, 270, img_brave.width - 20, img_brave.height - 10))
    crop_dash.save(os.path.join(SHOTS_DIR, "qp3_05_service_dashboard.png"))
    print("Generated qp3_05_service_dashboard.png from real Power BI Service")

# 3. qp3_exp8_service_report_tile.png -> Crop from Power BI Home showing Slice_N_Dril and Artificial Intelligence Sample
home_path = os.path.join(SHOTS_DIR, "real_brave_pbi_home.png")
if os.path.exists(home_path):
    img_home = Image.open(home_path)
    # Crop the Recommended section: x from 100 to 700, y from 420 to 820
    crop_tile = img_home.crop((100, 430, 700, 810))
    crop_tile.save(os.path.join(SHOTS_DIR, "qp3_exp8_service_report_tile.png"))
    print("Generated qp3_exp8_service_report_tile.png from real Power BI Home")

# 4. Process Power BI Desktop real crops from real_pbi_desktop.png
pbi_path = os.path.join(SHOTS_DIR, "real_pbi_desktop.png")
if os.path.exists(pbi_path):
    img_pbi = Image.open(pbi_path)
    w, h = img_pbi.size

    # qp3_exp7_slicer_drilldown.png -> Crop clean bottom row of working visuals (Bar + Donut + Table)
    crop_canvas = img_pbi.crop((40, 470, 910, h - 5))
    crop_canvas.save(os.path.join(SHOTS_DIR, "qp3_exp7_slicer_drilldown.png"))
    print("Generated qp3_exp7_slicer_drilldown.png from real Power BI Desktop")

    # qp3_exp7_hierarchies_pane.png -> Crop Data and Visualizations pane (x from 920 to w, y from 270 to h)
    crop_pane = img_pbi.crop((920, 270, w, h))
    crop_pane.save(os.path.join(SHOTS_DIR, "qp3_exp7_hierarchies_pane.png"))
    print("Generated qp3_exp7_hierarchies_pane.png from real Power BI Desktop")

print("All real screenshot crops successfully generated!")
