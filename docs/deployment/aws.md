# AWS Deployment Guide

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI configured locally
- Docker installed
- Domain name (optional)

## Infrastructure Setup

### 1. ECR Repository Setup
    # Create ECR repositories for frontend and backend
    aws ecr create-repository --repository-name DocChat-frontend
    aws ecr create-repository --repository-name DocChat-backend

### 2. ECS Cluster Creation
    # Create ECS cluster
    aws ecs create-cluster --cluster-name DocChat-cluster

### 3. MongoDB Atlas Setup
1. Create MongoDB Atlas cluster
2. Configure network access
3. Create database user
4. Get connection string

### 4. S3 Bucket for Documents
    # Create S3 bucket
    aws s3 mb s3://DocChat-documents
    
    # Enable versioning
    aws s3api put-bucket-versioning \
        --bucket DocChat-documents \
        --versioning-configuration Status=Enabled

## Application Deployment

### 1. Build and Push Docker Images
    # Login to ECR
    aws ecr get-login-password --region region | docker login --username AWS --password-stdin account-id.dkr.ecr.region.amazonaws.com

    # Build and push images
    docker build -t DocChat-backend -f deploy/docker/Dockerfile.backend .
    docker tag DocChat-backend:latest account-id.dkr.ecr.region.amazonaws.com/DocChat-backend:latest
    docker push account-id.dkr.ecr.region.amazonaws.com/DocChat-backend:latest

### 2. ECS Service Deployment
1. Create task definitions
2. Configure services
3. Set up load balancers
4. Configure auto-scaling

### 3. CloudFront Setup
1. Create distribution
2. Configure SSL certificate
3. Set up caching rules

### 4. Route53 Configuration
1. Create hosted zone
2. Configure DNS records
3. Set up health checks

## Monitoring and Maintenance

### CloudWatch Setup
    # Create log groups
    aws logs create-log-group --log-group-name /ecs/DocChat-backend
    aws logs create-log-group --log-group-name /ecs/DocChat-frontend

### Backup Configuration
- Configure S3 lifecycle rules
- Set up MongoDB Atlas backups
- Create backup retention policies

## Security Considerations
- Enable AWS WAF
- Configure security groups
- Set up IAM roles and policies
- Enable CloudTrail logging 