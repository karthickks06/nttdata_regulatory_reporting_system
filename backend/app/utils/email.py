"""Email notification utilities"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from app.core.config import settings


class EmailService:
    """Email notification service"""

    def __init__(
        self,
        smtp_host: str = "localhost",
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        body: str,
        from_address: str = "noreply@regulatory-system.com",
        cc_addresses: Optional[List[str]] = None,
        bcc_addresses: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        html: bool = False
    ) -> Dict[str, Any]:
        """
        Send email notification.

        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject
            body: Email body
            from_address: Sender address
            cc_addresses: CC addresses
            bcc_addresses: BCC addresses
            attachments: List of file paths to attach
            html: Whether body is HTML

        Returns:
            Send result
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_address
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            msg['Date'] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

            if cc_addresses:
                msg['Cc'] = ', '.join(cc_addresses)

            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {file_path.split("/")[-1]}'
                            )
                            msg.attach(part)
                    except Exception as e:
                        print(f"Failed to attach file {file_path}: {e}")

            # Send email
            all_recipients = to_addresses.copy()
            if cc_addresses:
                all_recipients.extend(cc_addresses)
            if bcc_addresses:
                all_recipients.extend(bcc_addresses)

            # Note: This is a placeholder implementation
            # In production, you would actually connect to SMTP server
            print(f"[EMAIL] Sending to: {', '.join(all_recipients)}")
            print(f"[EMAIL] Subject: {subject}")

            return {
                "success": True,
                "sent_to": len(all_recipients),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def send_workflow_notification(
        self,
        workflow_name: str,
        status: str,
        recipients: List[str],
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send workflow status notification"""
        subject = f"Workflow '{workflow_name}' - {status.upper()}"

        body = f"""
Workflow Status Update

Workflow: {workflow_name}
Status: {status}
Time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

"""

        if details:
            body += "\nDetails:\n"
            for key, value in details.items():
                body += f"  {key}: {value}\n"

        return await self.send_email(
            to_addresses=recipients,
            subject=subject,
            body=body
        )

    async def send_alert(
        self,
        alert_type: str,
        message: str,
        recipients: List[str],
        severity: str = "medium"
    ) -> Dict[str, Any]:
        """Send alert notification"""
        subject = f"[{severity.upper()}] Alert: {alert_type}"

        body = f"""
System Alert

Type: {alert_type}
Severity: {severity}
Message: {message}
Time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

This is an automated alert from the Regulatory Reporting System.
"""

        return await self.send_email(
            to_addresses=recipients,
            subject=subject,
            body=body
        )

    async def send_report_notification(
        self,
        report_name: str,
        report_path: str,
        recipients: List[str]
    ) -> Dict[str, Any]:
        """Send report generation notification"""
        subject = f"Report Generated: {report_name}"

        body = f"""
Report Generation Complete

Report: {report_name}
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

The report has been generated and is available at: {report_path}
"""

        return await self.send_email(
            to_addresses=recipients,
            subject=subject,
            body=body,
            attachments=[report_path] if report_path else None
        )
