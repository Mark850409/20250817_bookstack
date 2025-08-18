---
title: AzureDevops-LangFlowChatBot流程部署筆記
created: 2025-01-09 21:24:00Z
tags:
  - AI
  - 人工智慧
  - LangFlow
  - LangChain
  - LINEBOT
  - Azure
---
# 1. AzureDevops-LangFlowChatBot流程部署筆記

## 1.1. 簡介

這個 Azure DevOps 腳本是用來自動化部署 Azure 資源、建立容器映像檔，並部署應用程式和容器執行個體的完整流程。以下是它的重點分解：

### 1.1.1. 重點功能

1.  **觸發條件**
    *   當有任何分支更新時，觸發管線。
2.  **部署 Azure 資源階段**
    *   驗證 Azure 登入和檢查服務主體的角色權限。
    *   檢查資源群組是否存在，若不存在則創建。
    *   建立 Azure 儲存帳戶與檔案分享。
3.  **建立 Azure 容器登錄服務 (ACR)**
    *   驗證 Azure 登入並切換訂閱。
    *   檢查 ACR 是否存在，不存在則創建。
    *   賦予服務主體對 ACR 的拉取權限。
4.  **建置與推送 Docker 映像檔**
    *   使用 Docker 建置容器映像檔。
    *   標籤並將映像檔推送到 ACR。
    *   驗證推送是否成功。
5.  **部署 Azure 容器執行個體**
    *   創建容器執行個體，並掛載 Azure File Share 作為資料卷。
    *   配置容器的 CPU、記憶體、埠號及 DNS 名稱。
6.  **部署 Azure Functions**
    *   創建 Azure Functions 的應用服務計劃。
    *   創建 Function App 並配置 Python 3.11 環境。
    *   將程式碼壓縮為 ZIP 文件，並透過 ZIP 部署至 Function App。

### 1.1.2. 其他細節

*   **環境配置**
    *   使用變數來管理資源名稱（例如：資源群組、位置、儲存帳戶、ACR 名稱等）。
    *   指定作業系統類型為 Linux。
*   **錯誤處理**
    *   驗證每個資源是否成功創建，若失敗則中止部署。
*   **依賴性管理**
    *   `PushContainerImage` 階段依賴 `CreateContainerRegistry` 階段完成後執行。
    *   `DeployContainer` 階段依賴於 `DeployResources` 和 `PushContainerImage` 階段完成後執行。
這個腳本適合需要在 Azure 上自動部署資源、容器和功能應用的完整 CI/CD 流程。

## 1.2. 目錄

