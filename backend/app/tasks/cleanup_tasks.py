"""Background cleanup tasks for expired sessions, cache, and rate limits"""

import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import shutil

from sqlalchemy import text
from app.db.postgres import engine
from app.core.config import settings


class CleanupScheduler:
    """Manages periodic cleanup of expired data"""

    def __init__(self):
        self.running = False

    async def run_cleanup_loop(self):
        """Run cleanup tasks periodically"""
        self.running = True

        while self.running:
            try:
                await self.cleanup_expired_data()
                # Sleep for configured interval
                await asyncio.sleep(settings.CLEANUP_INTERVAL_HOURS * 3600)
            except Exception as e:
                print(f"❌ Cleanup error: {e}")
                await asyncio.sleep(300)  # Retry after 5 minutes on error

    async def cleanup_expired_data(self):
        """Clean up expired sessions, cache, rate limits, and temp files"""
        print("🧹 Starting cleanup task...")

        async with engine.begin() as conn:
            # Clean expired sessions
            session_expiry = datetime.utcnow() - timedelta(days=settings.SESSION_EXPIRY_DAYS)
            result = await conn.execute(
                text("DELETE FROM sessions WHERE expires_at < :expiry"),
                {"expiry": session_expiry}
            )
            print(f"  ✓ Deleted {result.rowcount} expired sessions")

            # Clean expired cache
            cache_expiry = datetime.utcnow()
            result = await conn.execute(
                text("DELETE FROM cache WHERE expires_at < :expiry"),
                {"expiry": cache_expiry}
            )
            print(f"  ✓ Deleted {result.rowcount} expired cache entries")

            # Clean expired rate limits
            rate_limit_expiry = datetime.utcnow()
            result = await conn.execute(
                text("DELETE FROM rate_limits WHERE expires_at < :expiry"),
                {"expiry": rate_limit_expiry}
            )
            print(f"  ✓ Deleted {result.rowcount} expired rate limit entries")

            # Clean old temp files
            temp_path = Path(settings.STORAGE_PATH) / "temp"
            if temp_path.exists():
                cutoff_time = datetime.utcnow() - timedelta(days=settings.TEMP_FILE_EXPIRY_DAYS)
                deleted_count = 0

                for item in temp_path.rglob("*"):
                    if item.is_file():
                        file_mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if file_mtime < cutoff_time:
                            item.unlink()
                            deleted_count += 1

                print(f"  ✓ Deleted {deleted_count} old temporary files")

        print("✅ Cleanup task completed")

    def stop(self):
        """Stop the cleanup scheduler"""
        self.running = False
