"""Vector similarity search utilities"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(
    vector1: List[float],
    vector2: List[float]
) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vector1: First vector
        vector2: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    try:
        vec1 = np.array(vector1).reshape(1, -1)
        vec2 = np.array(vector2).reshape(1, -1)

        similarity = cosine_similarity(vec1, vec2)[0][0]
        return float(similarity)

    except Exception:
        return 0.0


def find_most_similar(
    query_vector: List[float],
    vectors: List[List[float]],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find most similar vectors to query vector.

    Args:
        query_vector: Query vector
        vectors: List of vectors to search
        top_k: Number of top results to return

    Returns:
        List of indices and similarity scores
    """
    try:
        query = np.array(query_vector).reshape(1, -1)
        vector_matrix = np.array(vectors)

        similarities = cosine_similarity(query, vector_matrix)[0]

        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "index": int(idx),
                "similarity": float(similarities[idx])
            })

        return results

    except Exception as e:
        return []


def calculate_euclidean_distance(
    vector1: List[float],
    vector2: List[float]
) -> float:
    """
    Calculate Euclidean distance between two vectors.

    Args:
        vector1: First vector
        vector2: Second vector

    Returns:
        Euclidean distance
    """
    try:
        vec1 = np.array(vector1)
        vec2 = np.array(vector2)

        distance = np.linalg.norm(vec1 - vec2)
        return float(distance)

    except Exception:
        return float('inf')


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize vector to unit length.

    Args:
        vector: Input vector

    Returns:
        Normalized vector
    """
    try:
        vec = np.array(vector)
        norm = np.linalg.norm(vec)

        if norm == 0:
            return vector

        normalized = vec / norm
        return normalized.tolist()

    except Exception:
        return vector


def batch_similarity_search(
    query_vectors: List[List[float]],
    corpus_vectors: List[List[float]],
    top_k: int = 5
) -> List[List[Dict[str, Any]]]:
    """
    Perform batch similarity search for multiple queries.

    Args:
        query_vectors: List of query vectors
        corpus_vectors: List of corpus vectors
        top_k: Number of top results per query

    Returns:
        List of results for each query
    """
    try:
        queries = np.array(query_vectors)
        corpus = np.array(corpus_vectors)

        # Calculate all similarities at once
        similarities = cosine_similarity(queries, corpus)

        results = []
        for query_similarities in similarities:
            # Get top k for this query
            top_indices = np.argsort(query_similarities)[::-1][:top_k]

            query_results = []
            for idx in top_indices:
                query_results.append({
                    "index": int(idx),
                    "similarity": float(query_similarities[idx])
                })

            results.append(query_results)

        return results

    except Exception:
        return []


def filter_by_similarity_threshold(
    query_vector: List[float],
    vectors: List[List[float]],
    threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Filter vectors by similarity threshold.

    Args:
        query_vector: Query vector
        vectors: List of vectors
        threshold: Minimum similarity threshold

    Returns:
        List of indices and scores above threshold
    """
    try:
        query = np.array(query_vector).reshape(1, -1)
        vector_matrix = np.array(vectors)

        similarities = cosine_similarity(query, vector_matrix)[0]

        results = []
        for idx, similarity in enumerate(similarities):
            if similarity >= threshold:
                results.append({
                    "index": idx,
                    "similarity": float(similarity)
                })

        # Sort by similarity descending
        results.sort(key=lambda x: x['similarity'], reverse=True)

        return results

    except Exception:
        return []


def calculate_vector_statistics(
    vectors: List[List[float]]
) -> Dict[str, Any]:
    """
    Calculate statistics for a set of vectors.

    Args:
        vectors: List of vectors

    Returns:
        Statistics dictionary
    """
    try:
        vector_matrix = np.array(vectors)

        stats = {
            "count": len(vectors),
            "dimensions": vector_matrix.shape[1] if len(vectors) > 0 else 0,
            "mean": vector_matrix.mean(axis=0).tolist(),
            "std": vector_matrix.std(axis=0).tolist(),
            "min": vector_matrix.min(axis=0).tolist(),
            "max": vector_matrix.max(axis=0).tolist()
        }

        # Calculate pairwise similarities
        if len(vectors) > 1:
            similarities = cosine_similarity(vector_matrix)
            # Get upper triangle (exclude diagonal)
            upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]

            stats["avg_similarity"] = float(upper_triangle.mean())
            stats["min_similarity"] = float(upper_triangle.min())
            stats["max_similarity"] = float(upper_triangle.max())

        return stats

    except Exception as e:
        return {
            "error": str(e)
        }


def create_vector_index(
    vectors: List[List[float]],
    index_type: str = "flat"
) -> Dict[str, Any]:
    """
    Create vector index for fast similarity search.

    Args:
        vectors: List of vectors
        index_type: Index type (flat, hnsw)

    Returns:
        Index information
    """
    # This is a simplified version
    # For production, use FAISS or similar library

    return {
        "success": True,
        "index_type": index_type,
        "vector_count": len(vectors),
        "dimensions": len(vectors[0]) if vectors else 0,
        "note": "Use FAISS or similar for production indexes"
    }
