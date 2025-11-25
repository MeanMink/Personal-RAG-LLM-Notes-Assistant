# Notes RAG Assistant

A local semantic search engine for your Markdown notes. Built this because I got tired of forgetting what I wrote and where I wrote it.

---

## Why This Exists

I take a lot of notes—project ideas, research, Master's degree work, random thoughts at 2am. The problem? Finding anything later was a nightmare. Keyword search helps, but it misses the point when I can't remember the exact words I used.

So I built this: a way to ask questions about my notes and actually get useful answers. Everything runs locally with Ollama, so your notes stay private.

---

## What It Does

- Indexes all your `.md` files with semantic embeddings
- Lets you search by *meaning*, not just keywords
- Generates answers using your own notes as context
- Works completely offline

Think of it as Ctrl+F but it actually understands what you're looking for.

---

## How It Works

```text
notes-rag-assistant/
├── config.yaml       # Settings (models, paths, chunking params)
├── notes/            # Your .md files go here
├── storage/          # Vector embeddings stored here
└── src/
    ├── indexer.py    # Builds the search index
    └── cli.py        # Query interface
```

The basic flow:
1. Your notes get split into chunks (~512 tokens each)
2. Each chunk becomes a vector embedding via `nomic-embed-text`
3. When you ask a question, it finds the most relevant chunks
4. A local LLM (`phi3:mini-4k`) reads those chunks and answers

---

## Configuration

Here's what the `config.yaml` looks like:

```yaml
notes_folder: "notes/"
storage_folder: "storage/"
ollama_url: "http://localhost:11434"
embed_model: "nomic-embed-text"
llm_model: "phi3:mini-4k"
chunk_size: 512
chunk_overlap: 50
similarity_top_k: 4
response_mode: "compact"
```

**Key settings:**
- `embed_model`: I'm using `nomic-embed-text` because it handles longer text better than OpenAI's ada-002
- `llm_model`: `phi3:mini-4k` is lightweight enough to run locally without melting your laptop
- `chunk_size: 512`: Smaller chunks = more precise retrieval. Default is 1024 but I found 512 works better for note-style content
- `chunk_overlap: 50`: Prevents thoughts from getting cut off mid-sentence
- `similarity_top_k: 4`: Returns 4 relevant chunks per query—enough context without noise

---

## Setup

1. **Clone this repo**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Ollama running:**
   ```bash
   ollama server start
   ollama pull nomic-embed-text
   ollama pull phi3:mini-4k
   ```

4. **Add your notes to the `notes/` folder**  
   (Works great with Obsidian vaults—just symlink it)

5. **Build the index:**
   ```bash
   python -m src.indexer
   ```

6. **Ask questions:**
   ```bash
   python -m src.cli -q "What did I write about X?"
   ```

---

## Updating Your Notes

Added or changed some files? Just rebuild:

```bash
python -m src.cli -r
```

It only re-indexes what changed, so it's fast.

---
