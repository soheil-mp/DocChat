# DocuChat - Knowledge Base Chat with RAG

## Overview
DocuChat is a single-page application that lets users upload documents to a knowledge base and interact with the uploaded content via a conversational AI. The project leverages Retrieval-Augmented Generation (RAG) to ensure responses are relevant to the documents.

## Project Structure

```bash
docuchat/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── config.py        # Configuration and environment settings
│   │   ├── models/          # Database models
│   │   │   └── __init__.py
│   │   ├── routes/          # API endpoints
│   │   │   └── __init__.py
│   │   └── services/        # Business logic
│   │       └── __init__.py
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Chat/
│   │   │   ├── Upload/
│   │   │   └── Config/
│   │   ├── services/        # API services
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── .env.example        # Frontend environment variables
└── README.md
```

## Features
- **Document Upload**: Support for multiple file types (PDF, DOCX, TXT)
- **Chat Interface**: Conversational AI interface with RAG capabilities
- **Customizable Settings**: Fine-tune model parameters for optimal responses

## Tech Stack
- **Frontend**: React, TailwindCSS, React Router, React Query
- **Backend**: FastAPI, LangChain, LangGraph
- **Database**: MongoDB
- **Vector Database**: Pinecone
- **AI/ML**: OpenAI GPT models

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

# Setup environment variables
cp .env.example .env
# Edit .env with your settings
```

### Running the Application

#### 1. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload
```
The API will be available at http://localhost:8000

#### 2. Start the Frontend
```bash
cd frontend
npm start
```
The application will be available at http://localhost:3000

## Usage

### 1. Document Upload
- Navigate to the "Upload" section
- Drag and drop files or use the file picker
- Supported formats: PDF, DOCX, TXT
- Wait for processing confirmation

### 2. Chat Interface
- Go to the "Chat" section
- Type your questions in the chat input
- Receive AI responses based on your uploaded documents
- View source documents used for responses

### 3. Configuration
Access the Settings panel to customize:
- **Model Selection**: [OpenAI, Cohere, Hugging Face]
- **Temperature**: [0.1 - 1.0]
- **Max Tokens**: [0 - 2048]
- **Top-p**: [0.0 - 1.0]
- **Frequency Penalty**: [0.0 - 2.0]
- **Presence Penalty**: [0.0 - 2.0]

## Environment Variables

### Backend (.env)
```
DATABASE_URL=mongodb://localhost:27017
VECTOR_DB_API_KEY=your_pinecone_api_key
VECTOR_DB_ENVIRONMENT=your_pinecone_environment
OPENAI_API_KEY=your_openai_api_key
PORT=8000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## Future Enhancements
- Advanced document filtering capabilities
- Response summarization
- Admin dashboard for document management
- Multi-language support
- Batch document processing
- Custom training capabilities

## Additional Features

### Monitoring & Observability
- Prometheus metrics
- Sentry error tracking
- Structured logging

### Security
- API key authentication
- Rate limiting
- Request validation

### Performance
- Redis caching
- Response time monitoring
- Health checks

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details

