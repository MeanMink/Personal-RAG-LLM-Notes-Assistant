Here's how it all works -- majority of it written by ChatGPT :)))) --- but tweaked and fact-checked by me of course!!!

# 🧠 Notes RAG Assistant

Your **second brain** over your personal Obsidian-style notes. Use a local LLM via \[Ollama] with \[LlamaIndex] to semantically search, connect, and *understand* your scattered Markdown notes—no more lost insights.

---

## 🚀 What It Does

* 🤖 **Builds a semantic index** of your `*.md` notes
* 🔍 **Performs similarity-based search** (not just keyword)
* 💡 **Synthesizes answers** with your own writing as context

All locally, using **Ollama** (for embeddings + LLM) and **LlamaIndex** (for chunking, embedding, retrieving).

---

## 📂 Repo Structure

```text
notes-rag-assistant/
├── config.yaml
├── notes/           ← Put your Obsidian `.md` files here
├── storage/         ← Holds embedding indices (auto-generated; add to `.gitignore`)
└── src/
    ├── index_notes.py    ← Build or update the vector store
    └── query_notes.py    ← Ask questions using the RAG engine
```

The key idea:

* `notes/` = your personal Markdown files
* `storage/` = where processed vectors and metadata are saved
* `config.yaml` = central configuration (paths, model names, chunking, etc.)
* `src/` = indexing and querying scripts you run directly

---

## ⚙️ `config.yaml`

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

| Config Key         | Description                                                                                                                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `notes_folder`     | Path with your `.md` files (recursively). If empty, nothing gets indexed.                                                                                                                                                                                                       |
| `storage_folder`   | Directory where LlamaIndex saves the vector store. Usually permanent.                                                                                                                                                                                                           |
| `ollama_url`       | Defaults to `http://localhost:11434`—Ollama’s default REST API endpoint.                                                                                                                                                                                                        |
| `embed_model`      | Embedding model name (via Ollama). We recommend `"nomic-embed-text"` for great semantic quality and long-context encoding, outperforming OpenAI's `text-embedding-ada-002` especially on longer inputs ([LlamaIndex][1], [rocm.docs.amd.com][2], [LlamaIndex][3], [Ollama][4]). |
| `llm_model`        | LLM to run locally via Ollama—`"phi3:mini-4k"` is a lightweight and efficient \~3 B parameter model with a 4K context window, excellent for local use ([Ollama][5], [Ollama][6]).                                                                                               |
| `chunk_size`       | Max tokens per chunk: 512 is smaller than LlamaIndex’s default (1024) and yields finer-grained semantic retrieval, with better precision on note-like content ([LlamaIndex][7], [LlamaIndex][8]).                                                                               |
| `chunk_overlap`    | How many tokens overlap between adjacent chunks (50 here instead of the default 20). This ensures continuity across splits—even if a thought spans chunk boundaries.                                                                                                            |
| `similarity_top_k` | Number of top similar chunks returned for each query. `4` is a sweet spot if chunks are smaller—gives enough context without overwhelming the model.                                                                                                                            |
| `response_mode`    | LlamaIndex generates answers by “stitching” retrieved chunks. `"compact"` is lean and to-the-point. Other modes like `"refine"` or `"tree_summarize"` give longer, thought-out responses.                                                                                       |

---

## 🧠 What "Indexing" Means (Simple Version)

1. **Chunking**: each Markdown file is broken into \~512-token segments (with overlap), so you can embed them effectively.
2. **Embedding**: every chunk is converted into a high-dimensional vector using `nomic‑embed‑text`.
3. **Storing**: these embeddings (plus metadata & pointers to your raw Markdown) get saved under `storage/`.
4. **Querying**: when you ask a question:

   * the question is embedded the same way,
   * LlamaIndex finds the top‑K most similar chunks by cosine similarity,
   * your local LLM (`phi3:mini‑4k`) uses those retrieved chunks as context to generate a meaningful, semantically-informed answer.

👉 This leverages meaning, context, and recall—so even if you don't remember which file or filename you wrote something in, the system finds it for you.

---

## 🛠️ Quick Start

1. **Clone the repo** and `cd` into it.

2. **Install the dependencies**:

   ```bash
   python3 -m pip install llama-index llama-index-embeddings-ollama llama-index-llms-ollama ollama
   ```

3. **Set up Ollama**:

   ```bash
   ollama server start
   ollama pull nomic-embed-text
   ollama pull phi3:mini-4k
   ```

4. **Place your Obsidian `.md` files** into the `notes/` folder (you can symlink your vault).

5. **Build the index**:

   ```bash
   python src/index_notes.py --config config.yaml
   ```

6. **Ask a question**:

   ```bash
   python src/query_notes.py --config config.yaml --question "Where did I outline the research plan?"
   ```

---

## ♻️ Updating Notes

Add, edit, or remove Markdown files in `notes/` and re-run:

```bash
python src/index_notes.py --config config.yaml --refresh
```

Only changed files will be re-indexed, so it’s fast too.

---

## 💡 Why I Built This

* I *write a lot* of notes—ideas, essays, planning documents…
* Keyword search is okay, but misses the **meaning connections**
* I kept forgetting what I *already wrote*: “Was that idea in project X or my reading notes?”
* → So I built a **local, semantic search + answer engine** over my actual words

This gives you full control, offline functionality, and a way to intelligently *ask your past self* what you thought about something.

---

## ✅ TL;DR

* Put your `.md` files into `notes/`
* Configure paths, embedding and LLM models in `config.yaml`
* Run `index_notes.py` to build semantic index under `storage/`
* Ask natural-language questions via `cli.py` and get answers grounded in your own writing

Feel free to tweak chunk parameters, embedding/LMM models, or respond with interactive UI. Fork, pull requests, feedback—I’d love to see what you build with this.

