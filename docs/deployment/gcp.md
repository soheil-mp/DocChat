# Google Cloud Platform Deployment Guide

## Prerequisites
- GCP Account
- gcloud CLI installed
- Docker installed
- Domain name (optional)

## Infrastructure Setup

### 1. Container Registry Setup
    # Configure Docker for GCP
    gcloud auth configure-docker

    # Enable required APIs
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable container.googleapis.com

### 2. GKE Cluster Creation
    # Create GKE cluster
    gcloud container clusters create docuchat-cluster \
        --num-nodes=3 \
        --machine-type=e2-medium \
        --region=us-central1

### 3. Cloud Storage Setup
    # Create bucket for documents
    gsutil mb gs://docuchat-documents

    # Enable versioning
    gsutil versioning set on gs://docuchat-documents

## Application Deployment

### 1. Build and Push Docker Images
    # Build and push images
    docker build -t gcr.io/project-id/docuchat-backend -f deploy/docker/Dockerfile.backend .
    docker push gcr.io/project-id/docuchat-backend

### 2. Kubernetes Deployment
1. Apply configurations
2. Set up ingress
3. Configure SSL
4. Set up monitoring

## Monitoring and Maintenance

### Cloud Monitoring Setup
- Configure logging
- Set up alerts
- Create dashboards

### Backup Strategy
- Configure Cloud Storage lifecycle
- Set up database backups
- Create disaster recovery plan 