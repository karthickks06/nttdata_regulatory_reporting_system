"""File operations utility functions"""

from typing import Optional, List, BinaryIO
from pathlib import Path
import shutil
import hashlib
from datetime import datetime
import aiofiles

from app.core.config import settings


async def save_uploaded_file(
    file: BinaryIO,
    filename: str,
    subdirectory: str = "uploads"
) -> dict:
    """
    Save uploaded file to storage.

    Args:
        file: File object
        filename: Target filename
        subdirectory: Subdirectory within storage path

    Returns:
        Dictionary with file info
    """
    try:
        # Create directory
        upload_dir = settings.STORAGE_PATH / "temp" / subdirectory
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_path = upload_dir / f"{timestamp}_{filename}"

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        # Calculate file hash
        file_hash = hashlib.sha256(content).hexdigest()

        return {
            "success": True,
            "file_path": str(file_path),
            "filename": filename,
            "size": len(content),
            "hash": file_hash
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def read_file(file_path: str) -> Optional[bytes]:
    """Read file contents"""
    try:
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
            return content
    except Exception:
        return None


async def write_file(file_path: str, content: bytes) -> bool:
    """Write content to file"""
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        return True
    except Exception:
        return False


async def delete_file(file_path: str) -> bool:
    """Delete file"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception:
        return False


async def move_file(source: str, destination: str) -> bool:
    """Move file from source to destination"""
    try:
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, destination)
        return True
    except Exception:
        return False


async def copy_file(source: str, destination: str) -> bool:
    """Copy file from source to destination"""
    try:
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return True
    except Exception:
        return False


async def list_files(directory: str, pattern: str = "*") -> List[str]:
    """List files in directory matching pattern"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return []

        files = [str(f) for f in dir_path.glob(pattern) if f.is_file()]
        return files
    except Exception:
        return []


async def get_file_info(file_path: str) -> Optional[dict]:
    """Get file information"""
    try:
        path = Path(file_path)

        if not path.exists():
            return None

        stats = path.stat()

        return {
            "path": str(path),
            "name": path.name,
            "size": stats.st_size,
            "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "extension": path.suffix
        }
    except Exception:
        return None


async def calculate_file_hash(file_path: str) -> Optional[str]:
    """Calculate SHA256 hash of file"""
    try:
        content = await read_file(file_path)
        if content:
            return hashlib.sha256(content).hexdigest()
        return None
    except Exception:
        return None


async def ensure_directory(directory: str) -> bool:
    """Ensure directory exists"""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


async def cleanup_temp_files(max_age_days: int = 1) -> int:
    """Clean up old temporary files"""
    try:
        temp_dir = settings.STORAGE_PATH / "temp"
        if not temp_dir.exists():
            return 0

        count = 0
        cutoff = datetime.utcnow().timestamp() - (max_age_days * 86400)

        for file_path in temp_dir.rglob("*"):
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff:
                    file_path.unlink()
                    count += 1

        return count
    except Exception:
        return 0
