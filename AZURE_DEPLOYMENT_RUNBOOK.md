# Azure Deployment Runbook

## WellnessAI - Production Deployment Guide

This runbook covers deploying the Holistic Wellness AI Coach to Azure using **Azure App Service** for the backend and **Azure Static Web Apps** for the frontend.

---

## Prerequisites

- Azure CLI installed (`az --version`)
- Azure subscription with active billing
- Google Gemini API key
- Git repository with your code

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "YOUR_SUBSCRIPTION_NAME"
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Azure Cloud                             │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────────┐     │
│  │  Azure Static       │    │  Azure App Service      │     │
│  │  Web Apps           │───▶│  (Python Flask)         │     │
│  │  (Frontend)         │    │  (Backend API)          │     │
│  │                     │    │                         │     │
│  │  - index.html       │    │  - app.py               │     │
│  │  - style.css        │    │  - decision_making.py   │     │
│  │  - script.js        │    │  - perception.py        │     │
│  └─────────────────────┘    │  - action.py            │     │
│                             └───────────┬─────────────┘     │
│                                         │                   │
│  ┌─────────────────────┐                │                   │
│  │  Azure Key Vault    │◀───────────────┘                   │
│  │  (Secrets)          │                                    │
│  │  - GEMINI_API_KEY   │                                    │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │  Google Gemini API            │
              │  (External)                   │
              └───────────────────────────────┘
```

---

## Step 1: Create Resource Group

```bash
# Variables - customize these
RESOURCE_GROUP="wellnessai-rg"
LOCATION="eastus"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

---

## Step 2: Deploy Backend (Azure App Service)

### 2.1 Create App Service Plan

```bash
APP_SERVICE_PLAN="wellnessai-plan"
BACKEND_APP_NAME="wellnessai-api"  # Must be globally unique

# Create App Service Plan (B1 is the minimum for production)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux
```

### 2.2 Create Web App

```bash
# Create the web app with Python 3.11 runtime
az webapp create \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON:3.11"
```

### 2.3 Configure Environment Variables

```bash
# Set the Gemini API key as an environment variable
az webapp config appsettings set \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings GEMINI_API_KEY="your-gemini-api-key-here"

# Set startup command
az webapp config set \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 120 app:app"
```

### 2.4 Prepare Backend for Deployment

Create a `startup.txt` in the backend folder:

```bash
gunicorn --bind=0.0.0.0 --timeout 120 app:app
```

Update `requirements.txt` to include gunicorn:

```txt
flask
flask-cors
google-generativeai
pydantic
python-dotenv
gunicorn
```

### 2.5 Deploy Backend Code

```bash
# Navigate to backend directory
cd /Users/gowtham/Downloads/EAG/Assignment6/backend

# Deploy using ZIP deployment
zip -r backend.zip . -x "*.pyc" -x "__pycache__/*" -x ".env"

az webapp deployment source config-zip \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --src backend.zip

# Clean up
rm backend.zip
```

### 2.6 Enable CORS

```bash
# Get your frontend URL (will be set after frontend deployment)
# For now, allow all origins during testing
az webapp cors add \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --allowed-origins "*"
```

### 2.7 Verify Backend Deployment

```bash
# Get the backend URL
BACKEND_URL="https://${BACKEND_APP_NAME}.azurewebsites.net"
echo "Backend URL: $BACKEND_URL"

# Test the API
curl $BACKEND_URL
```

Expected response:
```json
{
  "message": "Wellness Plan API",
  "endpoints": {...}
}
```

---

## Step 3: Deploy Frontend (Azure Static Web Apps)

### 3.1 Update Frontend API URL

Before deploying, update `script.js` to point to your Azure backend:

```javascript
// Change this line in script.js
const response = await fetch('https://wellnessai-api.azurewebsites.net/api/generate-plan', {
```

### 3.2 Create Static Web App

```bash
FRONTEND_APP_NAME="wellnessai-frontend"

# Create Static Web App
az staticwebapp create \
  --name $FRONTEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --source "." \
  --branch "main" \
  --app-location "/frontend" \
  --output-location "" \
  --login-with-github
```

### 3.3 Alternative: Manual Deployment

If not using GitHub integration:

