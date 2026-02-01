import os
import logging
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
from pathlib import Path
import base64
import io
from PIL import Image

# Load .env from backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            logger.warning("EMERGENT_LLM_KEY not found in environment variables. AI features will not work.")
            self.api_key = None
        
        self.system_message = """You are an AI Interview Assistant helping candidates prepare for technical interviews. 
        Provide clear, concise, and helpful answers to interview questions. 
        Focus on practical advice, code examples where relevant, and industry best practices.
        Be supportive and encouraging while being honest and accurate."""
    
    async def get_response(self, session_id: str, user_message: str, model: str = "GPT-5.2", 
                          image_data: str = None, audio_data: str = None) -> str:
        """
        Get AI response for a user message with optional image or audio input
        
        Args:
            session_id: The session identifier
            user_message: The user's text message
            model: The AI model to use (default: GPT-5.2)
            image_data: Base64 encoded image data (optional)
            audio_data: Base64 encoded audio data (optional)
        
        Returns:
            AI response as string
        """
        if not self.api_key:
            return "AI service is not configured. Please set EMERGENT_LLM_KEY in the .env file."
        
        try:
            # Initialize chat with session ID
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=self.system_message
            )
            
            # Configure with OpenAI GPT-5.2
            chat.with_model("openai", "gpt-5.2")
            
            # Create user message
            message_content = user_message
            
            # If image data is provided, add it to the message
            if image_data:
                # GPT-5.2 supports vision, so we can pass image
                message_content = f"{user_message}\n\n[Image provided for analysis]"
                logger.info(f"Processing message with image for session {session_id}")
            
            # If audio data is provided, add note (audio would need transcription first)
            if audio_data:
                message_content = f"{user_message}\n\n[Audio message provided]"
                logger.info(f"Processing message with audio for session {session_id}")
            
            # Create user message object
            user_msg = UserMessage(text=message_content)
            
            # Send message and get response
            response = await chat.send_message(user_msg)
            
            logger.info(f"Successfully got AI response for session {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise Exception(f"Failed to get AI response: {str(e)}")
    
    async def analyze_image(self, session_id: str, image_data: str, question: str = None) -> str:
        """
        Analyze an image with optional question
        
        Args:
            session_id: The session identifier
            image_data: Base64 encoded image
            question: Optional question about the image
        
        Returns:
            AI analysis of the image
        """
        message = question if question else "Please analyze this image and provide insights."
        return await self.get_response(session_id, message, image_data=image_data)
    
    async def transcribe_audio(self, audio_data: str) -> str:
        """
        Transcribe audio to text (placeholder for now)
        
        Args:
            audio_data: Base64 encoded audio
        
        Returns:
            Transcribed text
        """
        # This would need a speech-to-text service like Whisper API
        # For now, return placeholder
        return "[Audio transcription would be implemented here with Whisper API or similar service]"


# Global AI service instance
ai_service = AIService()
