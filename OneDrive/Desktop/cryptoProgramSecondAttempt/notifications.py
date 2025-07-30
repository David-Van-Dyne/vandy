"""
Email Notification System for Trading Bot
Sends email alerts when the bot makes trading decisions
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import config

class EmailNotifier:
    """Handles email notifications for trading events"""
    
    def __init__(self):
        """Initialize email notifier with configuration"""
        self.enabled = getattr(config, 'EMAIL_NOTIFICATIONS', False)
        self.smtp_server = getattr(config, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(config, 'SMTP_PORT', 587)
        self.sender_email = getattr(config, 'SENDER_EMAIL', '')
        self.sender_password = getattr(config, 'SENDER_PASSWORD', '')
        self.recipient_email = getattr(config, 'RECIPIENT_EMAIL', '')
        
        if self.enabled and not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("⚠️  Email notifications enabled but missing credentials")
            self.enabled = False
    
    def send_email(self, subject: str, body: str, is_html: bool = False):
        """Send an email notification"""
        if not self.enabled:
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"🤖 Bitcoin Bot: {subject}"
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            
            # Add body
            if is_html:
                part = MIMEText(body, "html")
            else:
                part = MIMEText(body, "plain")
            message.attach(part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            print(f"✅ Email sent: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def notify_trade_signal(self, signal: str, price: float, signal_data: dict):
        """Send notification for new trading signal"""
        if not self.enabled:
            return
        
        subject = f"{signal.upper()} Signal - ${price:,.2f}"
        
        body = f"""
🤖 BITCOIN TRADING BOT ALERT

📊 TRADING SIGNAL: {signal.upper()}
💰 Bitcoin Price: ${price:,.2f}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Technical Analysis:
   • SMA 10: ${signal_data.get('sma_10', 0):,.2f}
   • SMA 30: ${signal_data.get('sma_30', 0):,.2f}
   • RSI: {signal_data.get('rsi', 0):.1f}
   • Trend: {'UP' if signal_data.get('sma_10', 0) > signal_data.get('sma_30', 0) else 'DOWN'}

💡 Reason: {signal_data.get('reason', 'Technical analysis')}

{'🚀 POSITION WILL BE OPENED' if signal in ['BUY', 'STRONG_BUY'] else '🛑 STAYING OUT OF MARKET'}

Bot Status: {'Sandbox Mode' if config.SANDBOX_MODE else 'Live Trading'}
        """
        
        self.send_email(subject, body.strip())
    
    def notify_position_opened(self, signal: str, price: float, size: float, value: float):
        """Send notification when position is opened"""
        if not self.enabled:
            return
        
        subject = f"Position Opened - {signal} ${price:,.2f}"
        
        body = f"""
🚀 POSITION OPENED

📊 Trade Details:
   • Type: {signal.upper()}
   • Entry Price: ${price:,.2f}
   • Position Size: {size:.6f} BTC
   • Position Value: ${value:,.2f}
   • Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 Risk Management:
   • Stop Loss: {config.STOP_LOSS_PERCENT}% (${price * (1 - config.STOP_LOSS_PERCENT/100):,.2f})
   • Take Profit: {config.TAKE_PROFIT_PERCENT}% (${price * (1 + config.TAKE_PROFIT_PERCENT/100):,.2f})

Mode: {'Sandbox (Test)' if config.SANDBOX_MODE else 'Live Trading'}
        """
        
        self.send_email(subject, body.strip())
    
    def notify_position_closed(self, signal: str, entry_price: float, exit_price: float, 
                             size: float, pnl: float, reason: str):
        """Send notification when position is closed"""
        if not self.enabled:
            return
        
        pnl_percent = (pnl / (entry_price * size)) * 100
        emoji = "🎉" if pnl > 0 else "😞" if pnl < 0 else "😐"
        
        subject = f"Position Closed - {pnl_percent:+.1f}% PnL"
        
        body = f"""
{emoji} POSITION CLOSED

📊 Trade Summary:
   • Type: {signal.upper()}
   • Entry Price: ${entry_price:,.2f}
   • Exit Price: ${exit_price:,.2f}
   • Position Size: {size:.6f} BTC
   • Reason: {reason}
   • Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💰 Profit/Loss:
   • PnL Amount: ${pnl:+,.2f}
   • PnL Percentage: {pnl_percent:+.2f}%
   • Price Change: {((exit_price - entry_price) / entry_price) * 100:+.2f}%

Mode: {'Sandbox (Test)' if config.SANDBOX_MODE else 'Live Trading'}
        """
        
        self.send_email(subject, body.strip())
    
    def notify_bot_started(self):
        """Send notification when bot starts"""
        if not self.enabled:
            return
        
        subject = "Bot Started"
        
        body = f"""
🤖 BITCOIN TRADING BOT STARTED

⚙️ Configuration:
   • Mode: {'Sandbox (Safe Testing)' if config.SANDBOX_MODE else 'Live Trading'}
   • Max Position: ${config.MAX_POSITION_SIZE:,.2f}
   • Stop Loss: {config.STOP_LOSS_PERCENT}%
   • Take Profit: {config.TAKE_PROFIT_PERCENT}%
   • Strategy: SMA + RSI
   • Analysis Frequency: 5 minutes

🛡️ Safety:
   • Trading Enabled: {config.ENABLE_TRADING}
   • Exchange: {'Sandbox' if config.SANDBOX_MODE else 'Live'} Coinbase

Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.send_email(subject, body.strip())
    
    def notify_bot_stopped(self, runtime: str, total_trades: int, total_pnl: float):
        """Send notification when bot stops"""
        if not self.enabled:
            return
        
        subject = f"Bot Stopped - {total_trades} trades, ${total_pnl:+,.2f} PnL"
        
        body = f"""
🛑 BITCOIN TRADING BOT STOPPED

📊 Session Summary:
   • Runtime: {runtime}
   • Total Trades: {total_trades}
   • Total PnL: ${total_pnl:+,.2f}
   • Mode: {'Sandbox (Test)' if config.SANDBOX_MODE else 'Live Trading'}

Stopped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.send_email(subject, body.strip())
    
    def notify_error(self, error_message: str):
        """Send notification for critical errors"""
        if not self.enabled:
            return
        
        subject = "⚠️ Bot Error"
        
        body = f"""
⚠️ TRADING BOT ERROR

🚨 Error Details:
{error_message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Mode: {'Sandbox' if config.SANDBOX_MODE else 'Live Trading'}

Please check the bot status and logs.
        """
        
        self.send_email(subject, body.strip())
    
    def test_email(self):
        """Send a test email to verify configuration"""
        if not self.enabled:
            print("❌ Email notifications are disabled")
            return False
        
        subject = "Test Email"
        body = f"""
✅ EMAIL NOTIFICATION TEST

This is a test email from your Bitcoin trading bot.
If you receive this, email notifications are working correctly!

Configuration:
• SMTP Server: {self.smtp_server}:{self.smtp_port}
• From: {self.sender_email}
• To: {self.recipient_email}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return self.send_email(subject, body.strip())

# Create global instance
email_notifier = EmailNotifier()

# For easy importing
__all__ = ['email_notifier', 'EmailNotifier']
