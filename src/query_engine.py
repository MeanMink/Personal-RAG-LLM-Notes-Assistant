from llama_index.core import load_index_from_storage, StorageContext
from src.config import STORAGE_DIR, SIMILARITY_TOP_K, RESPONSE_MODE
from src.utils import get_logger
from src.indexer import configure_models

logger = get_logger('query_engine')

def get_query_engine():
    logger.info("Loading index from %s", STORAGE_DIR)
    logger.info("Storage directory contents: %s", list(STORAGE_DIR.iterdir() if STORAGE_DIR.exists() else ["Directory not found"]))
    
    # Get the LLM
    embed_model, llm_model = configure_models()
    
    storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
    logger.info("Storage context loaded")
    
    index = load_index_from_storage(
        storage_context=storage_context, 
        embed_model=embed_model,
    )
    logger.info("Index loaded, document count: %s", len(index.docstore.docs) if hasattr(index, 'docstore') else "Unknown")
    
    qe = index.as_query_engine(
        response_mode=RESPONSE_MODE,
        similarity_top_k=SIMILARITY_TOP_K,
        llm=llm_model,
    )
    return qe
