"""
Email Sender for CreatorPulse
Handles sending newsletters via Resend API
"""

import os
from typing import List, Optional, Dict
import resend
import markdown


class NewsletterEmailSender:
    """Send newsletters via Resend API"""

    def __init__(self):
        self.api_key = os.getenv('RESEND_API_KEY')
        if self.api_key:
            resend.api_key = self.api_key

    def send_newsletter(
        self,
        to_emails: List[str],
        subject: str,
        content: str,
        from_email: str = "CreatorPulse <newsletter@resend.dev>",
        reply_to: Optional[str] = None
    ) -> Dict:
        """
        Send a newsletter to a list of recipients

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject line
            content: Newsletter content (Markdown format)
            from_email: Sender email (must be verified domain)
            reply_to: Optional reply-to email address

        Returns:
            Dictionary with send results
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'RESEND_API_KEY not configured',
                'message': 'Please add your Resend API key to .env file'
            }

        try:
            # Convert Markdown to HTML
            html_content = self._markdown_to_html(content)

            # Send email via Resend
            params = {
                "from": from_email,
                "to": to_emails,
                "subject": subject,
                "html": html_content,
                "text": content  # Fallback plain text
            }

            if reply_to:
                params["reply_to"] = reply_to

            response = resend.Emails.send(params)

            return {
                'success': True,
                'id': response.get('id'),
                'recipients': len(to_emails),
                'message': f'Newsletter sent to {len(to_emails)} recipient(s)'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to send newsletter: {str(e)}'
            }

    def send_test_email(
        self,
        test_email: str,
        subject: str,
        content: str,
        from_email: str = "CreatorPulse <newsletter@resend.dev>"
    ) -> Dict:
        """
        Send a test newsletter to a single email address

        Args:
            test_email: Test recipient email
            subject: Email subject
            content: Newsletter content (Markdown)
            from_email: Sender email

        Returns:
            Dictionary with send results
        """
        return self.send_newsletter(
            to_emails=[test_email],
            subject=f"[TEST] {subject}",
            content=content,
            from_email=from_email
        )

    def _markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert Markdown to HTML with newsletter styling

        Args:
            markdown_content: Newsletter in Markdown format

        Returns:
            HTML formatted email
        """
        # Convert markdown to HTML
        html_body = markdown.markdown(
            markdown_content,
            extensions=['extra', 'codehilite', 'tables']
        )

        # Wrap in email template
        html_email = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #6366f1;
            border-bottom: 3px solid #6366f1;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #1e40af;
            margin-top: 30px;
        }}
        h3 {{
            color: #4b5563;
        }}
        a {{
            color: #6366f1;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        blockquote {{
            border-left: 4px solid #6366f1;
            margin: 20px 0;
            padding-left: 20px;
            color: #6b7280;
            font-style: italic;
        }}
        code {{
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #1f2937;
            color: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.875rem;
            color: #6b7280;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
        <div class="footer">
            <p>Sent via CreatorPulse | <a href="#">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
        """

        return html_email

    def validate_api_key(self) -> bool:
        """Check if Resend API key is configured"""
        return bool(self.api_key)

    def get_sender_info(self) -> Dict:
        """Get information about the configured sender"""
        if not self.api_key:
            return {
                'configured': False,
                'message': 'Resend API key not found in environment variables'
            }

        return {
            'configured': True,
            'api_key_present': True,
            'default_from': 'newsletter@resend.dev',
            'message': 'Resend is configured and ready to send emails'
        }


# Helper function for quick email sending
def send_newsletter_email(
    to_emails: List[str],
    subject: str,
    content: str,
    from_email: str = "CreatorPulse <newsletter@resend.dev>"
) -> Dict:
    """
    Quick helper to send newsletter emails

    Args:
        to_emails: List of recipient emails
        subject: Email subject
        content: Newsletter content (Markdown)
        from_email: Sender email

    Returns:
        Send result dictionary
    """
    sender = NewsletterEmailSender()
    return sender.send_newsletter(to_emails, subject, content, from_email)
