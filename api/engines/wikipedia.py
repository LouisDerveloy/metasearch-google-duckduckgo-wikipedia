import httpx
from typing import List, Optional, Tuple
from engines.base import SearchEngineBase
from models.search import SearchResult
import urllib.parse

class WikipediaSearchEngine(SearchEngineBase):
    def __init__(self):
        super().__init__("wikipedia", enabled=True)
        self.base_url = "https://fr.wikipedia.org/api/rest_v1/"
        self.api_url = "https://fr.wikipedia.org/w/api.php"
        self.timeout = 10

    def is_configured(self) -> bool:
        """Wikipedia ne nécessite pas de configuration"""
        return True

    async def search(self, query: str, max_results: Optional[int] = None) -> Tuple[List[SearchResult], Optional[str]]:
        """Recherche Wikipedia via API MediaWiki"""
        print(f"DEBUG Wikipedia search() - Query: '{query}'")

        try:
            num_results = min(max_results or self.max_results, 20)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 1. Recherche des pages correspondantes
                search_response = await client.get(
                    self.api_url,
                    params={
                        "action": "query",
                        "format": "json",
                        "list": "search",
                        "srsearch": query,
                        "srlimit": num_results,
                        "srinfo": "totalhits",
                        "srprop": "size|wordcount|timestamp|snippet"
                    }
                )

                search_data = search_response.json()

                if "error" in search_data:
                    return [], f"Erreur API Wikipedia: {search_data['error']['info']}"

                search_results = []
                pages = search_data.get("query", {}).get("search", [])

                print(f"DEBUG Wikipedia: {len(pages)} pages trouvées")

                # 2. Pour chaque page, récupérer les détails
                for page in pages[:num_results]:
                    page_title = page["title"]
                    page_url = f"https://fr.wikipedia.org/wiki/{urllib.parse.quote(page_title.replace(' ', '_'))}"

                    # Nettoyer le snippet (retire le HTML)
                    snippet = page.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")

                    search_results.append(SearchResult(
                        title=page_title,
                        url=page_url,
                        description=snippet or f"Article Wikipedia sur {page_title}",
                        ads=False,
                        searchEngine=self.name
                    ))

                print(f"DEBUG Wikipedia: {len(search_results)} résultats traités")
                return search_results, None

        except httpx.TimeoutException:
            return [], "Timeout lors de la recherche Wikipedia"
        except httpx.RequestError as e:
            return [], f"Erreur réseau Wikipedia: {str(e)}"
        except Exception as e:
            print(f"❌ Erreur générale Wikipedia: {e}")
            return [], f"Erreur inattendue Wikipedia: {str(e)}"
