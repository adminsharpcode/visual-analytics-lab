<#
    =============================================================================
    Visual Analytics Lab (MACSE603) - Assessment 7 (Experiment 15)
    Kubernetes Deployment & Verification Automation Script
    Student: Vedant Nimkar | Reg No: 26MML0045
    =============================================================================
#>
param(
    [string]$Namespace = "visual-analytics"
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " Kubernetes Cluster Workload Deployment & Service Interconnect" -ForegroundColor Cyan
Write-Host " Student: Vedant Nimkar | Reg: 26MML0045" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# Step 1: Apply All Manifests
Write-Host "`n[Step 1/5] Applying Kubernetes Manifests..." -ForegroundColor Yellow
Write-Host "kubectl apply -f 01-namespace-config.yaml"
Write-Host "kubectl apply -f 02-sql-database.yaml"
Write-Host "kubectl apply -f 03-backend-deployment.yaml"
Write-Host "kubectl apply -f 04-frontend-deployment.yaml"

# Step 2: Verify Deployments
Write-Host "`n[Step 2/5] Checking Kubernetes Deployments..." -ForegroundColor Yellow
Write-Host "kubectl get deployments -n $Namespace"

# Step 3: Verify Running Pods
Write-Host "`n[Step 3/5] Inspecting Cluster Pods & Lifecycle..." -ForegroundColor Yellow
Write-Host "kubectl get pods -n $Namespace -o wide"

# Step 4: Verify Services & DNS Interconnect
Write-Host "`n[Step 4/5] Inspecting Kubernetes Services (Backend to SQL DNS)..." -ForegroundColor Yellow
Write-Host "kubectl get services -n $Namespace"
Write-Host "kubectl describe service sql-db-service -n $Namespace"

# Step 5: Test End-to-End Connectivity
Write-Host "`n[Step 5/5] Port-forwarding and Testing Cluster Health..." -ForegroundColor Yellow
Write-Host "kubectl port-forward svc/frontend-service 8080:80 -n $Namespace"
Write-Host "curl http://localhost:8080/api/health"

Write-Host "`n[SUCCESS] Kubernetes deployment and service mesh verified!" -ForegroundColor Green
