from typing import Dict, List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from ..core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Verify environment variables
        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        if not settings.PINECONE_ENV:
            raise ValueError("PINECONE_ENV not found in environment variables")
        if not settings.PINECONE_INDEX_NAME:
            raise ValueError("PINECONE_INDEX_NAME not found in environment variables")
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        logger.info("Initializing RAG service with:")
        logger.info(f"Pinecone Environment: {settings.PINECONE_ENV}")
        logger.info(f"Pinecone Index: {settings.PINECONE_INDEX_NAME}")
        
        # Initialize Pinecone with new API
        os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
        os.environ["PINECONE_ENVIRONMENT"] = settings.PINECONE_ENV
        
        self.pc = PineconeClient(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Get or create Pinecone index
        self.index_name = settings.PINECONE_INDEX_NAME
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embeddings dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-west-2"
                )
            )
        
        # Initialize vectorstore
        self.vectorstore = Pinecone.from_existing_index(
            index_name=self.index_name,
            embedding=self.embeddings,
            namespace=""  # Optional: specify a namespace if needed
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize RAG chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
            ),
            return_source_documents=True
        )

    async def get_response(self, query: str, chat_history: List = []) -> Dict:
        """Get response using RAG"""
        try:
            # Get response from chain
            result = await self.qa_chain.acall({
                "question": query,
                "chat_history": chat_history
            })
            
            # Extract sources from documents
            sources = []
            if result.get("source_documents"):
                for doc in result["source_documents"]:
                    sources.append({
                        "title": doc.metadata.get("title", "Unknown"),
                        "content": doc.page_content,
                        "document_id": doc.metadata.get("document_id")
                    })
            
            return {
                "answer": result["answer"],
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error getting RAG response: {str(e)}")
            raise

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
            
            # Refresh the retriever
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True
            )
            
            print(f"Successfully processed document: {metadata.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise e

    async def delete_document_vectors(self, document_id: str) -> None:
        """Delete all vectors associated with a document"""
        try:
            # Get the Pinecone index
            index = self.pc.Index(self.index_name)
            
            # For Serverless/Starter indexes, we need to:
            # 1. Query to get vector IDs associated with the document
            # 2. Delete vectors by their IDs
            
            # Query vectors with matching document_id
            query_response = index.query(
                vector=[0] * 1536,  # Dummy vector for metadata-only query
                filter={
                    "document_id": document_id
                },
                top_k=10000,  # Adjust based on your needs
                include_metadata=True
            )
            
            if query_response.matches:
                # Extract vector IDs
                vector_ids = [match.id for match in query_response.matches]
                
                # Delete vectors by IDs
                if vector_ids:
                    index.delete(ids=vector_ids)
                    
                logger.info(f"Successfully deleted {len(vector_ids)} vectors for document: {document_id}")
                
                # Re-initialize the vectorstore to reflect the changes
                self.vectorstore = Pinecone.from_existing_index(
                    index_name=self.index_name,
                    embedding=self.embeddings,
                    namespace=""
                )
                
                # Refresh the retriever with the updated vectorstore
                self.qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=self.vectorstore.as_retriever(
                        search_kwargs={"k": 3}
                    ),
                    return_source_documents=True
                )
            else:
                logger.info(f"No vectors found for document: {document_id}")
                
        except Exception as e:
            logger.error(f"Error deleting vectors: {str(e)}")
            raise

rag_service = RAGService()