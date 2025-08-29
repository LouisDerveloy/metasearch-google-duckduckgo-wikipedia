from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional, Tuple
import os
from engines.base import SearchEngineBase
from models.search import SearchResult

class GoogleSearchEngine(SearchEngineBase):
    def __init__(self):
        super().__init__("google", enabled=True)
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cse_id = os.getenv("GOOGLE_CSE_ID")
        self.max_results = os.getenv("MAX_RESULTS_PER_QUERY")
        self.service = None

        # Debug pour voir les valeurs
        print(f"API KEY: {self.api_key}")
        print(f"CSE ID: {self.cse_id}")
        print(f"DEBUG Google Init - API Key: {'✅' if self.api_key else '❌'} ({len(self.api_key or '')} chars)")
        print(f"DEBUG Google Init - CSE ID: {'✅' if self.cse_id else '❌'} ({len(self.cse_id or '')} chars)")
        print(f"DEBUG Google Init - is_configured(): {self.is_configured()}")

        if self.is_configured():
            try:
                print("DEBUG: Tentative d'initialisation du service Google...")
                self.service = build("customsearch", "v1", developerKey=self.api_key)
                print("DEBUG: Service Google initialisé avec succès ✅")
            except Exception as e:
                print(f"❌ Erreur initialisation Google API: {e}")
                self.service = None
        else:
            print("DEBUG: Configuration Google incomplète - service non initialisé")

    def is_configured(self) -> bool:
        """Vérifie la configuration Google"""
        # Vérification plus stricte
        api_key_valid = self.api_key is not None and len(self.api_key.strip()) > 0
        cse_id_valid = self.cse_id is not None and len(self.cse_id.strip()) > 0

        print(f"DEBUG is_configured - API Key valid: {api_key_valid}")
        print(f"DEBUG is_configured - CSE ID valid: {cse_id_valid}")

        return api_key_valid and cse_id_valid

    async def search(self, query: str, max_results: Optional[int] = None) -> Tuple[List[SearchResult], Optional[str]]:
        """Recherche Google Custom Search"""
        print(f"DEBUG search() - Service disponible: {'✅' if self.service else '❌'}")
        print(f"DEBUG search() - Query: '{query}'")

        if not self.service:
            return [], f"Service Google non initialisé (API Key: {'✅' if self.api_key else '❌'}, CSE ID: {'✅' if self.cse_id else '❌'})"

        try:
            num_results = min(max_results or self.max_results, 10)
            print(f"DEBUG: Recherche Google avec {num_results} résultats max")

            # Test direct avant la requête
            print(f"DEBUG: CSE ID utilisé: '{self.cse_id}'")
            print(f"DEBUG: API Key utilisée: '{self.api_key[:10]}...'")

            result = self.service.cse().list(
                q=query,
                cx=self.cse_id,
                num=num_results
            ).execute()

            print(f"DEBUG: Réponse Google reçue: {len(result.get('items', []))} résultats")

            search_results = []
            if 'items' in result:
                for item in result['items']:
                    search_result = SearchResult(
                        title=item.get('title', ''),
                        url=item.get('link', ''),
                        description=item.get('snippet', ''),
                        ads=False,
                        searchEngine=self.name
                    )
                    search_results.append(search_result)

            return search_results, None

        except HttpError as e:
            print(f"❌ HttpError Google: {e}")
            print(f"❌ Status: {e.resp.status}")
            print(f"❌ Reason: {e.resp.reason}")

            # Passer l'erreur Google directement
            if e.resp.status == 429:
                return [], "Quota Google épuisé (100 requêtes/jour). Réessaye demain ou active la facturation."
            elif e.resp.status == 403:
                return [], "Clé API Google invalide ou API Custom Search non activée"
            elif e.resp.status == 400:
                error_details = getattr(e, 'error_details', None)
                if error_details:
                    return [], f"Requête invalide: {error_details[0].get('message', 'Erreur inconnue')}"
                else:
                    return [], f"Requête invalide (400): {str(e)}"
            else:
                error_details = getattr(e, 'error_details', None)
                if error_details:
                    error_msg = error_details[0].get('message', str(e))
                else:
                    error_msg = str(e)
                return [], f"Erreur Google API ({e.resp.status}): {error_msg}"

        except Exception as e:
            print(f"❌ Erreur générale Google: {e}")
            return [], f"Erreur inattendue Google: {str(e)}"
