from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import time
from models.search import SearchResult

class SearchEngineBase(ABC):
    """Classe de base abstraite pour tous les moteurs de recherche"""

    def __init__(self, name: str, enabled: bool = True, max_results: int = 20):
        self.name = name
        self.enabled = enabled
        self.max_results = max_results

    @abstractmethod
    async def search(self, query: str, max_results: Optional[int] = None) -> Tuple[List[SearchResult], Optional[str]]:
        """
        Effectue une recherche

        Args:
            query: Terme de recherche
            max_results: Nombre max de résultats (optionnel)

        Returns:
            Tuple[List[SearchResult], Optional[str]]: (résultats, message_erreur)
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Vérifie si le moteur est correctement configuré"""
        pass

    async def execute_search(self, query: str, max_results: Optional[int] = None) -> dict:
        """
        Exécute une recherche avec mesure du temps et gestion d'erreurs

        Returns:
            dict: Format EngineResponse
        """
        if not self.enabled:
            return {
                "engine": self.name,
                "results": [],
                "success": False,
                "error_message": f"Moteur {self.name} désactivé",
                "search_time": 0
            }

        if not self.is_configured():
            return {
                "engine": self.name,
                "results": [],
                "success": False,
                "error_message": f"Moteur {self.name} mal configuré",
                "search_time": 0
            }

        start_time = time.time()

        try:
            results, error_message = await self.search(query, max_results or self.max_results)
            search_time = time.time() - start_time

            return {
                "engine": self.name,
                "results": results,
                "success": error_message is None,
                "error_message": error_message,
                "search_time": search_time
            }

        except Exception as e:
            search_time = time.time() - start_time
            return {
                "engine": self.name,
                "results": [],
                "success": False,
                "error_message": f"Erreur inattendue: {str(e)}",
                "search_time": search_time
            }
