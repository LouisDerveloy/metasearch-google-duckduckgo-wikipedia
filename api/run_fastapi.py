import logging
import os
import sys
import time
import urllib.parse
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Charger les variables d'environnement
load_dotenv('.env.local')

from models.search import SearchRequest, SearchResponse, EngineResponse, SearchEngine
from engines import engine_manager


def setup_logging():
    """Configuration du logging pour FastAPI"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'fastapi.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # Aussi dans stdout pour le service
        ]
    )

    # Logger spécialisé
    logger = logging.getLogger('MetasearchAPI')
    return logger


# Setup initial
logger = setup_logging()

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "Origin",
        "X-Requested-With"
    ],
)


@app.get("/api")
async def root():
    return {
        "message": "Metasearch API",
        "version": "1.0.0",
        "available_engines": engine_manager.get_available_engines(),
        "engine_status": engine_manager.get_engine_status()
    }


@app.get("/api/engines")
async def get_engines():
    """Obtenir la liste et le statut de tous les moteurs"""
    return {
        "engines": engine_manager.get_available_engines(),
        "status": engine_manager.get_engine_status()
    }


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Effectuer une recherche sur les moteurs spécifiés"""

    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="La requête ne peut pas être vide")

    if not request.engines:
        request.engines = [SearchEngine.GOOGLE]

    start_time = time.time()

    query = urllib.parse.unquote(request.query.strip())

    try:
        # Convertir les enums en strings
        engine_names = [engine.value for engine in request.engines]

        # Rechercher sur tous les moteurs demandés
        engine_responses = await engine_manager.search_multiple(
            query,
            engine_names,
            request.max_results
        )

        # Convertir en EngineResponse objects
        responses = [EngineResponse(**response) for response in engine_responses]

        # Calculer le total des résultats
        total_results = sum(len(response.results) for response in responses if response.success)

        search_time = time.time() - start_time

        return SearchResponse(
            query=query,
            engines_responses=responses,
            total_results=total_results,
            search_time=search_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")


@app.get("/api/engines/{engine_name}/test")
async def test_engine(engine_name: str):
    """Tester un moteur spécifique avec une requête simple"""
    engine = engine_manager.get_engine(engine_name)
    if not engine:
        raise HTTPException(status_code=404, detail=f"Moteur '{engine_name}' non trouvé")

    test_query = "test search"
    result = await engine.execute_search(test_query, 5)

    return {
        "engine": engine_name,
        "test_query": test_query,
        "result": result
    }


@app.get("/api/engines/{engine_name}/config")
async def check_engine_config(engine_name: str):
    """Vérifier la configuration détaillée d'un moteur"""
    engine = engine_manager.get_engine(engine_name)
    if not engine:
        raise HTTPException(status_code=404, detail=f"Moteur '{engine_name}' non trouvé")

    if engine_name == "google":
        import os
        api_key = os.getenv("GOOGLE_API_KEY")
        cse_id = os.getenv("GOOGLE_CSE_ID")

        return {
            "engine": engine_name,
            "config_status": {
                "api_key_present": bool(api_key),
                "api_key_length": len(api_key) if api_key else 0,
                "api_key_preview": f"{api_key[:8]}..." if api_key and len(api_key) > 8 else "Non définie",
                "cse_id_present": bool(cse_id),
                "cse_id_length": len(cse_id) if cse_id else 0,
                "cse_id_preview": f"{cse_id[:8]}..." if cse_id and len(cse_id) > 8 else "Non définie",
                "env_file_loaded": os.path.exists(".env.local"),
            },
            "is_configured": engine.is_configured(),
            "service_initialized": hasattr(engine, 'service') and engine.service is not None
        }

    elif engine_name == "duckduckgo":
        return {
            "engine": engine_name,
            "config_status": {
                "api_available": True,
                "no_auth_required": True,
                "service_url": "https://api.duckduckgo.com/"
            },
            "is_configured": engine.is_configured(),
            "ready": True
        }

    elif engine_name == "wikipedia":
        return {
            "engine": engine_name,
            "config_status": {
                "api_available": True,
                "no_auth_required": True,
                "service_url": "https://fr.wikipedia.org/w/api.php",
                "language": "français"
            },
            "is_configured": engine.is_configured(),
            "ready": True
        }

    return {
        "engine": engine_name,
        "is_configured": engine.is_configured()
    }


def main():
    """Point d'entrée principal pour FastAPI"""
    try:
        # Configuration du serveur
        host = "127.0.0.1"
        port = int(os.getenv("PORT", 8000))

        # Déterminer si on tourne comme service ou en mode dev
        running_as_service = os.getenv("RUNNING_AS_SERVICE", "0") == "1"

        if running_as_service:
            logger.info(f"🚀 Démarrage FastAPI en mode SERVICE sur {host}:{port}")
            uvicorn_log_level = "warning"  # Moins verbeux pour le service
        else:
            logger.info(f"🚀 Démarrage FastAPI en mode DEV sur {host}:{port}")
            uvicorn_log_level = "info"

        # Démarrer uvicorn
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,  # Pas de reload en service
            access_log=True,
            log_level=uvicorn_log_level,
            loop="asyncio"
        )

    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage de FastAPI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
