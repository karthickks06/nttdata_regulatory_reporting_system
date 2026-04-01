"""Notification background task"""

import asyncio
from typing import Dict, Any, List

from app.utils.email import send_email

async def send_notification(
    recipients: List[str],
    subject: str,
    body: str,
    notification_type: str = "email"
) -> Dict[str, Any]:
    """
    Send notification to users.
    
    Args:
        recipients: List of email addresses
        subject: Email subject
        body: Email body
        notification_type: Type of notification (email, slack, etc.)
        
    Returns:
        Sending results
    """
    if notification_type == "email":
        for recipient in recipients:
            try:
                await send_email(recipient, subject, body)
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")
        
        return {
            "status": "success",
            "sent": len(recipients)
        }
    
    return {"status": "unsupported", "type": notification_type}
