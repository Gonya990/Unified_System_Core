#!/bin/bash
PROJECT_ID="my-home-435112"
SERVICE_NAME="connect-landing-page"
REGION="us-central1"

echo "Building and deploying $SERVICE_NAME to GCP..."

# Build the image using Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run-source-lib/$SERVICE_NAME --project $PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run-source-lib/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --project $PROJECT_ID

echo "Deployment complete!"
