# Python Microservice Template

This template provides a starting point for new Python microservices in the Unified System Core.

## Features
- FastAPI web framework
- Google Cloud Logging integration
- Docker containerization
- Kubernetes deployment manifests
- Health check endpoint

## Usage
1. Copy this template to a new directory
2. Update `app.py` with your service logic
3. Update `requirements.txt` with dependencies
4. Update `deployment.yaml` with correct image and secrets
5. Build and deploy

## Deployment
Use the provided `deployment.yaml` for GKE deployment.
Ensure secrets are created in GCP Secret Manager and referenced in the manifest.
