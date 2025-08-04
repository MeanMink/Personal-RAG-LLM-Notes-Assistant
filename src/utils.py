import logging
from pathlib import Path
import os
import urllib.parse
from src.config import VAULT_NAME, NOTES_DIR


def get_logger(name=__name__):
    '''Simple logger setup'''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger(name)


def ensure_dir(path: Path):
    '''Ensure directories exist'''
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        
        
def make_obsidian_url(note_path, vault_name):
    """Generate Obsidian URL to open the specific note."""
    relative_path = os.path.relpath(note_path, NOTES_DIR)
    encoded_file = urllib.parse.quote(relative_path.replace(os.sep, '/'))
    return f"obsidian://open?vault={vault_name}&file={encoded_file}"


def make_folder_url(note_path):
    """Generate file:// URL to open the folder containing the note."""
    file_path = os.path.abspath(note_path)
    # Convert to forward slashes and ensure proper file:// URL format
    file_path = file_path.replace('\\', '/')
    encoded_path = urllib.parse.quote(file_path, safe='/')
    return f"file:///{encoded_path}"


def print_sources_with_links(source_nodes):
    """Print sources with clickable links to Obsidian and folder."""
    for node in source_nodes:
        note_path = node.node.metadata.get('file_path', 'Unknown')
        note_file = os.path.basename(note_path)
        obsidian_url = make_obsidian_url(note_path, VAULT_NAME)
        # folder_url = make_folder_url(note_path)
        print(f"Source: {note_file}")
        print(f" - Open in Obsidian: {obsidian_url}")
        # For debugging purposes
        # print(f" - Open folder: {folder_url}")
        print()