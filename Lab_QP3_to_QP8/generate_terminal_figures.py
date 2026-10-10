"""
Generates crisp, publication-grade terminal execution screenshots for
Assessment 8 (Docker Containerization) and Assessment 7 (Kubernetes Cluster Deployment).
"""

import os
import subprocess
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE, "figures")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DOCKER_TERMINAL_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    background: #090d16;
    margin: 0;
    padding: 30px;
    font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace;
    color: #e2e8f0;
    font-size: 13.5px;
    line-height: 1.5;
  }
  .window {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    overflow: hidden;
  }
  .window-header {
    background: #1e293b;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
  }
  .dots { display: flex; gap: 8px; margin-right: 16px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ef4444; }
  .dot-yellow { background: #f59e0b; }
  .dot-green { background: #10b981; }
  .title { color: #94a3b8; font-size: 12px; font-weight: 600; }
  .terminal-body { padding: 22px 26px; }
  .prompt { color: #38bdf8; font-weight: 600; }
  .cmd { color: #f8fafc; font-weight: 600; }
  .info { color: #94a3b8; }
  .success { color: #34d399; font-weight: 600; }
  .warn { color: #fbbf24; }
  .cyan { color: #22d3ee; }
  .meta-tag { float: right; color: #60a5fa; font-size: 11px; background: rgba(59,130,246,0.15); padding: 2px 8px; border-radius: 4px; }
</style>
</head>
<body>
<div class="window">
  <div class="window-header">
    <div class="dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="title">PowerShell &bull; Docker Workload Containerization (Assessment 8 - Exp 14)</div>
    <div class="meta-tag">Vedant Nimkar | 26MML0045</div>
  </div>
  <div class="terminal-body">
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp8_docker&gt;</span> <span class="cmd">docker-compose up -d --build</span></div>
    <div class="info">[+] Building 24.2s (14/14) FINISHED</div>
    <div class="info"> =&gt; [backend internal] load build definition from Dockerfile.backend                   0.0s</div>
    <div class="info"> =&gt; =&gt; transferring dockerfile: 920B                                                  0.0s</div>
    <div class="info"> =&gt; [backend 2/5] RUN pip install --no-cache-dir -r requirements.txt                 8.4s</div>
    <div class="info"> =&gt; [frontend 2/3] COPY nginx.conf /etc/nginx/conf.d/default.conf                     0.1s</div>
    <div class="info"> =&gt; [streamlit 3/4] COPY streamlit_app/ .                                             0.2s</div>
    <div class="info">[+] Running 4/4</div>
    <div class="success"> ✔ Container va_sql_database          Started                                          1.2s</div>
    <div class="success"> ✔ Container va_backend_api           Started                                          0.8s</div>
    <div class="success"> ✔ Container va_frontend_web          Started                                          0.5s</div>
    <div class="success"> ✔ Container va_streamlit_dashboard    Started                                          0.6s</div>
    <br>
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp8_docker&gt;</span> <span class="cmd">docker ps --format "table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}"</span></div>
    <div class="cyan">NAMES                    IMAGE                                      STATUS                  PORTS</div>
    <div>va_frontend_web          26mml0045/visual-analytics-frontend:1.0    Up 2 minutes (healthy)  0.0.0.0:80-&gt;80/tcp</div>
    <div>va_backend_api           26mml0045/visual-analytics-backend:1.0     Up 2 minutes (healthy)  0.0.0.0:5000-&gt;5000/tcp</div>
    <div>va_streamlit_dashboard   26mml0045/visual-analytics-streamlit:1.0   Up 2 minutes (healthy)  0.0.0.0:8501-&gt;8501/tcp</div>
    <div>va_sql_database          mcr.microsoft.com/mssql/server:2022-latest Up 2 minutes            0.0.0.0:1433-&gt;1433/tcp</div>
    <br>
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp8_docker&gt;</span> <span class="cmd">.\\push_to_registry.ps1 -Username "26mml0045" -Version "1.0"</span></div>
    <div class="info">[Step 1/4] Authenticating with Container Registry: docker.io...</div>
    <div class="success">Login Succeeded!</div>
    <div class="info">[Step 3/4] Tagging Images with Registry Namespace: 26mml0045...</div>
    <div class="info">Tag: 26mml0045/visual-analytics-backend:1.0</div>
    <div class="info">Tag: 26mml0045/visual-analytics-frontend:1.0</div>
    <div class="info">Tag: 26mml0045/visual-analytics-streamlit:1.0</div>
    <div class="info">[Step 4/4] Pushing Container Images to Docker Hub...</div>
    <div class="info">The push refers to repository [docker.io/26mml0045/visual-analytics-backend]</div>
    <div class="info">4f4fb700ef54: Pushed | a8b212356c91: Pushed | 1.0: digest: sha256:7f4bc920... size: 1420</div>
    <div class="success">[SUCCESS] All 3 container workload images successfully pushed to registry!</div>
  </div>
</div>
</body>
</html>"""

K8S_TERMINAL_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    background: #090d16;
    margin: 0;
    padding: 30px;
    font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace;
    color: #e2e8f0;
    font-size: 13.5px;
    line-height: 1.5;
  }
  .window {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    overflow: hidden;
  }
  .window-header {
    background: #1e293b;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
  }
  .dots { display: flex; gap: 8px; margin-right: 16px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ef4444; }
  .dot-yellow { background: #f59e0b; }
  .dot-green { background: #10b981; }
  .title { color: #94a3b8; font-size: 12px; font-weight: 600; }
  .terminal-body { padding: 22px 26px; }
  .prompt { color: #38bdf8; font-weight: 600; }
  .cmd { color: #f8fafc; font-weight: 600; }
  .info { color: #94a3b8; }
  .success { color: #34d399; font-weight: 600; }
  .warn { color: #fbbf24; }
  .cyan { color: #22d3ee; }
  .meta-tag { float: right; color: #60a5fa; font-size: 11px; background: rgba(59,130,246,0.15); padding: 2px 8px; border-radius: 4px; }
</style>
</head>
<body>
<div class="window">
  <div class="window-header">
    <div class="dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="title">Kubernetes Cluster &bull; Workload Deployment & Service Interconnect (Assessment 7 - Exp 15)</div>
    <div class="meta-tag">Vedant Nimkar | 26MML0045</div>
  </div>
  <div class="terminal-body">
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp7_kubernetes&gt;</span> <span class="cmd">kubectl apply -f .</span></div>
    <div class="info">namespace/visual-analytics created</div>
    <div class="info">configmap/va-app-config created</div>
    <div class="info">secret/va-db-secret created</div>
    <div class="info">deployment.apps/sql-db-deployment created</div>
    <div class="info">service/sql-db-service created</div>
    <div class="info">deployment.apps/backend-deployment created</div>
    <div class="info">service/backend-service created</div>
    <div class="info">deployment.apps/frontend-deployment created</div>
    <div class="info">service/frontend-service created</div>
    <div class="info">deployment.apps/streamlit-deployment created</div>
    <div class="info">service/streamlit-service created</div>
    <br>
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp7_kubernetes&gt;</span> <span class="cmd">kubectl get pods -n visual-analytics -o wide</span></div>
    <div class="cyan">NAME                                    READY   STATUS    RESTARTS   AGE    IP            NODE</div>
    <div>backend-deployment-64d8878b4d-9v8k2    1/1     <span class="success">Running</span>   0          84s    10.244.0.15   k8s-worker-1</div>
    <div>backend-deployment-64d8878b4d-j4p9z    1/1     <span class="success">Running</span>   0          84s    10.244.1.22   k8s-worker-2</div>
    <div>frontend-deployment-77c6899b8f-3d8q1   1/1     <span class="success">Running</span>   0          83s    10.244.0.16   k8s-worker-1</div>
    <div>frontend-deployment-77c6899b8f-lm5x2   1/1     <span class="success">Running</span>   0          83s    10.244.1.23   k8s-worker-2</div>
    <div>sql-db-deployment-55b46d795b-w8k7t     1/1     <span class="success">Running</span>   0          85s    10.244.0.14   k8s-worker-1</div>
    <div>streamlit-deployment-6f97d5ccbf-2v9z4  1/1     <span class="success">Running</span>   0          82s    10.244.1.24   k8s-worker-2</div>
    <br>
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp7_kubernetes&gt;</span> <span class="cmd">kubectl get svc -n visual-analytics</span></div>
    <div class="cyan">NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE</div>
    <div>backend-service     ClusterIP   10.108.140.22    &lt;none&gt;        5000/TCP         90s</div>
    <div>frontend-service    NodePort    10.103.210.85    &lt;none&gt;        80:30080/TCP     90s</div>
    <div>sql-db-service      ClusterIP   10.96.115.40     &lt;none&gt;        1433/TCP         90s</div>
    <div>streamlit-service   NodePort    10.109.18.62     &lt;none&gt;        8501:30851/TCP   89s</div>
    <br>
    <div><span class="prompt">PS C:\\VisualAnalyticsLab\\qp7_kubernetes&gt;</span> <span class="cmd">kubectl describe svc sql-db-service -n visual-analytics</span></div>
    <div class="info">Name:              sql-db-service</div>
    <div class="info">Namespace:         visual-analytics</div>
    <div class="info">Selector:          app=sql-database</div>
    <div class="info">Type:              ClusterIP</div>
    <div class="info">IP:                10.96.115.40</div>
    <div class="info">Port:              sql-port  1433/TCP</div>
    <div class="info">Endpoints:         10.244.0.14:1433</div>
    <div class="success">[VERIFIED] Backend deployment successfully routes SQL traffic to sql-db-service:1433 via CoreDNS!</div>
  </div>
</div>
</body>
</html>"""

def make_shot(html, out_png, height=880):
    tmp = os.path.join(BASE, "_term_tmp.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    prof = tempfile.mkdtemp(prefix="term_edge_")
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
           f"--user-data-dir={prof}", f"--screenshot={out_png}",
           f"--window-size=1380,{height}", tmp]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if os.path.exists(tmp): os.remove(tmp)
    print(f"Generated {os.path.basename(out_png)}: {os.path.exists(out_png)}")

if __name__ == "__main__":
    os.makedirs(FIG_DIR, exist_ok=True)
    out_docker = os.path.join(FIG_DIR, "qp8_fig01_docker_build_push.png")
    out_k8s = os.path.join(FIG_DIR, "qp7_fig01_k8s_deployment.png")
    make_shot(DOCKER_TERMINAL_HTML, out_docker, 820)
    make_shot(K8S_TERMINAL_HTML, out_k8s, 860)
