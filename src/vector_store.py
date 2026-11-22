import re
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def create_vector_store(chunks):
    """
    Create embeddings for PDF chunks using Sentence Transformers.
    """

    if not chunks:
        raise ValueError("No text chunks available.")

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    return embeddings, chunks, model


def search_similar_chunks(question, embeddings, chunks, model, top_k=5):
    """
    Hybrid search using semantic similarity and keyword matching.
    """

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    semantic_scores = np.dot(
        embeddings,
        question_embedding.T
    ).flatten()

    keywords = set(
        re.findall(r"\b[a-zA-Z]+\b", question.lower())
    )

    scores = []

    for idx, chunk in enumerate(chunks):
        chunk_words = set(
            re.findall(r"\b[a-zA-Z]+\b", chunk["text"].lower())
        )

        matches = keywords.intersection(chunk_words)

        keyword_score = len(matches) / max(len(keywords), 1)

        final_score = (
            0.7 * semantic_scores[idx]
            + 0.3 * keyword_score
        )

        scores.append(final_score)

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append({
            "text": chunks[idx]["text"],
            "page": chunks[idx]["page"],
            "score": float(scores[idx])
        })

    return results
