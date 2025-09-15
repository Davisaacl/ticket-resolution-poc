import os, json
from typing import List, Tuple
import numpy as np
import faiss

try:
    from sentence_transformers import SentenceTransformer
    # Use env EMBED_MODEL if set, otherwise default
    _embedder = SentenceTransformer(os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2"))
    def embed_texts(texts: List[str]) -> np.ndarray:
        return np.array(_embedder.encode(texts, normalize_embeddings=True))
except Exception:
    _embedder = None
    def embed_texts(texts: List[str]) -> np.ndarray:
        # Fallback: generates deterministic random vectors so PoC still works
        rng = np.random.default_rng(42)
        return rng.normal(size=(len(texts), 384))

class VectorStore:
    def __init__(self, dim=384, path="kb.index", meta_path="kb_meta.json"):
        self.dim = dim
        self.path = path
        self.meta_path = meta_path
        self.meta: List[str] = []
        if os.path.exists(path) and os.path.exists(meta_path):
            self.index = faiss.read_index(path)
            self.meta = json.load(open(meta_path, "r", encoding="utf-8"))
        else:
            self.index = faiss.IndexFlatIP(dim)

    def build(self, docs: List[str]):
        """Build a new index with provided docs."""
        embs = embed_texts(docs).astype("float32")
        self.index = faiss.IndexFlatIP(embs.shape[1])
        self.index.add(embs)
        self.meta = docs
        faiss.write_index(self.index, self.path)
        json.dump(self.meta, open(self.meta_path, "w", encoding="utf-8"))

    def search(self, query: str, k=5) -> List[Tuple[str, float]]:
        """Return top-k docs with similarity score."""
        if not self.meta:
            return []
        q = embed_texts([query]).astype("float32")
        D, I = self.index.search(q, min(k, len(self.meta)))
        return [(self.meta[i], float(D[0][j])) for j, i in enumerate(I[0])]
