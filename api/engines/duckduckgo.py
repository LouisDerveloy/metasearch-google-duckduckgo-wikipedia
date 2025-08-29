from ddgs import DDGS
from typing import List, Optional, Tuple
from engines.base import SearchEngineBase
from models.search import SearchResult
import asyncio

class DuckDuckGoSearchEngine(SearchEngineBase):
    def __init__(self):
        super().__init__("duckduckgo", enabled=True)

    def is_configured(self) -> bool:
        """DuckDuckGo ne nécessite pas de configuration"""
        return True

    async def search(self, query: str, max_results: Optional[int] = None) -> Tuple[List[SearchResult], Optional[str]]:
        """Recherche DuckDuckGo via duckduckgo-search"""
        print(f"DEBUG DDG search() - Query: '{query}'")

        try:
            num_results = min(max_results or self.max_results, 20)

            # La librairie est synchrone, on l'exécute dans un thread
            def _sync_search():
                with DDGS() as ddgs:
                    # ✅ Correction: utiliser 'query' au lieu de 'keywords'
                    results = list(ddgs.text(
                        query=query,  # ✅ Paramètre correct
                        region='fr-fr',
                        safesearch='moderate',
                        timelimit=None,
                        max_results=num_results
                    ))
                    return results

            # Exécuter de manière asynchrone
            loop = asyncio.get_event_loop()
            ddg_results = await loop.run_in_executor(None, _sync_search)

            search_results = []
            for result in ddg_results:
                search_results.append(SearchResult(
                    title=result.get('title', ''),
                    url=result.get('href', ''),
                    description=result.get('body', ''),
                    ads=False,
                    searchEngine=self.name
                ))

            print(f"DEBUG DDG: {len(search_results)} résultats traités")
            return search_results, None

        except Exception as e:
            print(f"❌ Erreur DuckDuckGo: {e}")
            return [], f"Erreur DuckDuckGo: {str(e)}"
