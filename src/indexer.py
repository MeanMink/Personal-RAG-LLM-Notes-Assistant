# from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama
# from src.config import NOTES_DIR, STORAGE_DIR, EMBED_MODEL, LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, OLLAMA_URL
# from src.utils import ensure_dir, get_logger

# logger = get_logger('indexer')

# # Configure Ollama models 
# def configure_models():
#     return OllamaEmbedding(model_name=EMBED_MODEL, base_url=OLLAMA_URL), Ollama(model=LLM_MODEL, base_url=OLLAMA_URL)

# # Build or rebuild the index

# def build_index():
#     logger.info("Loading documents from %s", NOTES_DIR)
#     reader = SimpleDirectoryReader(str(NOTES_DIR), recursive=True, filename_as_id=True)
#     docs = reader.load_data()

#     splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
#     embed_model, _ = configure_models()
#     ensure_dir(STORAGE_DIR)
#     storage = StorageContext.from_defaults()

#     logger.info("Building vector index...")
#     index = VectorStoreIndex.from_documents(
#         docs,
#         storage_context=storage,
#         transformations=[splitter],
#         embed_model=embed_model
#     )
#     index.storage_context.persist(persist_dir=str(STORAGE_DIR))
#     logger.info("Index persisted to %s", STORAGE_DIR)

#     return index

from pathlib import Path
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from src.config import NOTES_DIR, STORAGE_DIR, EMBED_MODEL, LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, OLLAMA_URL
from src.utils import ensure_dir, get_logger

logger = get_logger('indexer')

def configure_models():
    return OllamaEmbedding(model_name=EMBED_MODEL, base_url=OLLAMA_URL), Ollama(model=LLM_MODEL, base_url=OLLAMA_URL)

def build_index():
    logger.info("Loading documents from %s", NOTES_DIR)
    reader = SimpleDirectoryReader(str(NOTES_DIR), recursive=True, filename_as_id=True)
    docs = reader.load_data()

    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    embed_model, _ = configure_models()
    
    # Clear existing index directory to ensure fresh start
    import shutil
    storage_dir_path = Path(STORAGE_DIR)
    if storage_dir_path.exists():
        logger.info("Clearing existing index directory...")
        shutil.rmtree(storage_dir_path)
    
    ensure_dir(STORAGE_DIR)
    
    # Always create fresh storage context
    storage = StorageContext.from_defaults()

    logger.info("Building vector index...")
    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=storage,
        transformations=[splitter],
        embed_model=embed_model
    )
    
    # Persist the index
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    logger.info("Index persisted to %s", STORAGE_DIR)

    return index

