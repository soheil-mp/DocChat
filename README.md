
[![CC0 License](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=flat)](https://www.pinecone.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![LangChain](https://img.shields.io/badge/🦜%20LangChain-000000?style=flat)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Jest](https://img.shields.io/badge/Jest-C21325?style=flat&logo=jest&logoColor=white)](https://jestjs.io/)
[![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)


[Demo](#) · [Documentation](docs/) · [Report Bug](https://github.com/soheil-mp/DocChat/issues) · [Request Feature]([issues/](https://github.com/soheil-mp/DocChat/issues))

# DocChat 
> 🤖 An intelligent document Q&A chat interface powered by RAG (Retrieval-Augmented Generation) - transform your documents into interactive knowledge bases.

<div align="center">

![DocChat Demo](docs/assets/demo.png)

</div>

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#️-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#️-tech-stack)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Security](#-security)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

- 📄 **Smart Document Management**
  - Multi-format support (PDF, DOCX, TXT)
  - Batch uploads with progress tracking
  - Version control & metadata management

- 💬 **AI-Powered Chat**
  - Context-aware responses using RAG
  - Real-time interactions
  - Source citations
  - Conversation history

- ⚙️ **Customization**
  - Multiple LLM providers (OpenAI, Anthropic, Cohere)
  - Adjustable generation parameters
  - Custom prompting
  - Flexible output formatting

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- Python 3.8+
- MongoDB
- Pinecone account
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/DocChat.git
cd DocChat
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # Configure your environment variables
```

3. **Set up the frontend**
```bash
cd frontend
npm install
cp .env.example .env     # Configure your environment variables
```

### Running Locally

1. **Start the backend server**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Launch the frontend**
```bash
cd frontend
npm start
```

Visit [http://localhost:3000](http://localhost:3000) to see the application.

## 🏗️ Architecture

```mermaid
graph TD
    A[Client] -->|HTTP/WebSocket| B[FastAPI Backend]
    B -->|Document Storage| C[MongoDB]
    B -->|Vector Storage| D[Pinecone]
    B -->|RAG Pipeline| E[LangChain]
    E -->|LLM Requests| F[OpenAI]
```

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
DocChat/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── api/         # REST endpoints
│   │   ├── core/        # Core utilities
│   │   ├── services/    # Business logic
│   │   └── models/      # Data models
│   └── tests/           # Backend tests
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── features/    # Feature modules
│   │   └── lib/        # Utilities
│   └── tests/          # Frontend tests
└── docs/               # Documentation
```

</details>

## 🛠️ Tech Stack

<details>
<summary>Click to expand</summary>

### Frontend
- React 18 with TypeScript
- TailwindCSS & HeadlessUI
- React Query & Zustand
- Jest & Testing Library

### Backend
- FastAPI
- LangChain & LangGraph
- MongoDB & Pinecone
- OpenAI GPT-4

</details>

## 📦 Deployment

### Docker Deployment

The application can be deployed using Docker in both development and production environments.

#### Development Environment

```bash
# Start all services with hot-reload
docker-compose -f deploy/docker/docker-compose.dev.yml up --build

# Start specific services
docker-compose -f deploy/docker/docker-compose.dev.yml up backend mongodb
docker-compose -f deploy/docker/docker-compose.dev.yml up frontend

# View logs
docker-compose -f deploy/docker/docker-compose.dev.yml logs -f
```

#### Production Environment

```bash
# Build and start all services in detached mode
docker-compose -f deploy/docker/docker-compose.yml up --build -d

# Check service status
docker-compose -f deploy/docker/docker-compose.yml ps

# Monitor logs
docker-compose -f deploy/docker/docker-compose.yml logs -f
```

#### Container Architecture

- **Backend Container**: Python FastAPI application with uvicorn server
- **Frontend Container**: Nginx serving built React application
- **MongoDB Container**: Database service with persistent storage
- **Volumes**: 
  - `mongodb_data`: Persistent database storage
  - `uploads`: Document storage for processed files

#### Environment Configuration

1. Backend Environment (.env)
```bash
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB_NAME=DocChat
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_environment
JWT_SECRET_KEY=your_jwt_secret
```

2. Frontend Environment
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

#### Health Monitoring

The deployment includes health checks for all services:
- Backend: HTTP health endpoint at `/health`
- Frontend: Nginx status page
- MongoDB: Connection check

#### Scaling Considerations

- Backend can be scaled horizontally using Docker Swarm or Kubernetes
- MongoDB should be configured with replication for production
- Consider using managed services for databases in production

### Cloud Platform Deployment

#### AWS Deployment
- EC2 instances for application containers
- ECS/EKS for container orchestration
- MongoDB Atlas for database
- S3 for document storage
- CloudFront for CDN
- Route53 for DNS management

[Detailed AWS Setup Guide](docs/deployment/aws.md)

#### Google Cloud Platform
- Google Compute Engine for containers
- Google Kubernetes Engine for orchestration
- Cloud Storage for documents
- Cloud CDN for content delivery
- Cloud DNS for domain management

[Detailed GCP Setup Guide](docs/deployment/gcp.md)

#### Microsoft Azure
- Azure Container Instances
- AKS for Kubernetes deployment
- Azure Cosmos DB with MongoDB API
- Azure Blob Storage for documents
- Azure CDN for content delivery

[Detailed Azure Setup Guide](docs/deployment/azure.md)

### Security Considerations

- All containers run as non-root users
- Environment variables for sensitive data
- Regular security updates for base images
- Network isolation between services
- Rate limiting on API endpoints
- CORS configuration
- SSL/TLS encryption

### Backup Strategy

1. Database Backups
```bash
# Manual MongoDB backup
docker-compose exec mongodb mongodump --out /backup

# Restore from backup
docker-compose exec mongodb mongorestore /backup
```

2. Document Storage Backups
```bash
# Backup uploads volume
docker run --rm --volumes-from DocChat_backend_1 -v $(pwd):/backup \
  alpine tar czvf /backup/uploads.tar.gz /app/uploads
```

## 🔒 Security

- JWT-based authentication
- Rate limiting
- Input validation
- CORS protection
- Regular security audits

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🔧 Development

### Code Style

```bash
# Backend
pip install black isort flake8
black .
isort .
flake8

# Frontend
npm run lint
npm run format
```

### Testing

```bash
# Backend
pytest
pytest --cov=app tests/

# Frontend
npm run test
npm run test:coverage
```

## 🐳 Docker Support

### Development
```bash
# Development with hot-reload
docker-compose -f docker-compose.dev.yml up

# Production build
docker-compose -f docker-compose.prod.yml up
```

### Production
```bash
# Build images
docker build -t DocChat-backend -f backend/Dockerfile.prod backend/
docker build -t DocChat-frontend -f frontend/Dockerfile.prod frontend/

# Run containers
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Troubleshooting

<details>
<summary>Common Issues</summary>

### Backend Issues
1. **MongoDB Connection Errors**
   ```bash
   # Check MongoDB status
   mongosh
   # Verify connection string in .env
   ```

2. **Pinecone API Issues**
   - Verify API key and environment
   - Check index name and dimension

### Frontend Issues
1. **WebSocket Connection Failed**
   - Verify backend is running
   - Check CORS settings
   - Confirm WebSocket URL

2. **Build Failures**
   ```bash
   # Clear node modules and reinstall
   rm -rf node_modules
   npm install
   ```

</details>

## 📈 Performance

### Optimizations
- Document chunking strategy
- Vector store indexing
- Response streaming
- Frontend caching
- API rate limiting

### Monitoring
- Prometheus metrics
- Grafana dashboards
- Error tracking
- Usage analytics

## 🔄 Updates & Migration

### Version History
- v1.0.0 - Initial release
- v1.1.0 - Added streaming support
- v1.2.0 - Multiple document handling
- v2.0.0 - New UI and improved RAG

### Migration Guides
- [v1.x to v2.x Migration](docs/migration/v1-to-v2.md)
- [Database Schema Updates](docs/migration/database.md)

