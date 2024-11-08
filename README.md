# DocuChat - Knowledge Base Chat with RAG

## Overview
DocuChat is a single-page application that lets users upload documents to a knowledge base and interact with the uploaded content via a conversational AI. The project leverages Retrieval-Augmented Generation (RAG) to provide accurate, document-grounded responses.

## Project Structure

```
docuchat/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/          # API endpoints (auth, chat, docs)
│   │   ├── core/            # Core utilities and config
│   │   ├── db/              # Database and repositories
│   │   ├── models/          # Domain models and schemas
│   │   └── services/        # Business logic services
│   └── tests/               # Backend tests
│
├── frontend/
│   ├── src/
│   │   ├── assets/          # Static assets
│   │   ├── components/      # Reusable UI components
│   │   ├── features/        # Feature modules
│   │   │   ├── auth/
│   │   │   ├── chat/
│   │   │   └── documents/
│   │   ├── lib/            # Third-party integrations
│   │   ├── store/          # State management
│   │   └── types/          # TypeScript types
│   └── tests/              # Frontend tests
│
├── deploy/                  # Deployment configurations
│   ├── docker/
│   └── k8s/
│
└── docs/                   # Documentation
    ├── api/
    ├── architecture/
    └── guides/
```

## Key Features
- 📄 **Document Management**
  - Support for multiple file formats (PDF, DOCX, TXT)
  - Batch upload capabilities
  - Document versioning and metadata tracking
  
- 💬 **Intelligent Chat Interface**
  - Context-aware conversations using RAG
  - Source attribution for responses
  - Chat history management
  - Real-time typing indicators
  
- ⚙️ **Advanced Configuration**
  - Model selection (OpenAI, Anthropic, Cohere)
  - Fine-tuning of generation parameters
  - Custom prompt templates
  - Response formatting options

## Tech Stack
### Frontend
- **Core**: TypeScript, React 18
- **Styling**: TailwindCSS, HeadlessUI
- **State Management**: React Query, Zustand
- **Testing**: Jest, React Testing Library

### Backend
- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph
- **Database**: MongoDB (documents), Pinecone (vectors)
- **LLM Integration**: OpenAI GPT-4

## Getting Started

### Prerequisites
- Node.js and npm
- Python 3.8+
- MongoDB
- Pinecone account
- OpenAI API key

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/docuchat.git
cd docuchat
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials
```

#### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Add TypeScript and necessary types
npm install --save-dev typescript @types/react @types/react-dom

#
# npm install react-router-dom axios zustand
# npm install --save-dev @types/react-router-dom

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Initialize TypeScript configuration
npx tsc --init
```

### Running the Application

#### 1. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload
```
The API will be available at [http://localhost:8000](http://localhost:8000)

#### 2. Start the Frontend
```bash
cd frontend
npm start
```
The application will be available at [http://localhost:3000](http://localhost:3000)

## Unit Testing 

```bash
pytest -v
```

## Process pdf documents

Process PDF documents inside backend/documents for the RAG process.
```
python backend/scripts/process_existing_documents.py
```


## Development

### Architecture
```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   Client   │────▶│   FastAPI  │────▶│  MongoDB   │
└────────────┘     └────────────┘     └────────────┘
                         │
                         ▼
                  ┌────────────┐     ┌────────────┐
                  │ LangChain  │────▶│  Pinecone  │
                  └────────────┘     └────────────┘
                         │
                         ▼
                  ┌────────────┐
                  │   OpenAI   │
                  └────────────┘
```

### API Documentation
Full API documentation is available at `/docs` when running the backend server.

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Docker Support
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Cloud Deployment
Deployment guides available for:
- AWS (ECS, EKS)
- Google Cloud (GKE)
- Azure (AKS)
- Digital Ocean

## Monitoring
- Application metrics via Prometheus/Grafana
- Error tracking with Sentry
- Custom analytics dashboard

## Security Considerations
- JWT authentication
- Rate limiting
- Input sanitization
- CORS configuration
- Regular dependency audits

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details

