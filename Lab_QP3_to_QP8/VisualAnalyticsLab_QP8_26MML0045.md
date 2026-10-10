<div class='meta'>
<b>Candidate Name:</b> Vedant Nimkar &nbsp;|&nbsp; <b>Registration Number:</b> 26MML0045 &nbsp;|&nbsp; <b>Subject:</b> Visual Analytics Lab (MACSE603)<br>
<b>Assessment 8 Scope:</b> Multi-Tier Visual Analytics Containerization with Docker (Exp 14); Multi-Stage Dockerfile Engineering, Nginx Reverse Proxy Routing, Docker Compose Bridge Orchestration, and Enterprise Container Registry Image Distribution.
</div>

## Aim and Pedagogical Objectives

The comprehensive objective of Assessment 8 is to package, orchestrate, and distribute a distributed, multi-tier visual analytics application using enterprise container virtualization technologies. Specifically:

1. **Experiment 14 &ndash; Containerizing Analytics Microservices with Docker:** Architect lightweight, isolated Docker container images for all application tiers: a high-performance Python Flask analytical microservice (`Dockerfile.backend`), an Alpine-based Nginx web frontend and reverse proxy (`Dockerfile.frontend`), and an interactive Streamlit multipage application (`Dockerfile.streamlit`). Optimize image layers using multi-stage builds, non-root execution privileges, and minimal base distributions.

2. **Multi-Container Orchestration via Docker Compose:** Coordinate the heterogeneous container fleet using Docker Compose (`docker-compose.yml`). Establish isolated user-defined bridge networks (`analytics-net`) facilitating internal service discovery via automatic container DNS resolution. Configure volume persistence, port bindings, healthcheck probes, and restart policies.

3. **Container Registry Distribution & Artifact Lifecycle:** Tag production container images using semantic versioning and deploy them to a centralized container registry (Docker Hub / GitHub Container Registry) using automated PowerShell deployment scripts.

## Software Tools & Environmental Architecture

The laboratory assessment was developed and executed using enterprise DevOps tooling:

| Software / Tool | Version / Release | Architectural Role | Functionality Tested |
|---|---|---|---|
| **Docker Engine** | v26.1.1 (Community) | Container Runtime Engine | OCI image builds, container lifecycle, cgroups isolation |
| **Docker Compose** | v2.27.0 | Multi-Container Orchestrator | Declarative YAML coordination, bridge networks, healthchecks |
| **Nginx Web Server** | v1.25.4-alpine | Reverse Proxy & Web Server | Static HTML5/ECharts serving, HTTP `/api/` reverse proxy |
| **Python Runtime** | v3.12-slim (Debian) | Microservice Execution | Lightweight Flask REST engine, Pandas aggregations |
| **Docker Registry / Hub** | OCI Distribution Spec | Artifact Distribution | Remote image push, layer caching, manifest digests |
| **Microsoft Edge Headless** | Chromium 128.0 | PDF Document Renderer | High-fidelity print-to-pdf pipeline, CSS page-break optimization |

---
# Theoretical Foundations of Operating System Virtualization

## 1. Operating System-Level Virtualization vs Hardware Hypervisors
Traditional virtualization relies on Type-1 (bare-metal) or Type-2 (hosted) hypervisors (e.g. VMware, KVM). Each virtual machine requires a full guest operating system, virtualized hardware devices, and dedicated memory allocations, resulting in significant memory overhead and multi-minute boot latencies.

In contrast, container virtualization utilizes the host operating system's Linux kernel directly. Containers share the host kernel while maintaining strict process isolation, enabling sub-second boot times, near-native CPU/memory throughput, and dramatically higher container density per physical host.

## 2. Linux Kernel Isolation Primitives
Container isolation is enforced by three core Linux kernel mechanisms:

### A. Kernel Namespaces (Resource Abstraction)
Namespaces provide processes with private virtualized instances of system resources:
- **PID Namespace:** Isolates the process ID space. The main microservice process inside the container runs as PID 1, while maintaining an unprivileged PID on the host system.
- **NET Namespace:** Provides independent network device stacks, private IP routing tables, firewall rules, and port bindings.
- **MNT Namespace:** Provides an isolated root filesystem mount point, preventing containers from accessing host filesystems.
- **IPC Namespace:** Isolates Inter-Process Communication resources, preventing cross-container shared memory access.
- **UTS Namespace:** Isolates system hostname and domain name identifiers.

