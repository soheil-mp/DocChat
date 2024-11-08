from typing import Optional, List
from app.models.chat import ChatSession, Message, MessageRole, ChatRequest
from app.db.mongodb import db
from app.core.config import settings
import logging
from datetime import datetime
import uuid
from openai import OpenAI

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.db = None
        self.vector_store = None
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        prompt_template: str = "chat_with_docs"
    ) -> ChatSession:
        """Process a chat message and return the updated session"""
        try:
            # Create or get session
            if session_id:
                session = await self.get_session(session_id, user_id)
                if not session:
                    raise ValueError("Session not found")
            else:
                session = await self.create_session(user_id)

            # Create user message
            user_message = Message(
                role=MessageRole.USER,
                content=message,
                created_at=datetime.utcnow()
            )

            try:
                # Convert session messages to OpenAI format
                messages = [
                    {
                        "role": "system", 
                        "content": """You are a helpful AI assistant. You must maintain context of the conversation 
                        and remember details that users share with you. When users share personal information like 
                        their name, you should remember and use it in future responses. Be conversational and friendly 
                        while maintaining professionalism."""
                    }
                ]
                
                # Add conversation history
                for msg in session.messages:
                    messages.append({
                        "role": msg.role.value,
                        "content": msg.content
                    })
                
                # Add the new user message
                messages.append({
                    "role": "user",
                    "content": message
                })

                # Get response from OpenAI with full conversation history
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )

                ai_content = response.choices[0].message.content

                # Create AI message
                ai_message = Message(
                    role=MessageRole.ASSISTANT,
                    content=ai_content,
                    created_at=datetime.utcnow()
                )

            except Exception as e:
                logger.error(f"Error generating AI response: {str(e)}")
                ai_message = Message(
                    role=MessageRole.ASSISTANT,
                    content="I apologize, but I encountered an error generating a response.",
                    created_at=datetime.utcnow()
                )

            # Update session with new messages
            session.messages.extend([user_message, ai_message])
            session.updated_at = datetime.utcnow()

            # Save to database
            await self.save_session(session)

            return session

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    async def create_session(self, user_id: str, title: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title or "New Chat",
            messages=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to database
        await db.db.sessions.insert_one(session.dict())
        return session

    async def get_session(self, session_id: str, user_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        session_data = await db.db.sessions.find_one({
            "id": session_id,
            "user_id": user_id
        })
        return ChatSession(**session_data) if session_data else None

    async def save_session(self, session: ChatSession):
        """Save or update a chat session"""
        await db.db.sessions.update_one(
            {"id": session.id},
            {"$set": session.dict()},
            upsert=True
        )

    async def list_sessions(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChatSession]:
        """List chat sessions for a user"""
        cursor = db.db.sessions.find(
            {"user_id": user_id}
        ).sort("updated_at", -1).skip(skip).limit(limit)
        
        sessions = []
        async for session_data in cursor:
            sessions.append(ChatSession(**session_data))
        return sessions

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete a chat session"""
        result = await db.db.sessions.delete_one({
            "id": session_id,
            "user_id": user_id
        })
        return result.deleted_count > 0

# Create a global instance
chat_service = ChatService()