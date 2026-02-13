# Copilot Instructions for Unified System Core

## Project Overview
Unified System Core is a monorepo containing AI-powered microservices deployed on Google Kubernetes Engine (GKE). The system includes a Telegram bot, content factory, and various AI integrations.

## Architecture
- **AI Core**: Telegram bot with AI capabilities (Gemini, GitHub Models)
- **Content Factory**: Video/audio processing pipelines
- **Infrastructure**: GKE Autopilot, Cloud SQL, Secret Manager, Artifact Registry

## Key Technologies
- Python/FastAPI for services
- Kubernetes for orchestration
- Google Cloud Platform
- GitHub Actions for CI/CD
- Binary Authorization for security

## Coding Standards
- Use type hints
- Follow PEP 8
- Structured logging with JSON
- Health checks for all services
- RBAC with minimal privileges

## Deployment
- Automated via GitHub Actions
- Preview environments per PR
- Binary authorized images
- Secrets from GCP - Secrets from GCP - Secrets from GCP - Secrets from GCP - Secrets from GCP - Secrets from  f- Secrets from GCP - Secrets from GCP - Secing

## Development Workflow
1. Create feature branch
2. Implement with tests
3. Open PR for review
4. Preview environment deploys automatically
5. Merge after approval
6. Production deploy via CI/CD