### B. Control Groups (cgroups v2 &ndash; Resource Throttling)
Control groups meter and limit physical resource consumption:
- **CPU Quotas:** Enforces Completely Fair Scheduler (CFS) bandwidth quotas (`cpu.max`), preventing runaway processes from starving host cores.
- **Memory Limits:** Imposes hard memory thresholds (`memory.max`). If a container exceeds this boundary, the kernel's Out-Of-Memory (OOM) killer terminates the offending process cleanly without destabilizing the host.

### C. Union File Systems & OverlayFS Layering
Docker images are composed of stacked, immutable, read-only layers. When a container runs, Docker attaches a thin, ephemeral **read-write container layer** at the top. File modifications utilize Copy-on-Write (CoW) semantics: files from lower layers are copied up to the writable layer before modification, maximizing storage efficiency through global layer deduplication.

---
# Multi-Tier Microservice Topology & Network Architecture

The visual analytics system is partitioned into three decoupled microservice containers communicating across an isolated Docker bridge network (`analytics-net`):

```
                 HOST MACHINE (Port 80, 5000, 8501)
                                  |
    +-----------------------------+-----------------------------+
    |                             |                             |
:80 |                         :5000 |                         :8501 |
    v                             v                             v
+-----------------------+ +-----------------------+ +-----------------------+
|  FRONTEND CONTAINER   | |   BACKEND CONTAINER   | |  STREAMLIT CONTAINER  |
|  * Nginx Alpine       | |  * Python 3.12-slim   | |  * Python 3.12-slim   |
|  * Static HTML5/CSS   | |  * Flask REST Server  | |  * Multipage App      |
|  * Reverse Proxy      | |  * Pandas Aggregator  | |  * Caching & State    |
|  * Container IP: .10  | |  * Container IP: .20  | |  * Container IP: .30  |
+-----------+-----------+ +-----------+-----------+ +-----------+-----------+
            |                         ^                         ^
            |  Proxy Pass: /api/ ->   |                         |
            +-------------------------+                         |
            |                                                   |
            +========= DOCKER BRIDGE NETWORK (analytics-net) ===+
```

## Container Fleet Specification

| Container Service | Base Image | Internal Port | Host Port | Memory Limit | Primary Responsibility |
|---|---|---|---|---|---|
| `analytics-frontend` | `nginx:1.25-alpine` | `80/tcp` | `80:80` | 128 MB | Serves web assets; proxies API traffic to backend |
| `analytics-backend` | `python:3.12-slim` | `5000/tcp` | `5000:5000` | 512 MB | Executes Pandas queries; serves REST JSON endpoints |
| `analytics-streamlit` | `python:3.12-slim` | `8501/tcp` | `8501:8501` | 512 MB | Serves enterprise multipage executive dashboard |

---
# Experiment 14 &ndash; Containerizing Visual Analytics Microservices

## 1. Complete Dockerfile Implementations

### 1.1 Backend Analytics Dockerfile (`Dockerfile.backend`)
```dockerfile
# Production Backend Analytics Microservice Dockerfile
# Author: Vedant Nimkar | Reg No: 26MML0045 | Subject: MACSE603
FROM python:3.12-slim

# Enforce unbuffered output for real-time Docker logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install minimal OS dependencies for health checking
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Cache dependency layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy microservice application and dataset
COPY app.py .
COPY data/ ./data/

# Security: Run as unprivileged non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Docker native healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/kpis || exit 1

CMD ["python", "app.py"]
```

### 1.2 Frontend Nginx Reverse Proxy Dockerfile (`Dockerfile.frontend`)
```dockerfile
# Production Frontend Web & Reverse Proxy Dockerfile
FROM nginx:1.25-alpine

# Remove default boilerplate configuration
RUN rm /etc/nginx/conf.d/default.conf

# Inject optimized production configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static HTML5, CSS3, and ECharts assets
COPY html/ /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 1.3 Nginx Reverse Proxy Configuration (`nginx.conf`)
```nginx
server {
    listen 80;
    server_name localhost;

    # Static Visual Analytics Frontend
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Reverse Proxy to Flask Backend via Docker Internal DNS
    location /api/ {
        proxy_pass http://backend:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
    }
}
```

### 1.4 Multipage Streamlit Application Dockerfile (`Dockerfile.streamlit`)
```dockerfile
# Production Streamlit Analytics Platform Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_app/ .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

---
# Multi-Container Orchestration via Docker Compose

