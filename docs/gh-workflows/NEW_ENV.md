# Guide to create a completely new environment
This guide will proportion general links on how to create 
the necessary variables and information to make use of the github actions for creating a new environment.

## pre-tf-setup
### 1. [Create the Azure Credentials](https://learn.microsoft.com/en-us/cli/azure/azure-cli-sp-tutorial-1?view=azure-cli-latest&tabs=bash#create-a-service-principal)
Get the subscription id for the scope, narrow the scope to your need:
```bash
az account list --output table
```
Create the service principal:
```bash
az ad sp create-for-rbac --name learn-kedro --role contributor --scopes /subscriptions/<subscription-id>
```
Narrow the role access by using any of the role ids here: 
[Available Roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage)

Output example:
```json
{
  "appId": "myAppId",
  "displayName": "learn-kedro",
  "password": "myServicePrincipalPassword",
  "tenant": "myTentantId"
}
```
### 2. [Follow Steps for AZ CLI Secrets](https://learn.microsoft.com/en-us/cli/azure/azure-cli-sp-tutorial-1?view=azure-cli-latest&tabs=bash#create-a-service-principal)
