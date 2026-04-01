"""Document processing background task"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import AsyncSessionLocal
from app.models.regulatory_update import RegulatoryUpdate
from app.sub_agents.document_parser import DocumentParser
from sqlalchemy import select, update

async def process_document(update_id: int) -> Dict[str, Any]:
    """
    Process a regulatory update document.
    
    Args:
        update_id: ID of regulatory update to process
        
    Returns:
        Processing results
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(RegulatoryUpdate).where(RegulatoryUpdate.id == update_id)
        )
        update = result.scalar_one_or_none()
        
        if not update or not update.file_path:
            return {"error": "Update or file not found"}
        
        # Parse document
        parser = DocumentParser()
        parsed_data = await parser.parse_document(Path(update.file_path))
        
        # Mark as processed
        await db.execute(
            update(RegulatoryUpdate)
            .where(RegulatoryUpdate.id == update_id)
            .values(is_processed=True)
        )
        await db.commit()
        
        return {
            "status": "success",
            "text": parsed_data.get("text", ""),
            "entities": parsed_data.get("entities", [])
        }
