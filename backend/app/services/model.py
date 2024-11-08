from typing import List, Dict, Tuple, Optional
import tiktoken
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import os
import logging

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.tokenizer = None
    
    def initialize(self):
        """Initialize the model service"""
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    async def _get_token_count(self, messages: List[Dict]) -> int:
        """Count tokens in messages"""
        if self.tokenizer is None:
            self.initialize()
        
        total_tokens = 0
        for message in messages:
            total_tokens += len(self.tokenizer.encode(message["content"]))
        return total_tokens
    
    async def generate_response(self, messages: List[Dict], model_name: str, user_id: str, request_type: str) -> Tuple[str, Dict]:
        """Generate a response using the specified model"""
        try:
            # Initialize ChatOpenAI with the specified model
            chat = ChatOpenAI(
                model_name=model_name,
                temperature=0.7,
                streaming=False
            )
            
            # Create a chain
            chain = (
                ChatPromptTemplate.from_messages(messages)
                | chat
                | StrOutputParser()
            )
            
            # Generate response
            response = await chain.ainvoke({"messages": messages})
            
            # Count tokens
            input_tokens = await self._get_token_count(messages)
            output_tokens = len(self.tokenizer.encode(response))
            
            return response, {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            }
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request.", {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }

def generate_response(query: str) -> str:
    # Ensure OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

    # Initialize the chat model
    chat_model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Provide clear and concise responses."),
        ("human", "{query}")
    ])
    
    # Create the chain
    chain = prompt | chat_model | StrOutputParser()
    
    # Generate response
    response = chain.invoke({"query": query})
    
    return response

# Global instance
model_service = ModelService()
model_service.initialize()