- [1. AzureDevops-LangFlowChatBot流程部署筆記](#1-azuredevops-langflowchatbot流程部署筆記)
  - [1.1. 簡介](#11-簡介)
    - [1.1.1. 重點功能](#111-重點功能)
    - [1.1.2. 其他細節](#112-其他細節)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 完成畫面](#13-完成畫面)
  - [1.4. 操作步驟](#14-操作步驟)
    - [1.4.1. 建立用於登入Azure的Service connetions](#141-建立用於登入azure的service-connetions)
    - [1.4.2. Azure應用程式註冊](#142-azure應用程式註冊)
    - [1.4.3. 賦予資源群組權限](#143-賦予資源群組權限)
      - [1.4.3.1. 登錄 Azure](#1431-登錄-azure)
      - [1.4.3.2. 列出指定使用者的角色指派](#1432-列出指定使用者的角色指派)
      - [1.4.3.3. 建立角色指派](#1433-建立角色指派)
      - [1.4.3.4. 列出指定範圍的角色指派](#1434-列出指定範圍的角色指派)
    - [1.4.4. 撰寫`azure-pipelines.yml`](#144-撰寫azure-pipelinesyml)
  - [1.5. Azure DevOps Pipeline（指令解釋）](#15-azure-devops-pipeline指令解釋)
    - [1.5.1. 基本變數](#151-基本變數)
    - [1.5.2. 登錄 Azure](#152-登錄-azure)
    - [1.5.3. 列出指定使用者的角色指派](#153-列出指定使用者的角色指派)
    - [1.5.4. 建立角色指派](#154-建立角色指派)
    - [1.5.5. 列出指定範圍的角色指派](#155-列出指定範圍的角色指派)
    - [1.5.6. 查詢應用程式資訊](#156-查詢應用程式資訊)
    - [1.5.7. 建立資源群組](#157-建立資源群組)
    - [1.5.8. 創建 Function App](#158-創建-function-app)
    - [1.5.9. 部署 ZIP 檔案到 Function App](#159-部署-zip-檔案到-function-app)
    - [1.5.10. 查看 Function App 日誌](#1510-查看-function-app-日誌)
    - [1.5.11. 建立容器實例](#1511-建立容器實例)
    - [1.5.12. 查詢容器註冊資訊](#1512-查詢容器註冊資訊)
    - [1.5.13. 指派 ACR 拉取權限](#1513-指派-acr-拉取權限)
    - [1.5.14. 建立 App Service 計劃](#1514-建立-app-service-計劃)
    - [1.5.15. 設定環境變數](#1515-設定環境變數)

## 1.3. 完成畫面

![](https://markweb.idv.tw/uploads/2025-01/202501092118414.png)

![](https://markweb.idv.tw/uploads/2025-01/202501092118454.png)


<!--more-->
## 1.4. 操作步驟

### 1.4.1. 建立用於登入Azure的Service connetions

![](https://markweb.idv.tw/uploads/2025-01/202501092009355.png)


![](https://markweb.idv.tw/uploads/2025-01/202501092010417.png)


![](https://markweb.idv.tw/uploads/2025-01/202501092010684.png)


![](https://markweb.idv.tw/uploads/2025-01/202501092011935.png)

### 1.4.2. Azure應用程式註冊

AZURE_CLIENT_ID (Application ID)
1. 登入 Azure Portal。
2. 前往 Azure Active Directory > 應用程式註冊 (App registrations)。
3. 在應用程式註冊頁面找到服務主體的名稱，並點擊進入。
4. 在概覽頁面下可以看到 應用程式 (客戶端) ID (Application (client) ID)。
5. 這個值對應 AZURE_CLIENT_ID。

---

AZURE_TENANT_ID
1. 同樣在應用程式註冊的概覽頁面，可以看到 目錄 (租戶) ID (Directory (tenant) ID)。
2. 這個值對應 AZURE_TENANT_ID。

---

AZURE_CLIENT_SECRET

> [!NOTE]
> 注意：只能查看已生成的金鑰（Secret）一次，無法直接查詢已創建的金鑰值。如果需要新的 Secret，需重新生成。


1. 在應用程式註冊的頁面，選擇`憑證與密碼 (Certificates & secrets)`。
2. 找到 用戶端密碼 (Client secrets) 區塊。
3. 如果已有密碼，它只在創建當下可見，若已過期或無法取得，需要生成新的。
4. 點擊 新用戶端密碼 (New client secret)。
5. 輸入說明文字並選擇到期時間，點擊 新增。
6. 新增後，系統會顯示值 (Value)，立即複製並保存，這是 AZURE_CLIENT_SECRET。

### 1.4.3. 賦予資源群組權限

> [!NOTE]
> 請在地端先安裝好Azure cli或是直接在Azure Cloud Shell裡面執行

#### 1.4.3.1. 登錄 Azure

如果已成功登入，會返回當前帳戶資訊（例如訂閱 ID、帳戶名稱）。

```bash
az account show
```

如果您的帳戶有多個 Azure 訂閱，可以使用以下命令切換：

```bash
az account list --output table
```
找到您需要使用的訂閱 ID，然後執行：

```bash
az account set --subscription <SubscriptionId>
```
檢查可用的資源群組：
```bash
az group list --output table
```
創建資源群組：
```bash
az group create --name MyResourceGroup --location eastus
```

#### 1.4.3.2. 列出指定使用者的角色指派

```bash
az role assignment list \
  --assignee $AZURE_CLIENT_ID \
  --query "[].{Role:roleDefinitionName, Scope:scope}" -o table
```

#### 1.4.3.3. 建立角色指派

```bash
az role assignment create \
  --assignee $AZURE_CLIENT_ID \
  --role Contributor \
  --scope /subscriptions/<YOUR_AZURE_SUBSCRIPTION_ID>
```

- **Contributor**：允許使用者進行資源管理。
- **Scope**：定義角色指派的範圍。

#### 1.4.3.4. 列出指定範圍的角色指派

```bash
az role assignment list \
  --scope /subscriptions/<YOUR_AZURE_SUBSCRIPTION_ID>/resourceGroups/<YOUR_AZURE_RESOURSE_ID>
```

### 1.4.4. 撰寫`azure-pipelines.yml`
```yaml
trigger:
- '*'

variables:
  - group: AzureCredentials
  - name: azureServiceConnection
    value: "MyLangFlowConnection"  # 替換為您的 Azure Service Connection 名稱
  - name: subscriptionId
    value: "e7736fb9-bed4-4d1d-96d2-c79eb2c181c4"        # 替換為您的 Azure 訂閱 ID
  - name: resourceGroup
    value: "langflowdevopsgroup"
  - name: location
    value: "eastus"
  - name: containerRegistryName
    value: "mylangflowregistry"
  - name: containerInstanceName
    value: "mylangflowinstance"
  - name: containerCPUCounts
    value: "1"
  - name: containerMemoryCounts
    value: "2"
  - name: containerPorts
    value: "7860"
  - name: containerAddress
    value: "Public"
  - name: containerDNSName
    value: "mylangflowdevops" # 修正 DNS 名稱格式
  - name: storageAccountName
    value: "mylangflowstorageaccount"
  - name: fileShareName
    value: "mylangflowshare"
  - name: containerImage
    value: "mylangflowimage:latest"
  - name: functionAppName
    value: "mylangflowfunctionapp"


stages:
- stage: DeployResources
  displayName: "Deploy Azure Resources"
  jobs:
  - job: CreateResources
    displayName: "Create Azure Resources"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: AzureCLI@2
      displayName: "Login to Azure and Verify Permissions"
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          echo "Verifying Service Principal Permissions..."
          az account show --query "{Subscription: id, Tenant: tenantId}"
          az role assignment list --assignee $AZURE_CLIENT_ID --query [].roleDefinitionName -o table
    - task: AzureCLI@2
      displayName: "check Service Principal "
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: 'bash'
        scriptLocation: 'inlineScript'
        inlineScript: |
          az account show
    - task: AzureCLI@2
      displayName: "Check and Create Resource Group"
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          echo "Resource Group Name: ${{ variables.resourceGroup }}"
          echo "Checking if Resource Group exists..."
          resource_group_exists=$(az group exists --name ${{ variables.resourceGroup }})
          echo "az group exists returned: $resource_group_exists"
          if [ "$resource_group_exists" == "true" ]; then
              echo "Resource group ${{ variables.resourceGroup }} already exists."
          else
              echo "Resource group ${{ variables.resourceGroup }} does not exist. Attempting to create..."
              az group create --name ${{ variables.resourceGroup }} --location ${{ variables.location }}
              if [ $? -eq 0 ]; then
                  echo "Resource group ${{ variables.resourceGroup }} created successfully."
              else
                  echo "Failed to create resource group ${{ variables.resourceGroup }}."
                  exit 1
              fi
          fi


    - task: AzureCLI@2
      displayName: "Create Azure Storage Account"
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          echo "Creating Storage Account..."
          az storage account create \
            --name ${{ variables.storageAccountName }} \
            --resource-group ${{ variables.resourceGroup }} \
            --location ${{ variables.location }} \
            --sku Standard_LRS

    - task: AzureCLI@2
      displayName: "Create Azure File Share"
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          echo "Creating Azure File Share..."
          az storage share-rm create \
            --name ${{ variables.fileShareName }} \
            --storage-account ${{ variables.storageAccountName }} \
            --resource-group ${{ variables.resourceGroup }}

- stage: CreateContainerRegistry
  displayName: "Check and Create Azure Container Registry"
  jobs:
  - job: CheckAndCreateACR
    displayName: "Check and Create ACR"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - script: |
        echo "Logging into Azure CLI..."
        az login --service-principal \
          --username $AZURE_CLIENT_ID \
          --password $AZURE_CLIENT_SECRET \
          --tenant $AZURE_TENANT_ID || { echo "Login failed"; exit 1; }

        echo "Switching to Azure subscription..."
        az account set --subscription ${{ variables.subscriptionId }}

        echo "Checking if Azure Container Registry exists..."
        acr_exists=$(az acr list --query "[?name=='${{ variables.containerRegistryName }}'].name" -o tsv)
        if [ -z "$acr_exists" ]; then
          echo "Azure Container Registry ${{ variables.containerRegistryName }} does not exist. Creating..."
          az acr create --name ${{ variables.containerRegistryName }} --resource-group ${{ variables.resourceGroup }} --sku Basic --location ${{ variables.location }}
          if [ $? -eq 0 ]; then
            echo "Azure Container Registry ${{ variables.containerRegistryName }} created successfully."
          else
            echo "Failed to create Azure Container Registry."
            exit 1
          fi
        else
          echo "Azure Container Registry ${{ variables.containerRegistryName }} already exists."
        fi
        echo "Granting ACR pull permissions to the container instance..."
          az role assignment create \
            --assignee $AZURE_CLIENT_ID \
            --scope $(az acr show --name $(containerRegistryName) --query id -o tsv) \
            --role AcrPull || { echo "Failed to assign ACR pull role"; exit 1; }
      displayName: "Check and Create ACR"

- stage: PushContainerImage
  displayName: "Build and Push Docker Image to ACR"
  dependsOn: CreateContainerRegistry
  jobs:
  - job: BuildAndPushImage
    displayName: "Build and Push Docker Image"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - script: |
        echo "Logging into Azure CLI..."
            az login --service-principal \
              --username $AZURE_CLIENT_ID \
              --password $AZURE_CLIENT_SECRET \
              --tenant $AZURE_TENANT_ID || { echo "Login failed"; exit 1; }

        echo "Switching to Azure subscription..."
        az account set --subscription ${{ variables.subscriptionId }}

        echo "Logging into Azure Container Registry..."
        az acr login --name ${{ variables.containerRegistryName }}

        echo "Building Docker image..."
        docker build -t mylangflowimage:latest .

        echo "Checking if Docker image exists..."
        if docker images | grep -q "mylangflowimage"; then
          echo "Docker image 'mylangflowimage:latest' found. Proceeding to tag and push..."
        else
          echo "Docker image 'mylangflowimage:latest' not found. Build failed."
          exit 1
        fi

        echo "Tagging Docker image..."
        docker tag mylangflowimage:latest ${{ variables.containerRegistryName }}.azurecr.io/mylangflowimage:latest

        echo "Pushing Docker image to ACR..."
        docker push ${{ variables.containerRegistryName }}.azurecr.io/mylangflowimage:latest

        echo "Verifying Docker image in ACR..."
        az acr repository show --name ${{ variables.containerRegistryName }} --image mylangflowimage:latest
      displayName: "Build, Tag, and Push Docker Image to ACR"


- stage: DeployContainer
  displayName: "Deploy Container Instance"
  dependsOn: [DeployResources, PushContainerImage]  # 確保依賴 PushContainerImage
  jobs:
  - job: DeployContainerInstance
    displayName: "Deploy Container Instance"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: AzureCLI@2
      displayName: "Deploy Container Instance"
      inputs:
        azureSubscription: ${{ variables.azureServiceConnection }}
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          echo "Logging into Azure CLI..."
            az login --service-principal \
              --username $AZURE_CLIENT_ID \
              --password $AZURE_CLIENT_SECRET \
              --tenant $AZURE_TENANT_ID || { echo "Login failed"; exit 1; }

          echo "Switching to Azure subscription..."
          az account set --subscription ${{ variables.subscriptionId }}
          
          echo "Logging into Azure Container Registry..."
          az acr login --name ${{ variables.containerRegistryName }} || { echo "ACR login failed"; exit 1; }

          echo "Logging into Azure Container Registry..."
          az acr update -n $(containerRegistryName) --admin-enabled true

          echo "Fetching ACR credentials..."
          ACR_USERNAME=$(az acr credential show -n $(containerRegistryName) --query "username" -o tsv)
          ACR_PASSWORD=$(az acr credential show -n $(containerRegistryName) --query "passwords[0].value" -o tsv)

          echo "Fetching Storage Account Key..."
          storageKey=$(az storage account keys list --resource-group ${{ variables.resourceGroup }} --account-name ${{ variables.storageAccountName }} --query "[0].value" -o tsv)

          echo "Deploying Container Instance..."
          az container create \
            --resource-group ${{ variables.resourceGroup }} \
            --name ${{ variables.containerInstanceName }} \
            --image mylangflowregistry.azurecr.io/mylangflowimage:latest \
            --registry-login-server mylangflowregistry.azurecr.io \
            --registry-username $(az acr credential show --name mylangflowregistry --query "username" -o tsv) \
            --registry-password $(az acr credential show --name mylangflowregistry --query "passwords[0].value" -o tsv) \
            --cpu ${{ variables.containerCPUCounts }} \
            --memory ${{ variables.containerMemoryCounts }} \
            --ports ${{ variables.containerPorts }} \
            --ip-address ${{ variables.containerAddress }} \
            --dns-name-label ${{ variables.containerDNSName }} \
            --azure-file-volume-account-name ${{ variables.storageAccountName }} \
            --azure-file-volume-account-key $storageKey \
            --azure-file-volume-share-name ${{ variables.fileShareName }} \
            --azure-file-volume-mount-path /mnt/data \
            --os-type Linux  # 添加這行來指定作業系統類型


- stage: DeployFunctionApp
  displayName: "Deploy Azure Function App"
  jobs:
  - job: DeployFunction
    displayName: "Deploy Azure Function App"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: AzureCLI@2
      displayName: "Create and Deploy Function App"
      inputs:
        azureSubscription: $(azureServiceConnection)
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          # 設定變數
          FUNCTION_APP_NAME="$(functionAppName)"
          RESOURCE_GROUP="$(resourceGroup)"
          LOCATION="$(location)"
          STORAGE_ACCOUNT_NAME="$(storageAccountName)"
          APP_SERVICE_PLAN_NAME="mylangflowappservice"
          RUNTIME="python"
          RUNTIME_VERSION="3.11"
          FUNCTIONS_VERSION="4"

          # 確認變數是否存在
          if [ -z "$FUNCTION_APP_NAME" ] || [ -z "$RESOURCE_GROUP" ] || [ -z "$LOCATION" ] || [ -z "$STORAGE_ACCOUNT_NAME" ]; then
            echo "One or more required variables are not defined."
            exit 1
          fi

          echo "Creating App Service Plan..."
          az appservice plan create \
            --name $APP_SERVICE_PLAN_NAME \
            --resource-group $RESOURCE_GROUP \
            --location $LOCATION \
            --sku B1 \
            --is-linux

          # 創建 Function App
          echo "Creating Function App..."
          az functionapp create \
            --name $FUNCTION_APP_NAME \
            --resource-group $RESOURCE_GROUP \
            --storage-account $STORAGE_ACCOUNT_NAME \
            --plan $APP_SERVICE_PLAN_NAME \
            --runtime $RUNTIME \
            --runtime-version $RUNTIME_VERSION \
            --functions-version $FUNCTIONS_VERSION \
            --os-type Linux
          
          echo "Deploying Function App..."
          zip -r function_app.zip .
          echo "Zip File: $(ls -l function_app.zip)"
          az functionapp deployment source config-zip \
            --name $FUNCTION_APP_NAME \
            --resource-group $RESOURCE_GROUP \
            --src function_app.zip

```

## 1.5. Azure DevOps Pipeline（指令解釋）

### 1.5.1. 基本變數

```bash
AZURE_CLIENT_ID="<Azure 應用程式的客戶端 ID>"   # Azure 應用程式的客戶端 ID
AZURE_CLIENT_SECRET="<Azure 應用程式的客戶端密鑰>" # Azure 應用程式的客戶端密鑰
AZURE_TENANT_ID="<Azure 租戶 ID>"  # Azure 租戶 ID
```

### 1.5.2. 登錄 Azure

```bash
az login --service-principal \
  --username $AZURE_CLIENT_ID \
  --password $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID
```

### 1.5.3. 列出指定使用者的角色指派

```bash
az role assignment list \
  --assignee $AZURE_CLIENT_ID \
  --query "[].{Role:roleDefinitionName, Scope:scope}" -o table
```

### 1.5.4. 建立角色指派

```bash
az role assignment create \
  --assignee $AZURE_CLIENT_ID \
  --role Contributor \
  --scope /subscriptions/<YOUR_AZURE_SUBSCRIPTION_ID>
```

- **Contributor**：允許使用者進行資源管理。
- **Scope**：定義角色指派的範圍。

### 1.5.5. 列出指定範圍的角色指派

```bash
az role assignment list \
  --scope /subscriptions/<YOUR_AZURE_SUBSCRIPTION_ID>/resourceGroups/<YOUR_AZURE_RESOURSE_ID>
```

### 1.5.6. 查詢應用程式資訊

```bash
az ad sp show --id $AZURE_CLIENT_ID
```

- **--query id -o tsv**：僅返回應用程式的 ID。

### 1.5.7. 建立資源群組

```bash
az group create \
  --name LangFlowDevopsGroup \
  --location eastus
```

### 1.5.8. 創建 Function App

```bash
az functionapp create \
  --resource-group LangFlowDevopsGroup \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name myfirstazurefunction1 \
  --storage-account mylangflowstorageaccount \
  --os-type Linux
```

- **--consumption-plan-location**：定義計費方案的地區。
- **--runtime**：指定執行時環境。

### 1.5.9. 部署 ZIP 檔案到 Function App

```bash
az functionapp deployment source config-zip \
  --name mylangflowfunctionapp \
  --resource-group LangFlowDevopsGroup \
  --src function_app.zip
```

### 1.5.10. 查看 Function App 日誌

```bash
az functionapp log tail \
  --name mylangflowfunctionapp \
  --resource-group LangFlowDevopsGroup
```

### 1.5.11. 建立容器實例

```bash
az container create \
  --resource-group LangFlowDevopsGroup \
  --name myContainer \
  --image myImage \
  --cpu 1 \
  --memory 1.5 \
  --ports 80 \
  --ip-address Public \
  --dns-name-label mycontainerdns \
  --os-type Linux
```

### 1.5.12. 查詢容器註冊資訊

```bash
az acr show \
  --name mylangflowregistry \
  --query id -o tsv
```

### 1.5.13. 指派 ACR 拉取權限

```bash
az role assignment create \
  --assignee $AZURE_CLIENT_ID \
  --scope /subscriptions/<YOUR_AZURE_SUBSCRIPTION_ID>/resourceGroups/LangFlowDevopsGroup/providers/Microsoft.ContainerRegistry/registries/mylangflowregistry \
  --role AcrPull
```

- **AcrPull**：允許從 Azure Container Registry 拉取映像。

### 1.5.14. 建立 App Service 計劃

```bash
echo "Creating App Service Plan..."
az appservice plan create \
  --name mylangflowfunctionapp4 \
  --resource-group LangFlowDevopsGroup \
  --location eastus \
  --sku B1 \
  --is-linux
```

### 1.5.15. 設定環境變數

點擊`Pipelines>Library`，建立群組名稱與變數名稱
![](https://markweb.idv.tw/uploads/2025-01/202501092115206.png)


在`azure-pipelines.yml`加入此行即可使用
```yaml
variables:
  - group: AzureCredentials
```
