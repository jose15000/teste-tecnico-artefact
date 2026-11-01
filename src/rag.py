from __future__ import annotations

import functools
import os
import re
from pathlib import Path
from typing import Any

from fastembed import TextEmbedding
import numpy as np
import pymupdf

from src.data_loader import DATA_DIR, normalize_text

DEFAULT_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

STOPWORDS = {
    "qual", "quais", "como", "onde", "quando", "para", "com", "por", "sem",
    "que", "tem", "uma", "uns", "umas", "esse", "essa", "este", "esta",
    "voce", "voces", "loja", "musica", "emporio", "sobre", "mais",
}


def _find_pdf_path() -> Path:
    candidates = ["políticas_da_loja.pdf", "politicas_da_loja.pdf"]
    paths = [
        d / name for d in (DATA_DIR, Path("data")) for name in candidates
    ]
    return next((p for p in paths if p.exists()), DATA_DIR / candidates[0])


class PolicyRetriever:
    """Motor de busca híbrida (semântica densa + léxica) para as políticas da loja."""

    def __init__(
        self,
        pdf_path: str | Path | None = None,
        model_name: str = DEFAULT_MODEL,
    ):
        self.pdf_path = Path(pdf_path) if pdf_path else _find_pdf_path()
        self.chunks: list[dict[str, str]] = self._extract_chunks()
        self.model: TextEmbedding | None = None
        self.vectors: np.ndarray | None = None

        self._index_vectors(model_name)

    def _extract_chunks(self) -> list[dict[str, str]]:
        if not self.pdf_path.exists():
            return []

        doc = pymupdf.open(str(self.pdf_path))
        raw_text = "\n\n".join(page.get_text() for page in doc)
        doc.close()

        # Remove ruídos repetitivos de cabeçalho e numeração de páginas
        cleaned = re.sub(
            r"Empório\s+da\s+Música\s+Manual\s+de\s+Políticas[^\n]*|Página\s+\d+",
            "",
            raw_text,
        )

        # Segmenta por seções principais e subseções numeradas (1. a 10. e 1.1, 5.1, etc.)
        pattern = r"\n(?=(?:[0-9]+(?:\.[0-9]+)*\.?)\s+[A-ZÀ-Ú][^\n]+)"
        sections = [s.strip() for s in re.split(pattern, cleaned) if s.strip()]

        chunks: list[dict[str, str]] = []
        current_main = ""

        for sec in sections:
            lines = [line.strip() for line in sec.splitlines() if line.strip()]
            header = lines[0]

            # Identifica seção pai principal (ex.: '5. Política de Frete e Entregas')
            if re.match(r"^(?:[1-9]|10)\.\s+[A-ZÀ-Ú]", header):
                current_main = header
                # Se for apenas o título isolado sem corpo antes da primeira subseção, guarda contexto
                if len(lines) <= 1:
                    continue
                title = header
            elif re.match(r"^(?:[1-9]|10)\.[0-9]+", header) and current_main:
                title = f"{current_main} — {header}"
            else:
                title = header

            clean_content = re.sub(r"[ \t]+", " ", sec)
            chunks.append({
                "title": title,
                "content": clean_content,
                "norm_search": normalize_text(f"{title} {clean_content}"),
            })

        return chunks

    def _index_vectors(self, model_name: str) -> None:
        """Calcula matriz vetorial normalizada em memória com degradação segura."""
        if not self.chunks:
            return

        try:
            self.model = TextEmbedding(model_name=model_name)
            texts = [f"{c['title']}\n{c['content']}" for c in self.chunks]
            raw_embeddings = list(self.model.embed(texts))
            matrix = np.array(raw_embeddings, dtype=np.float32)

            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            self.vectors = matrix / np.maximum(norms, 1e-12)
        except Exception:
            # Fallback seguro caso o modelo ONNX não esteja acessível
            self.model = None
            self.vectors = None

    def search(self, query: str, top_k: int = 3) -> list[dict[str, str]]:
        if not self.chunks:
            return []

        scores = np.zeros(len(self.chunks), dtype=np.float32)

        # 1. Similaridade densa via embeddings (se disponível)
        if self.vectors is not None and self.model is not None:
            q_vec = np.array(list(self.model.embed([query]))[0], dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)
            if q_norm > 0:
                q_vec /= q_norm
            scores += np.dot(self.vectors, q_vec)

        # 2. Boost léxico para termos exatos e títulos
        norm_q = normalize_text(query)
        terms = [t for t in re.findall(r"\w+", norm_q) if len(t) > 2 and t not in STOPWORDS]

        for idx, chunk in enumerate(self.chunks):
            bonus = 0.0
            norm_title = normalize_text(chunk["title"])
            for term in terms:
                if term in norm_title:
                    bonus += 0.30
                elif term in chunk["norm_search"]:
                    bonus += 0.10
            scores[idx] += bonus

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices if scores[i] > 0.0]


@functools.lru_cache(maxsize=1)
def get_policy_retriever() -> PolicyRetriever:
    """Instância única com lazy-loading e cache."""
    return PolicyRetriever()


def search_policies(query: str, top_k: int = 3) -> dict[str, Any]:
    """Ferramenta para consulta às políticas e procedimentos da loja."""
    q = (query or "").strip()
    if not q:
        return {"error": "A busca não pode ser vazia."}

    results = get_policy_retriever().search(q, top_k=top_k)
    return {
        "total_found": len(results),
        "results": [
            {"title": r["title"], "content": r["content"]} for r in results
        ],
    }
