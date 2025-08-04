import yaml
from pathlib import Path

# Load configuration from config.yaml
BASE_DIR = Path(__file__).parent.parent
cfg_path = BASE_DIR / "config.yaml"
with open(cfg_path, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

# Expose settings
NOTES_DIR = BASE_DIR / cfg['notes_folder']
VAULT_NAME = "notes"
STORAGE_DIR = BASE_DIR / cfg['storage_folder']
OLLAMA_URL = cfg['ollama_url']
EMBED_MODEL = cfg['embed_model']
LLM_MODEL = cfg['llm_model']
CHUNK_SIZE = cfg['chunk_size']
CHUNK_OVERLAP = cfg['chunk_overlap']
SIMILARITY_TOP_K = cfg['similarity_top_k']
RESPONSE_MODE = cfg['response_mode']