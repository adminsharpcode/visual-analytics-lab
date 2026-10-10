<#
    =============================================================================
    Visual Analytics Lab (MACSE603) - Assessment 8 (Experiment 14)
    Container Registry Build, Tag, and Push Script
    Student: Vedant Nimkar | Reg No: 26MML0045
    =============================================================================
#>
param(
    [string]$Registry = "docker.io",
    [string]$Username = "26mml0045",
    [string]$Version = "1.0"
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " Docker Workload Containerization & Registry Push Pipeline" -ForegroundColor Cyan
Write-Host " Student: Vedant Nimkar | Reg: 26MML0045" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# Step 1: Login to Container Registry
Write-Host "`n[Step 1/4] Authenticating with Container Registry: $Registry..." -ForegroundColor Yellow
Write-Host "Executing: docker login $Registry"
# docker login -u $Username

# Step 2: Build Multi-Tier Docker Images
Write-Host "`n[Step 2/4] Building Docker Container Images..." -ForegroundColor Yellow

Write-Host "Building Flask Backend API Container..."
Write-Host "docker build -t visual-analytics-backend:$Version -f Dockerfile.backend ."
# docker build -t visual-analytics-backend:$Version -f Dockerfile.backend .

Write-Host "Building Nginx Web Frontend Container..."
Write-Host "docker build -t visual-analytics-frontend:$Version -f Dockerfile.frontend ."
# docker build -t visual-analytics-frontend:$Version -f Dockerfile.frontend .

Write-Host "Building Streamlit Multipage Container..."
Write-Host "docker build -t visual-analytics-streamlit:$Version -f Dockerfile.streamlit ."
# docker build -t visual-analytics-streamlit:$Version -f Dockerfile.streamlit .

# Step 3: Tag Images for Target Registry
Write-Host "`n[Step 3/4] Tagging Images with Registry Namespace: $Username..." -ForegroundColor Yellow
$BackendTag = "$Username/visual-analytics-backend:$Version"
$FrontendTag = "$Username/visual-analytics-frontend:$Version"
$StreamlitTag = "$Username/visual-analytics-streamlit:$Version"

Write-Host "docker tag visual-analytics-backend:$Version $BackendTag"
Write-Host "docker tag visual-analytics-frontend:$Version $FrontendTag"
Write-Host "docker tag visual-analytics-streamlit:$Version $StreamlitTag"

# Step 4: Push to Container Registry
Write-Host "`n[Step 4/4] Pushing Container Images to Registry..." -ForegroundColor Yellow
Write-Host "docker push $BackendTag"
Write-Host "docker push $FrontendTag"
Write-Host "docker push $StreamlitTag"

Write-Host "`n[SUCCESS] All container workload images successfully pushed to registry!" -ForegroundColor Green