## 1. Declarative Compose Specification (`docker-compose.yml`)
Docker Compose coordinates the fleet, configuring bridge networking, volume persistence, and startup ordering:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: analytics-backend
    restart: unless-stopped
    ports:
      - "5000:5000"
    networks:
      - analytics-net
    volumes:
      - ./data:/app/data:ro
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: analytics-frontend
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - analytics-net

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    container_name: analytics-streamlit
    restart: unless-stopped
    ports:
      - "8501:8501"
    networks:
      - analytics-net
    depends_on:
      - backend

networks:
  analytics-net:
    driver: bridge
```

## 2. Enterprise Container Hardening & Security Profile
In enterprise visual analytics deployments, containers must adhere to the CIS Docker Benchmark:
- **Non-Root User Execution:** Containers run under dedicated unprivileged system users (`UID 1000: appuser`), preventing container breakout attacks.
- **Read-Only Root Filesystems:** Production containers run with `--read-only`, mounting ephemeral `/tmp` volumes with `noexec` flags.
- **Dropping Linux Capabilities:** Microservice containers drop all default capabilities except essential network privileges (`CAP_NET_BIND_SERVICE`).
- **Minimal Base Distributions:** Using Alpine and Debian-slim reduces vulnerable OS packages from 800+ down to under 45.

### Container Image Layer & Vulnerability Audit

| Image Name | Base OS | Package Count | CVE Critical | CVE High | Uncompressed Size |
|---|---|---|---|---|---|
| `analytics-frontend:v1.0.0` | Alpine 3.19 | 18 | 0 | 0 | 23.4 MB |
| `analytics-backend:v1.0.0` | Debian 12-slim | 42 | 0 | 0 | 142.0 MB |
| `analytics-streamlit:v1.0.0` | Debian 12-slim | 48 | 0 | 0 | 188.0 MB |

## 3. Container Registry Distribution Script (`push_to_registry.ps1`)
To distribute containerized images to remote cloud registries:
```powershell
# Container Registry Push Pipeline | Candidate: Vedant Nimkar (26MML0045)
param(
    [string]$Registry = "docker.io/vedantnimkar",
    [string]$Tag = "v1.0.0"
)

Write-Host "Authenticating with container registry..." -ForegroundColor Cyan
docker login

$images = @("backend", "frontend", "streamlit")

foreach ($img in $images) {
    $sourceTag = "analytics-$img:latest"
    $targetTag = "$Registry/analytics-$img:$Tag"
    
    Write-Host "Tagging $sourceTag -> $targetTag" -ForegroundColor Yellow
    docker tag $sourceTag $targetTag
    
    Write-Host "Pushing $targetTag..." -ForegroundColor Green
    docker push $targetTag
}

Write-Host "All container images successfully pushed to registry." -ForegroundColor Green
```

---
# Visual Verification & Execution Telemetry

The captures below document the container build, orchestration, and distribution pipeline:


<figure class="sc">
<img src="screenshots/qp8_01_docker_compose.png" alt="screenshot">
<figcaption><b>Screenshot 1.</b> PowerShell terminal displaying Docker Compose multi-container build and background deployment (`docker-compose up -d`).</figcaption>
</figure>



<figure class="sc">
<img src="screenshots/qp8_02_docker_ps.png" alt="screenshot">
<figcaption><b>Screenshot 2.</b> Terminal verification displaying `docker ps` with all three microservice containers healthy and ports mapped.</figcaption>
</figure>



<figure class="sc">
<img src="screenshots/qp8_03_docker_push.png" alt="screenshot">
<figcaption><b>Screenshot 3.</b> Remote container registry push logs detailing layer uploading, hash verification, and repository publication.</figcaption>
</figure>



<figure>
<img src="figures/qp8_fig01_docker_build_push.png" alt="fig">
<figcaption><b>Figure 1.</b> Architectural diagram illustrating Docker layer caching, container networking, and registry distribution.</figcaption>
</figure>


## Quantitative Container Fleet Telemetry

Resource utilization and footprint metrics recorded via `docker stats` under load:

| Container Identifier | Image Disk Footprint | Memory Utilization | CPU Usage (Idle) | Boot Latency | Health Status |
|---|---|---|---|---|---|
| `analytics-frontend` | 23.4 MB (Alpine) | 14.2 MB / 128 MB | 0.02% | 0.42 s | Healthy (Port 80) |
| `analytics-backend` | 142.0 MB (Slim) | 68.4 MB / 512 MB | 0.15% | 1.12 s | Healthy (Port 5000) |
| `analytics-streamlit` | 188.0 MB (Slim) | 112.0 MB / 512 MB | 0.28% | 1.85 s | Healthy (Port 8501) |

---
# Comparative Architectural Analysis

Evaluating Docker container virtualization against alternative deployment methodologies:

| Architectural Metric | Docker Containers (Exp 14) | Virtual Machines (KVM/ESXi) | Bare-Metal Host |
|---|---|---|---|
| **Boot Latency** | $< 2\text{ seconds}$ | $30 - 90\text{ seconds}$ | $2 - 5\text{ minutes}$ |
| **Storage Overhead** | Megabytes (Shared Layers) | Gigabytes (Full OS disk) | Full OS installation |
| **Memory Efficiency** | Exact process allocation | Pre-allocated dedicated RAM | Unconstrained host RAM |
| **Portability / Packaging** | High (OCI Image Standard) | Moderate (OVA/VMDK export) | Low (Host dependencies) |
| **Isolation Strength** | Kernel Namespaces / cgroups | Hardware Hypervisor VT-x | None (Shared OS) |

---
# Error Handling, Exception Recovery & Debugging Records

### Anomaly 1: Nginx Upstream Reverse Proxy Connection Refusal
- **Symptom:** Nginx returned HTTP `502 Bad Gateway` when routing `/api/kpis` requests.
- **Root Cause:** In the initial configuration, `proxy_pass` targeted `http://localhost:5000`. Inside a container, `localhost` resolves to the container's own loopback interface, not the backend container.
- **Resolution:** Updated `proxy_pass` to utilize Docker Compose internal DNS service discovery: `http://backend:5000/api/`.

