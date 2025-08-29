from typing import Dict, List
from engines.base import SearchEngineBase
from engines.google import GoogleSearchEngine
from engines.duckduckgo import DuckDuckGoSearchEngine
from engines.wikipedia import WikipediaSearchEngine

class SearchEngineManager:
    """Gestionnaire central de tous les moteurs de recherche"""

    def __init__(self):
        self.engines: Dict[str, SearchEngineBase] = {
            "google": GoogleSearchEngine(),
            "duckduckgo": DuckDuckGoSearchEngine(),
            "wikipedia": WikipediaSearchEngine(),
        }

    def get_engine(self, name: str) -> SearchEngineBase:
        """Récupère un moteur par nom"""
        return self.engines.get(name.lower())

    def get_enabled_engines(self) -> List[SearchEngineBase]:
        """Récupère tous les moteurs activés et configurés"""
        return [engine for engine in self.engines.values()
                if engine.enabled and engine.is_configured()]

    def get_available_engines(self) -> List[str]:
        """Liste des noms de moteurs disponibles"""
        return list(self.engines.keys())

    def get_engine_status(self) -> Dict[str, dict]:
        """Statut de tous les moteurs"""
        status = {}
        for name, engine in self.engines.items():
            status[name] = {
                "name": engine.name,
                "enabled": engine.enabled,
                "configured": engine.is_configured(),
                "status": "ready" if (engine.enabled and engine.is_configured()) else "disabled"
            }
        return status

    async def search_multiple(self, query: str, engine_names: List[str], max_results: int = 10) -> List[dict]:
        """Recherche sur plusieurs moteurs simultanément"""
        import asyncio

        tasks = []
        for engine_name in engine_names:
            engine = self.get_engine(engine_name)
            if engine:
                tasks.append(engine.execute_search(query, max_results))

        if not tasks:
            return []

        # Exécuter toutes les recherches en parallèle
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtrer les exceptions
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                continue
            valid_results.append(result)

        return valid_results

# Instance globale
engine_manager = SearchEngineManager()
