from typing import List, Dict, Any
import openai
from fastapi import HTTPException
from ..config import Settings

settings = Settings()

class ChatService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        
    async def generate_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        try:
            messages = []
            # Add chat history if available
            if chat_history:
                for msg in chat_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add system message for context
            messages.append({
                "role": "system",
                "content": "You are a helpful assistant. Provide clear and concise responses."
            })
            
            # Add the current message
            messages.append({
                "role": "user",
                "content": message
            })

            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            if not response.choices:
                raise HTTPException(status_code=500, detail="No response generated")

            return response.choices[0].message['content'].strip()

        except openai.error.InvalidRequestError as e:
            print(f"OpenAI Invalid Request: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid request to AI service")
        except openai.error.AuthenticationError:
            print("OpenAI Authentication Error")
            raise HTTPException(status_code=401, detail="AI service authentication failed")
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate response")