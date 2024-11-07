from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
import pinecone
import tempfile
import os
from ..config import settings

class DocumentService:
    def __init__(self):
        # Initialize embeddings with explicit API key
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize Pinecone
        pinecone.init(
            api_key=settings.VECTOR_DB_API_KEY,
            environment=settings.VECTOR_DB_ENVIRONMENT
        )
        self.index_name = "docuchat"

    async def process_document(self, file: UploadFile) -> str:
        """Process uploaded document and store in vector database"""
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Load document based on file type
            if file.filename.endswith('.pdf'):
                loader = PyPDFLoader(temp_path)
            elif file.filename.endswith('.docx'):
                loader = Docx2txtLoader(temp_path)
            elif file.filename.endswith('.txt'):
                loader = TextLoader(temp_path)
            else:
                raise ValueError("Unsupported file type")

            # Process document
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)
            
            # Store in Pinecone
            vectorstore = Pinecone.from_documents(
                texts, 
                self.embeddings,
                index_name=self.index_name
            )

            return vectorstore.index_name

        finally:
            os.unlink(temp_path)