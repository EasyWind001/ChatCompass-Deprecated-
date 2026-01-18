"""
AI处理模块
"""
from .ollama_client import OllamaClient, AIAnalysisResult
from .openai_client import OpenAIClient, DeepSeekClient

__all__ = [
    'OllamaClient',
    'AIAnalysisResult',
    'OpenAIClient',
    'DeepSeekClient'
]