```bash
# Navigate to frontend directory
cd /Users/gowtham/Downloads/EAG/Assignment6/frontend

# Install SWA CLI
npm install -g @azure/static-web-apps-cli

# Deploy
swa deploy . --deployment-token <YOUR_DEPLOYMENT_TOKEN>
```

To get the deployment token:
```bash
az staticwebapp secrets list \
  --name $FRONTEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.apiKey" -o tsv
```

### 3.4 Verify Frontend Deployment

```bash
# Get the frontend URL
az staticwebapp show \
  --name $FRONTEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "defaultHostname" -o tsv
```

---

## Step 4: Secure with Azure Key Vault (Recommended)

### 4.1 Create Key Vault

```bash
KEY_VAULT_NAME="wellnessai-kv"  # Must be globally unique

az keyvault create \
  --name $KEY_VAULT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

### 4.2 Store Secrets

```bash
az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "GEMINI-API-KEY" \
  --value "your-gemini-api-key-here"
```

### 4.3 Grant App Service Access

```bash
# Enable managed identity for App Service
az webapp identity assign \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP

# Get the principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

# Grant access to Key Vault
az keyvault set-policy \
  --name $KEY_VAULT_NAME \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

### 4.4 Update App Settings to Use Key Vault Reference

```bash
az webapp config appsettings set \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings GEMINI_API_KEY="@Microsoft.KeyVault(VaultName=${KEY_VAULT_NAME};SecretName=GEMINI-API-KEY)"
```

---

## Step 5: Configure Custom Domain (Optional)

### 5.1 Backend Custom Domain

```bash
CUSTOM_DOMAIN="api.wellnessai.com"

# Add custom domain
az webapp config hostname add \
  --webapp-name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --hostname $CUSTOM_DOMAIN

# Create managed certificate
az webapp config ssl create \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --hostname $CUSTOM_DOMAIN

# Bind SSL certificate
az webapp config ssl bind \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --certificate-thumbprint <THUMBPRINT> \
  --ssl-type SNI
```

---

## Step 6: Set Up CI/CD with GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'wellnessai-api'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: './backend'

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Azure Static Web Apps
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/frontend"
          output_location: ""
```

---

## Step 7: Monitoring & Logging

### 7.1 Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app wellnessai-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --application-type web

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app wellnessai-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Add to App Service
az webapp config appsettings set \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### 7.2 View Logs

```bash
# Stream live logs
az webapp log tail \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --log-file logs.zip
```

---

## Step 8: Scaling (Production)

### 8.1 Scale Up (Vertical)

```bash
# Upgrade to Standard tier for auto-scaling
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku S1
```

### 8.2 Scale Out (Horizontal)

```bash
# Manual scale to 3 instances
az webapp scale \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --instance-count 3

# Or configure auto-scaling
az monitor autoscale create \
  --resource-group $RESOURCE_GROUP \
  --resource $BACKEND_APP_NAME \
  --resource-type Microsoft.Web/sites \
  --name wellnessai-autoscale \
  --min-count 1 \
  --max-count 10 \
  --count 2
```

---

## Quick Reference: All URLs

| Service | URL |
|---------|-----|
| **Backend API** | `https://wellnessai-api.azurewebsites.net` |
| **Frontend** | `https://<your-static-app>.azurestaticapps.net` |
| **Azure Portal** | `https://portal.azure.com` |

---

## Troubleshooting

### Backend not starting
```bash
# Check logs
az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP

# Restart app
az webapp restart --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP
```

### CORS errors
```bash
# Update CORS with specific frontend URL
az webapp cors remove --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --allowed-origins "*"
az webapp cors add --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --allowed-origins "https://your-frontend.azurestaticapps.net"
```

### API key not working
```bash
# Verify environment variable is set
az webapp config appsettings list --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP
```

---

## Cost Estimate (Monthly)

| Resource | SKU | Est. Cost |
|----------|-----|-----------|
| App Service Plan | B1 | ~$13 |
| Static Web Apps | Free | $0 |
| Key Vault | Standard | ~$0.03/10K ops |
| Application Insights | Free tier | $0 |
| **Total** | | **~$15/month** |

For production with S1 plan: ~$70/month

---

## Cleanup

To delete all resources:

```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

*Last updated: December 2025*
