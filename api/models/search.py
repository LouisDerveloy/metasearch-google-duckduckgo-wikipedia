from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class SearchEngine(str, Enum):
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"
    WIKIPEDIA = "wikipedia"

class SearchResult(BaseModel):
    title: str
    url: str
    description: str
    ads: Optional[bool] = False
    searchEngine: str

class SearchRequest(BaseModel):
    query: str
    max_results: int = 10
    engines: Optional[List[SearchEngine]] = [SearchEngine.GOOGLE]

class EngineResponse(BaseModel):
    """Réponse d'un moteur spécifique"""
    engine: str
    results: List[SearchResult]
    success: bool
    error_message: Optional[str] = None
    search_time: Optional[float] = None

class SearchResponse(BaseModel):
    """Réponse combinée de tous les moteurs"""
    query: str
    engines_responses: List[EngineResponse]
    total_results: int
    search_time: float

class EngineConfig(BaseModel):
    """Configuration d'un moteur"""
    name: str
    enabled: bool
    max_results: int = 10
    timeout: int = 10
    config: Dict[str, Any] = {}
