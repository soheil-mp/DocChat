from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from typing import List, Dict
from pinecone import Pinecone as PineconeClient, ServerlessSpec
import os
from ..core.config import settings
import time

class RAGService:
    def __init__(self):
        # Initialize OpenAI
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize Pinecone
        self.pc = PineconeClient(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        self.index_name = settings.PINECONE_INDEX_NAME
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        try:
            # Check if index exists
            indexes = self.pc.list_indexes()
            if self.index_name not in indexes.names():
                print(f"Creating new index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embeddings dimension
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                print(f"Successfully created index: {self.index_name}")
            else:
                print(f"Using existing index: {self.index_name}")
            
            # Initialize vectorstore
            self.vectorstore = Pinecone(
                index=self.pc.Index(self.index_name),
                embedding=self.embeddings,
                text_key="text"
            )
            
        except Exception as e:
            print(f"Error initializing RAG service: {str(e)}")
            raise e

    async def process_document(self, content: str, metadata: Dict) -> None:
        """Process and store document in vector database"""
        try:
            # Split text into chunks
            texts = self.text_splitter.split_text(content)
            print(f"Split document into {len(texts)} chunks")
            
            # Create documents with metadata
            documents = [
                {"text": text, "metadata": {
                    "title": metadata.get("title", "Unknown"),
                    "file_path": metadata.get("file_path", ""),
                    "chunk_id": f"{metadata.get('id', '')}_chunk_{i}",
                    "document_id": metadata.get("id", ""),
                    "source": text[:200] + "..."  # First 200 chars as preview
                }}
                for i, text in enumerate(texts)
            ]
            
            # Add to Pinecone
            self.vectorstore.add_texts(
                texts=[doc["text"] for doc in documents],
                metadatas=[doc["metadata"] for doc in documents]
            )
            print(f"Successfully processed document: {metadata.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise e
    
    async def get_response(self, query: str, chat_history: List = None) -> Dict:
        """Get response using RAG"""
        if chat_history is None:
            chat_history = []
            
        try:
            # Create retrieval chain with specific search parameters
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}  # Get top 3 most relevant chunks
                ),
                return_source_documents=True,
                verbose=True  # Add this for debugging
            )
            
            # Get response
            result = qa_chain({"question": query, "chat_history": chat_history})
            
            # Extract and format sources
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    if hasattr(doc, 'metadata'):
                        sources.append({
                            "title": doc.metadata.get("title", "Unknown"),
                            "content": doc.metadata.get("source", ""),
                            "document_id": doc.metadata.get("document_id", "")
                        })
            
            return {
                "answer": result["answer"],
                "sources": sources
            }
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            raise e

rag_service = RAGService()