"""
Local AI Integration for Sign3T
Handles local LLM operations using Ollama
"""

import ollama
import json
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import numpy as np

class LocalAI:
    """Manages local AI operations using Ollama"""
    
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check if the specified model is available"""
        try:
            models = ollama.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                print(f"Model {self.model_name} not found. Available models: {available_models}")
                # Try to use the first available model
                if available_models:
                    self.model_name = available_models[0]
                    print(f"Using {self.model_name} instead")
                else:
                    print("No models available. Please install a model with: ollama pull llama3.2")
                    self.model_name = None
        except Exception as e:
            print(f"Error checking models: {e}")
            self.model_name = None
    
    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using the local LLM"""
        if not self.model_name:
            return "Local AI model not available. Please install Ollama and a model."
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence transformers"""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def analyze_threat(self, location: str, context: str) -> Dict[str, Any]:
        """
        Analyzes the threat based on location and context using the local LLM.
        Returns a structured dictionary of threat indicators.
        """
        system_prompt = """You are an AI assistant for law enforcement threat assessment.
        Your goal is to identify potential threats, known individuals, and risks based on the provided context.
        Respond with a structured JSON object containing the following keys:
        - "threat_factors": List of identified threat factors (e.g., "Weapons involved", "History of violence", "Mental health crisis").
        - "weapons": List of specific weapons mentioned or implied.
        - "violence_history": List of specific violence indicators or past incidents.
        - "mental_health_indicators": Boolean indicating presence of mental health concerns.
        - "summary": A concise summary of the threat assessment.
        """

        prompt = f"""
        Location: {location}
        Context: {context}

        Analyze this situation and provide a threat assessment in the specified JSON format.
        """

        response = self.generate_text(prompt, system_prompt)

        try:
            # Try to parse JSON response
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback to structured response parsing if LLM doesn't return perfect JSON
            return self._parse_text_response(response)
    
    def _parse_text_response(self, response: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails"""
        return {
            "threat_factors": ["AI analysis unavailable"],
            "weapons": [],
            "violence_history": [],
            "mental_health_indicators": False,
            "summary": response[:200] + "..." if len(response) > 200 else response
        }
    
    def summarize_context(self, context_data: List[Dict[str, Any]]) -> str:
        """Summarize multiple context items"""
        if not context_data:
            return "No context data available."
        
        context_text = "\n".join([
            f"- {item.get('content', '')}" 
            for item in context_data[:5]  # Limit to first 5 items
        ])
        
        prompt = f"""
        Summarize the following law enforcement context data into a concise briefing:
        
        {context_text}
        
        Focus on:
        - Key threat indicators
        - Known individuals or suspects
        - Weapons or dangerous items
        - Location-specific risks
        - Recommended response approach
        """
        
        return self.generate_text(prompt)
    
    def is_available(self) -> bool:
        """Check if local AI is available"""
        return self.model_name is not None

# Global instance
local_ai = LocalAI()
