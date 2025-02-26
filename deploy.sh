#!/bin/bash

# IBM Cloud CLI login
ibmcloud login --apikey YOUR_IBM_CLOUD_API_KEY

# Target Cloud Functions namespace
ibmcloud target -g Default

# Deploy Backup Function
ibmcloud fn action create backup-function ibm_function_backup.py --kind python:3.7 --web true

# Deploy Recovery Function
ibmcloud fn action create recovery-function ibm_function_recovery.py --kind python:3.7 --web true

echo "Deployment completed successfully!"
