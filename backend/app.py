#!/usr/bin/env python3
"""
Main application entry point for NTT Data Regulatory Reporting System.

Run this file to start the entire backend:
- FastAPI server
- Background cleanup scheduler
- Task queue worker
- WebSocket support
- Automatic database table creation
- Automatic data seeding

Usage:
    python app.py
"""

import asyncio
import sys
import signal
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from app.main import app
from app.tasks.cleanup_tasks import CleanupScheduler
from app.core.config import settings


class ApplicationRunner:
    """Manages all application services in a single process"""

    def __init__(self):
        self.cleanup_scheduler = CleanupScheduler()
        self.running = True

    def initialize_system(self):
        """Run initialization tasks on first startup"""
        print("🔧 Initializing system...")

        # 1. Setup storage directories
        print("📁 Setting up storage directories...")
        from scripts.setup_storage import setup_storage
        setup_storage()

        # 2. Initialize database and create tables
        print("🗄️  Initializing database...")
        try:
            from app.db.postgres import engine, Base
            from sqlalchemy import text, inspect

            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection successful")

            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()

            if len(existing_tables) == 0:
                print("📋 No tables found. Creating database schema...")

                # Import all models to register them with Base
                from app.models import (
                    user, role, permission, session, cache, rate_limit,
                    task_queue, regulatory_update, requirement, data_mapping,
                    generated_code, test_case, report, workflow,
                    file_metadata, audit_log
                )

                # Create all tables
                Base.metadata.create_all(bind=engine)
                print(f"✅ Created {len(Base.metadata.tables)} database tables")

                # Run initial data seeding
                print("👤 Seeding initial data...")
                from scripts.seed_data import seed_data
                seed_data()
                print("✅ Initial data seeded successfully")
            else:
                print(f"✅ Found {len(existing_tables)} existing tables")

                # Check if admin user exists
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM users"))
                    user_count = result.scalar()

                    if user_count == 0:
                        print("👤 No users found. Running seed_data...")
                        from scripts.seed_data import seed_data
                        seed_data()
                        print("✅ Initial data seeded successfully")
                    else:
                        print(f"✅ Found {user_count} users in database")

        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            print("\n📝 Please ensure:")
            print("  1. PostgreSQL is running")
            print("  2. Database 'regulatory_reporting' exists")
            print("  3. Database user has CREATE TABLE permissions")
            sys.exit(1)

        # 3. Setup ChromaDB
        print("🔍 Initializing ChromaDB...")
        try:
            from app.db.chroma_db import get_chroma_client
            client = get_chroma_client()
            collections = client.list_collections()
            print(f"✅ ChromaDB initialized ({len(collections)} collections)")
        except Exception as e:
            print(f"⚠️  ChromaDB warning: {e}")

        print("✅ System initialization complete!\n")

    async def start_background_services(self):
        """Start all background services"""
        print("🚀 Starting background services...")

        # Start cleanup scheduler
        asyncio.create_task(self.cleanup_scheduler.run_cleanup_loop())
        print("✅ Cleanup scheduler started")

        # Start task queue worker
        from app.tasks.agent_execution import TaskQueueWorker
        self.task_worker = TaskQueueWorker()
        asyncio.create_task(self.task_worker.run())
        print("✅ Task queue worker started")

    def setup_signal_handlers(self):
        """Setup graceful shutdown"""
        def signal_handler(sig, frame):
            print("\n⚠️  Shutting down gracefully...")
            self.running = False
            self.cleanup_scheduler.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def run(self):
        """Run the application"""
        self.setup_signal_handlers()

        print("=" * 60)
        print("🏦 NTT Data Regulatory Reporting System")
        print("=" * 60)

        # Run initialization
        self.initialize_system()

        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"API URL: http://{settings.HOST}:{settings.PORT}")
        print(f"API Docs: http://{settings.HOST}:{settings.PORT}/api/v1/docs")
        print(f"Storage: {settings.STORAGE_PATH}")
        print("=" * 60)

        # Configure uvicorn
        config = uvicorn.Config(
            app=app,
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info",
            access_log=True,
        )

        server = uvicorn.Server(config)

        # Start background services on startup
        @app.on_event("startup")
        async def startup_event():
            await self.start_background_services()
            print("✅ All services started successfully!")

        @app.on_event("shutdown")
        async def shutdown_event():
            print("⚠️  Shutting down services...")
            self.cleanup_scheduler.stop()

        # Run the server
        server.run()


if __name__ == "__main__":
    runner = ApplicationRunner()
    runner.run()
