"""
Notification Service - Email and in-app notifications
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.utils.email import send_email
from app.core.config import settings


class NotificationService:
    """Service for managing notifications"""

    @staticmethod
    async def send_workflow_notification(
        db: AsyncSession,
        user_id: UUID,
        workflow_id: UUID,
        workflow_name: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send workflow status notification"""
        user = await NotificationService._get_user(db, user_id)
        if not user:
            return False

        subject = f"Workflow {status.title()}: {workflow_name}"
        body = NotificationService._format_workflow_email(
            workflow_name, status, workflow_id, details
        )

        return await send_email(
            to_email=user.email,
            subject=subject,
            body=body
        )

    @staticmethod
    async def send_approval_request(
        db: AsyncSession,
        approver_id: UUID,
        entity_type: str,
        entity_id: UUID,
        requester_name: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send approval request notification"""
        user = await NotificationService._get_user(db, approver_id)
        if not user:
            return False

        subject = f"Approval Required: {entity_type}"
        body = NotificationService._format_approval_email(
            entity_type, entity_id, requester_name, details
        )

        return await send_email(
            to_email=user.email,
            subject=subject,
            body=body
        )

    @staticmethod
    async def send_approval_decision(
        db: AsyncSession,
        requester_id: UUID,
        entity_type: str,
        entity_id: UUID,
        approved: bool,
        approver_name: str,
        comments: Optional[str] = None
    ) -> bool:
        """Send approval decision notification"""
        user = await NotificationService._get_user(db, requester_id)
        if not user:
            return False

        status = "Approved" if approved else "Rejected"
        subject = f"{entity_type} {status}"
        body = NotificationService._format_decision_email(
            entity_type, entity_id, approved, approver_name, comments
        )

        return await send_email(
            to_email=user.email,
            subject=subject,
            body=body
        )

    @staticmethod
    async def send_report_notification(
        db: AsyncSession,
        user_id: UUID,
        report_name: str,
        report_id: UUID,
        status: str,
        validation_results: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send report generation/validation notification"""
        user = await NotificationService._get_user(db, user_id)
        if not user:
            return False

        subject = f"Report {status.title()}: {report_name}"
        body = NotificationService._format_report_email(
            report_name, report_id, status, validation_results
        )

        return await send_email(
            to_email=user.email,
            subject=subject,
            body=body
        )

    @staticmethod
    async def send_error_notification(
        db: AsyncSession,
        admin_emails: List[str],
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send error notification to administrators"""
        subject = f"System Error: {error_type}"
        body = NotificationService._format_error_email(
            error_type, error_message, context
        )

        success = True
        for email in admin_emails:
            result = await send_email(
                to_email=email,
                subject=subject,
                body=body
            )
            success = success and result

        return success

    @staticmethod
    async def send_batch_notification(
        db: AsyncSession,
        user_ids: List[UUID],
        subject: str,
        body: str
    ) -> Dict[UUID, bool]:
        """Send notification to multiple users"""
        results = {}

        for user_id in user_ids:
            user = await NotificationService._get_user(db, user_id)
            if user:
                results[user_id] = await send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )
            else:
                results[user_id] = False

        return results

    @staticmethod
    async def send_regulatory_update_notification(
        db: AsyncSession,
        user_ids: List[UUID],
        update_title: str,
        update_id: UUID,
        source: str,
        effective_date: Optional[datetime] = None
    ) -> Dict[UUID, bool]:
        """Send regulatory update notification to relevant users"""
        subject = f"New Regulatory Update: {update_title}"
        body = NotificationService._format_regulatory_update_email(
            update_title, update_id, source, effective_date
        )

        return await NotificationService.send_batch_notification(
            db, user_ids, subject, body
        )

    @staticmethod
    async def _get_user(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _format_workflow_email(
        workflow_name: str,
        status: str,
        workflow_id: UUID,
        details: Optional[Dict[str, Any]]
    ) -> str:
        """Format workflow notification email"""
        body = f"""
        <html>
        <body>
            <h2>Workflow Status Update</h2>
            <p><strong>Workflow:</strong> {workflow_name}</p>
            <p><strong>Status:</strong> {status.upper()}</p>
            <p><strong>Workflow ID:</strong> {workflow_id}</p>
        """

        if details:
            body += "<h3>Details:</h3><ul>"
            for key, value in details.items():
                body += f"<li><strong>{key}:</strong> {value}</li>"
            body += "</ul>"

        body += f"""
            <p>View workflow details at: <a href="{settings.FRONTEND_URL}/workflows/{workflow_id}">{settings.FRONTEND_URL}/workflows/{workflow_id}</a></p>
        </body>
        </html>
        """
        return body

    @staticmethod
    def _format_approval_email(
        entity_type: str,
        entity_id: UUID,
        requester_name: str,
        details: Optional[Dict[str, Any]]
    ) -> str:
        """Format approval request email"""
        body = f"""
        <html>
        <body>
            <h2>Approval Required</h2>
            <p><strong>Type:</strong> {entity_type}</p>
            <p><strong>Requested by:</strong> {requester_name}</p>
            <p><strong>ID:</strong> {entity_id}</p>
        """

        if details:
            body += "<h3>Details:</h3><ul>"
            for key, value in details.items():
                body += f"<li><strong>{key}:</strong> {value}</li>"
            body += "</ul>"

        body += f"""
            <p>Please review and approve/reject at: <a href="{settings.FRONTEND_URL}/approvals">{settings.FRONTEND_URL}/approvals</a></p>
        </body>
        </html>
        """
        return body

    @staticmethod
    def _format_decision_email(
        entity_type: str,
        entity_id: UUID,
        approved: bool,
        approver_name: str,
        comments: Optional[str]
    ) -> str:
        """Format approval decision email"""
        status = "APPROVED" if approved else "REJECTED"
        body = f"""
        <html>
        <body>
            <h2>{entity_type} {status}</h2>
            <p><strong>Decision:</strong> {status}</p>
            <p><strong>Decided by:</strong> {approver_name}</p>
            <p><strong>ID:</strong> {entity_id}</p>
        """

        if comments:
            body += f"<p><strong>Comments:</strong> {comments}</p>"

        body += """
        </body>
        </html>
        """
        return body

    @staticmethod
    def _format_report_email(
        report_name: str,
        report_id: UUID,
        status: str,
        validation_results: Optional[Dict[str, Any]]
    ) -> str:
        """Format report notification email"""
        body = f"""
        <html>
        <body>
            <h2>Report Status Update</h2>
            <p><strong>Report:</strong> {report_name}</p>
            <p><strong>Status:</strong> {status.upper()}</p>
            <p><strong>Report ID:</strong> {report_id}</p>
        """

        if validation_results:
            body += "<h3>Validation Results:</h3><ul>"
            for key, value in validation_results.items():
                body += f"<li><strong>{key}:</strong> {value}</li>"
            body += "</ul>"

        body += f"""
            <p>View report at: <a href="{settings.FRONTEND_URL}/reports/{report_id}">{settings.FRONTEND_URL}/reports/{report_id}</a></p>
        </body>
        </html>
        """
        return body

    @staticmethod
    def _format_error_email(
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Format error notification email"""
        body = f"""
        <html>
        <body>
            <h2>System Error Alert</h2>
            <p><strong>Error Type:</strong> {error_type}</p>
            <p><strong>Message:</strong> {error_message}</p>
            <p><strong>Time:</strong> {datetime.utcnow().isoformat()}</p>
        """

        if context:
            body += "<h3>Context:</h3><ul>"
            for key, value in context.items():
                body += f"<li><strong>{key}:</strong> {value}</li>"
            body += "</ul>"

        body += """
        </body>
        </html>
        """
        return body

    @staticmethod
    def _format_regulatory_update_email(
        update_title: str,
        update_id: UUID,
        source: str,
        effective_date: Optional[datetime]
    ) -> str:
        """Format regulatory update notification email"""
        body = f"""
        <html>
        <body>
            <h2>New Regulatory Update</h2>
            <p><strong>Title:</strong> {update_title}</p>
            <p><strong>Source:</strong> {source}</p>
        """

        if effective_date:
            body += f"<p><strong>Effective Date:</strong> {effective_date.strftime('%Y-%m-%d')}</p>"

        body += f"""
            <p>View update at: <a href="{settings.FRONTEND_URL}/regulatory-updates/{update_id}">{settings.FRONTEND_URL}/regulatory-updates/{update_id}</a></p>
        </body>
        </html>
        """
        return body
