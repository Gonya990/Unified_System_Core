#!/bin/bash
set -e

# Configuration
REGISTRY="gonya"
PROJECT_ROOT="/home/gonya/Unified_System_Core/Projects/Bybit_Bot"

# Services to build
declare -A SERVICES=(
    ["ingestion"]="services/ingestion"
    ["alpha"]="services/alpha"
    ["execution"]="services/execution"
    ["risk"]="services/risk"
    ["compliance"]="services/compliance"
)

# Build each service
for SERVICE_NAME in "${!SERVICES[@]}"; do
    SERVICE_PATH="${SERVICES[$SERVICE_NAME]}"
    FULL_IMAGE_NAME="${REGISTRY}/bybit-${SERVICE_NAME}:latest"
    
    echo "--- Building ${SERVICE_NAME} ---"
    # Using the project root as context so we can include 'common' folder
    docker build -t "$FULL_IMAGE_NAME" -f "${PROJECT_ROOT}/${SERVICE_PATH}/Dockerfile" "$PROJECT_ROOT"
    
    echo "Successfully built ${FULL_IMAGE_NAME}"
done

echo "All services built successfully locally."