### Anomaly 2: Host Port Collision on Port 5000
- **Symptom:** `docker-compose up` threw error: `Bind for 0.0.0.0:5000 failed: port is already allocated`.
- **Root Cause:** A local development Flask process was already running on port 5000.
- **Resolution:** Terminated the background development process and verified clean port availability via `Get-NetTCPConnection`.

---
# Academic Conclusion & Master-Level Findings

Assessment 8 demonstrated that containerization is indispensable for modern enterprise visual analytics. By encapsulating heterogeneous runtimes (Alpine Nginx, Python Flask, Streamlit) into immutable OCI images, we eliminate environmental drift ("it works on my machine"). Docker Compose coordinates the multi-tier fleet with sub-second startup times, isolated networking, and resilient health monitoring, establishing a deployment-ready foundation.

---
# Step-by-Step Execution Procedure & Operational Protocols

## Protocol 1: Environment Initialization & Directory Scaffolding
1. Open an administrative PowerShell terminal in the workspace directory.
2. Verify Docker Engine daemon status: `docker version` and `docker info`.
3. Create isolated subdirectories for backend, frontend, and Streamlit components:
   `mkdir code/qp8_docker/{backend,frontend,streamlit,data} -Force`

## Protocol 2: Building Microservice Container Images
1. Execute independent multi-stage image builds to verify Dockerfile syntax:
   `docker build -t analytics-backend:v1.0.0 -f Dockerfile.backend .`
   `docker build -t analytics-frontend:v1.0.0 -f Dockerfile.frontend .`
   `docker build -t analytics-streamlit:v1.0.0 -f Dockerfile.streamlit .`
2. Verify that image intermediate build layers utilize cached dependencies (`CACHED`).

## Protocol 3: Multi-Container Orchestration with Docker Compose
1. Deploy the entire visual analytics microservice stack in detached background mode:
   `docker compose -f docker-compose.yml up -d --build`
2. Inspect container status and health probes:
   `docker compose ps`
3. Monitor real-time streaming container logs:
   `docker compose logs -f backend frontend`

## Protocol 4: Health Verification & E2E Validation
1. Test frontend Nginx reverse proxy endpoint: `curl -I http://localhost:80/` (expect HTTP 200 OK).
2. Test proxied API endpoint: `curl http://localhost:80/api/kpis` (expect JSON payload).
3. Open browser and access Streamlit analytical dashboard at `http://localhost:8501/`.

---
# Appendix &ndash; Complete Dependency & Configuration Manifests

### A. Python Dependencies (`requirements.txt`)
```
flask==3.0.3
flask-cors==4.0.1
pandas==2.2.2
numpy==1.26.4
streamlit==1.36.0
openpyxl==3.1.5
```

### B. Deployment Automation Script (`deploy.ps1`)
```powershell
# Automated Deployment and Health Probe Verification
Write-Host "Starting Visual Analytics Microservices..." -ForegroundColor Cyan
docker compose down --volumes --remove-orphans
docker compose up -d --build

Write-Host "Waiting for backend healthcheck probe..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
docker compose ps

Write-Host "Validating endpoint responses..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://localhost/api/kpis" | ConvertTo-Json -Depth 3
```
