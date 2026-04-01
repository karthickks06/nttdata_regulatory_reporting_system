"""Embeddings and tiktoken storage service"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import numpy as np
from datetime import datetime
import hashlib

from app.core.config import settings


class EmbeddingStorageService:
    """Service for storing and retrieving embeddings and tiktoken data"""

    def __init__(self):
        self.embeddings_dir = settings.STORAGE_PATH / "embeddings"
        self.vectors_dir = self.embeddings_dir / "vectors"
        self.tiktoken_cache_dir = self.embeddings_dir / "tiktoken_cache"
        self.indexes_dir = self.embeddings_dir / "indexes"

        # Ensure directories exist
        for directory in [self.vectors_dir, self.tiktoken_cache_dir, self.indexes_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    async def save_embeddings(
        self,
        embedding_id: str,
        embeddings: List[List[float]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save embeddings to storage.

        Args:
            embedding_id: Unique identifier
            embeddings: List of embedding vectors
            metadata: Additional metadata

        Returns:
            Save result
        """
        try:
            # Save as numpy array
            npy_path = self.vectors_dir / f"{embedding_id}.npy"
            embeddings_array = np.array(embeddings)
            np.save(npy_path, embeddings_array)

            # Save metadata
            meta_path = self.vectors_dir / f"{embedding_id}_metadata.json"
            meta_data = {
                "embedding_id": embedding_id,
                "shape": embeddings_array.shape,
                "dtype": str(embeddings_array.dtype),
                "saved_at": datetime.utcnow().isoformat(),
                **(metadata or {})
            }

            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, indent=2)

            return {
                "success": True,
                "embedding_id": embedding_id,
                "file_path": str(npy_path),
                "shape": list(embeddings_array.shape)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def load_embeddings(
        self,
        embedding_id: str
    ) -> Optional[np.ndarray]:
        """
        Load embeddings from storage.

        Args:
            embedding_id: Embedding identifier

        Returns:
            Numpy array of embeddings or None
        """
        try:
            npy_path = self.vectors_dir / f"{embedding_id}.npy"

            if not npy_path.exists():
                return None

            embeddings = np.load(npy_path)
            return embeddings

        except Exception:
            return None

    async def cache_tiktoken_result(
        self,
        text: str,
        tokens: List[int],
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Cache tiktoken tokenization result.

        Args:
            text: Input text
            tokens: Token IDs
            model: Model name

        Returns:
            Cache result
        """
        try:
            # Create hash of text for cache key
            text_hash = hashlib.sha256(text.encode()).hexdigest()

            cache_file = self.tiktoken_cache_dir / f"{text_hash}.json"

            cache_data = {
                "text_hash": text_hash,
                "text_preview": text[:100],
                "tokens": tokens,
                "token_count": len(tokens),
                "model": model,
                "cached_at": datetime.utcnow().isoformat()
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f)

            return {
                "success": True,
                "cache_key": text_hash,
                "token_count": len(tokens)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_cached_tokens(
        self,
        text: str
    ) -> Optional[List[int]]:
        """
        Get cached tiktoken result.

        Args:
            text: Input text

        Returns:
            Cached tokens or None
        """
        try:
            text_hash = hashlib.sha256(text.encode()).hexdigest()
            cache_file = self.tiktoken_cache_dir / f"{text_hash}.json"

            if not cache_file.exists():
                return None

            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            return cache_data.get("tokens")

        except Exception:
            return None

    async def save_embedding_index(
        self,
        index_id: str,
        index_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save embedding index metadata"""
        try:
            index_file = self.indexes_dir / f"{index_id}.json"

            data = {
                "index_id": index_id,
                "index_data": index_data,
                "created_at": datetime.utcnow().isoformat()
            }

            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            return {
                "success": True,
                "index_id": index_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_embedding_statistics(
        self,
        embedding_id: str
    ) -> Dict[str, Any]:
        """Get statistics for stored embeddings"""
        try:
            embeddings = await self.load_embeddings(embedding_id)

            if embeddings is None:
                return {
                    "success": False,
                    "error": "Embeddings not found"
                }

            stats = {
                "shape": list(embeddings.shape),
                "mean": float(embeddings.mean()),
                "std": float(embeddings.std()),
                "min": float(embeddings.min()),
                "max": float(embeddings.max())
            }

            return {
                "success": True,
                "statistics": stats
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def list_embeddings(self) -> Dict[str, Any]:
        """List all stored embeddings"""
        try:
            embeddings = []

            for meta_file in self.vectors_dir.glob("*_metadata.json"):
                with open(meta_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    embeddings.append(metadata)

            return {
                "success": True,
                "embeddings": embeddings,
                "count": len(embeddings)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
