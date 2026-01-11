"""
Alert Manager
Handles multi-channel alerts for newly discovered businesses
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime
from src.core.config_manager import config
from src.core.logger import get_logger

logger = get_logger(__name__)


class AlertManager:
    """Manage alerts across multiple channels"""
    
    def __init__(self):
        self.email_enabled = config.get('alerts.enable_email', False)
        self.telegram_enabled = config.get('alerts.enable_telegram', False)
        self.desktop_enabled = config.get('alerts.enable_desktop', False)
        
        logger.info(f"Alert Manager initialized - Email: {self.email_enabled}, "
                   f"Telegram: {self.telegram_enabled}, Desktop: {self.desktop_enabled}")
    
    def send_alert(self, business: Dict[str, Any]):
        """Send alert through all enabled channels"""
        try:
            if self.email_enabled:
                self.send_email_alert(business)
            
            if self.telegram_enabled:
                self.send_telegram_alert(business)
            
            if self.desktop_enabled:
                self.send_desktop_alert(business)
            
            logger.info(f"Alert sent for: {business.get('business_name')}")
            
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
    
    def send_batch_alert(self, businesses: List[Dict[str, Any]]):
        """Send batch alert with multiple businesses"""
        if not businesses:
            return
        
        try:
            if self.email_enabled:
                self.send_batch_email(businesses)
            
            if self.telegram_enabled:
                self.send_batch_telegram(businesses)
            
            logger.info(f"Batch alert sent for {len(businesses)} businesses")
            
        except Exception as e:
            logger.error(f"Error sending batch alert: {str(e)}")
    
    def send_email_alert(self, business: Dict[str, Any]):
        """Send email alert for a single business"""
        try:
            smtp_server = config.get('api_keys.email.smtp_server')
            smtp_port = config.get('api_keys.email.smtp_port')
            sender_email = config.get('api_keys.email.sender_email')
            sender_password = config.get('api_keys.email.sender_password')
            recipient_email = config.get('api_keys.email.recipient_email')
            
            if not all([smtp_server, sender_email, sender_password, recipient_email]):
                logger.warning("Email configuration incomplete")
                return
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 New {business['priority'].upper()} Priority Lead: {business['business_name']}"
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = self._create_email_html(business)
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            logger.info(f"Email alert sent for: {business['business_name']}")
            
        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")
    
    def send_batch_email(self, businesses: List[Dict[str, Any]]):
        """Send batch email with multiple businesses"""
        try:
            smtp_server = config.get('api_keys.email.smtp_server')
            smtp_port = config.get('api_keys.email.smtp_port')
            sender_email = config.get('api_keys.email.sender_email')
            sender_password = config.get('api_keys.email.sender_password')
            recipient_email = config.get('api_keys.email.recipient_email')
            
            if not all([smtp_server, sender_email, sender_password, recipient_email]):
                return
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Daily Lead Report: {len(businesses)} New Businesses Discovered"
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = self._create_batch_email_html(businesses)
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            logger.info(f"Batch email sent for {len(businesses)} businesses")
            
        except Exception as e:
            logger.error(f"Error sending batch email: {str(e)}")
    
    def send_telegram_alert(self, business: Dict[str, Any]):
        """Send Telegram alert for a single business"""
        try:
            bot_token = config.get('api_keys.telegram.bot_token')
            chat_id = config.get('api_keys.telegram.chat_id')
            
            if not bot_token or not chat_id:
                logger.warning("Telegram configuration incomplete")
                return
            
            # Create message
            message = self._create_telegram_message(business)
            
            # Send via Telegram Bot API
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Telegram alert sent for: {business['business_name']}")
            
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {str(e)}")
    
    def send_batch_telegram(self, businesses: List[Dict[str, Any]]):
        """Send batch Telegram message"""
        try:
            bot_token = config.get('api_keys.telegram.bot_token')
            chat_id = config.get('api_keys.telegram.chat_id')
            
            if not bot_token or not chat_id:
                return
            
            # Create summary message
            message = f"📊 <b>Daily Lead Report</b>\n\n"
            message += f"🎯 {len(businesses)} new businesses discovered\n\n"
            
            # Group by priority
            high_priority = [b for b in businesses if b.get('priority') == 'high']
            medium_priority = [b for b in businesses if b.get('priority') == 'medium']
            
            if high_priority:
                message += f"🔴 <b>High Priority:</b> {len(high_priority)}\n"
            if medium_priority:
                message += f"🟡 <b>Medium Priority:</b> {len(medium_priority)}\n"
            
            message += f"\n📱 Check dashboard for details"
            
            # Send message
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
        except Exception as e:
            logger.error(f"Error sending batch Telegram: {str(e)}")

    def send_desktop_alert(self, business: Dict[str, Any]):
        """Send desktop notification (Windows/Mac/Linux)"""
        try:
            # Try to use plyer for cross-platform notifications
            try:
                from plyer import notification

                title = f"🚨 New {business['priority'].upper()} Priority Lead"
                message = f"{business['business_name']}\n{business['platform']} - {business['category']}"

                notification.notify(
                    title=title,
                    message=message,
                    app_name='Business Discovery System',
                    timeout=10
                )

                logger.info(f"Desktop notification sent for: {business['business_name']}")

            except ImportError:
                logger.warning("plyer not installed - desktop notifications disabled")

        except Exception as e:
            logger.error(f"Error sending desktop notification: {str(e)}")

    def _create_email_html(self, business: Dict[str, Any]) -> str:
        """Create HTML email content for a single business"""
        priority_color = {
            'high': '#dc3545',
            'medium': '#ffc107',
            'low': '#28a745'
        }.get(business.get('priority', 'medium'), '#6c757d')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: {priority_color}; color: white; padding: 20px; border-radius: 5px; }}
                .content {{ background: #f8f9fa; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ color: #333; }}
                .button {{ background: #007bff; color: white; padding: 10px 20px;
                          text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🚨 New Business Discovered!</h2>
                    <p>Priority: {business.get('priority', 'medium').upper()}</p>
                </div>
                <div class="content">
                    <div class="field">
                        <span class="label">Business Name:</span>
                        <span class="value">{business.get('business_name', 'N/A')}</span>
                    </div>
                    <div class="field">
                        <span class="label">Platform:</span>
                        <span class="value">{business.get('platform', 'N/A')}</span>
                    </div>
                    <div class="field">
                        <span class="label">Category:</span>
                        <span class="value">{business.get('category', 'N/A')}</span>
                    </div>
                    <div class="field">
                        <span class="label">Location:</span>
                        <span class="value">{business.get('location', 'N/A')}</span>
                    </div>
                    <div class="field">
                        <span class="label">Confidence Score:</span>
                        <span class="value">{business.get('confidence_score', 0)}/100</span>
                    </div>
                    <div class="field">
                        <span class="label">Description:</span>
                        <p class="value">{business.get('description', 'N/A')}</p>
                    </div>
                    <a href="{business.get('page_url', '#')}" class="button">View Page</a>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def _create_batch_email_html(self, businesses: List[Dict[str, Any]]) -> str:
        """Create HTML email content for batch report"""
        # Group by priority
        high = [b for b in businesses if b.get('priority') == 'high']
        medium = [b for b in businesses if b.get('priority') == 'medium']
        low = [b for b in businesses if b.get('priority') == 'low']

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #007bff; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ background: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .business-card {{ background: white; padding: 15px; margin: 10px 0;
                                border-left: 4px solid #007bff; border-radius: 3px; }}
                .high {{ border-left-color: #dc3545; }}
                .medium {{ border-left-color: #ffc107; }}
                .low {{ border-left-color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📊 Daily Lead Report</h2>
                    <p>{datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                <div class="summary">
                    <h3>Summary</h3>
                    <p>Total Businesses: {len(businesses)}</p>
                    <p>🔴 High Priority: {len(high)} | 🟡 Medium Priority: {len(medium)} | 🟢 Low Priority: {len(low)}</p>
                </div>
        """

        # Add high priority businesses
        if high:
            html += "<h3>🔴 High Priority Leads</h3>"
            for b in high[:10]:  # Limit to 10
                html += self._create_business_card_html(b, 'high')

        # Add medium priority businesses
        if medium:
            html += "<h3>🟡 Medium Priority Leads</h3>"
            for b in medium[:10]:
                html += self._create_business_card_html(b, 'medium')

        html += """
            </div>
        </body>
        </html>
        """
        return html

    def _create_business_card_html(self, business: Dict[str, Any], priority: str) -> str:
        """Create HTML for a single business card"""
        return f"""
        <div class="business-card {priority}">
            <h4>{business.get('business_name', 'N/A')}</h4>
            <p><strong>Platform:</strong> {business.get('platform', 'N/A')} |
               <strong>Category:</strong> {business.get('category', 'N/A')}</p>
            <p><strong>Location:</strong> {business.get('location', 'N/A')}</p>
            <p><strong>Score:</strong> {business.get('confidence_score', 0)}/100</p>
            <p><a href="{business.get('page_url', '#')}">View Page</a></p>
        </div>
        """

    def _create_telegram_message(self, business: Dict[str, Any]) -> str:
        """Create Telegram message for a single business"""
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(business.get('priority', 'medium'), '⚪')

        message = f"{priority_emoji} <b>New Business Discovered!</b>\n\n"
        message += f"<b>Name:</b> {business.get('business_name', 'N/A')}\n"
        message += f"<b>Platform:</b> {business.get('platform', 'N/A')}\n"
        message += f"<b>Category:</b> {business.get('category', 'N/A')}\n"
        message += f"<b>Location:</b> {business.get('location', 'N/A')}\n"
        message += f"<b>Score:</b> {business.get('confidence_score', 0)}/100\n\n"

        if business.get('description'):
            desc = business['description'][:150]
            message += f"<i>{desc}...</i>\n\n"

        message += f"<a href='{business.get('page_url', '#')}'>View Page</a>"

        return message

