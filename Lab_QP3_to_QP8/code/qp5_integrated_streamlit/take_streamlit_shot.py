import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

py = r"C:\Users\ROG\AppData\Local\Programs\Python\Python312\python.exe"
st_script = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8\code\qp5_integrated_streamlit\streamlit_app\Home.py"
out1 = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8\figures\qp5_fig02_streamlit_app.png"
out2 = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8\figures\qp5_fig03_streamlit_kpis.png"

proc = subprocess.Popen([py, "-m", "streamlit", "run", st_script, "--server.port", "8501", "--server.headless", "true"])
time.sleep(5)

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1440,950")
options.add_argument("--disable-gpu")

try:
    driver = webdriver.Edge(options=options)
    driver.get("http://localhost:8501")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Enterprise Visual Analytics Hub')]"))
    )
    time.sleep(2)
    driver.save_screenshot(out1)
    
    # Click Executive KPIs
    kpi_nav = driver.find_element(By.XPATH, "//*[contains(text(), 'Executive KPIs')]")
    kpi_nav.click()
    time.sleep(4)
    driver.save_screenshot(out2)
    driver.quit()
    print("Both captures SUCCESS! Sizes:", os.path.getsize(out1), os.path.getsize(out2))
except Exception as e:
    print("Capture error:", e)
finally:
    proc.terminate()
    proc.kill()
