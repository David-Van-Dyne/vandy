# 📧 Email Notification Setup Guide

## ✅ Email System Status: READY!
The import issues have been resolved! Your email notification system is now fully functional and ready for configuration.

## 🔧 Quick Setup (5 minutes)

### Step 1: Set up Gmail App Password
1. **Go to Gmail Settings**: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. **Enable 2-Factor Authentication** (if not already enabled)
3. **Generate App Password**:
   - Search for "App passwords" in settings
   - Select "Mail" and your device
   - Copy the 16-character password (example: `abcd efgh ijkl mnop`)

### Step 2: Update Your .env File
Open your `.env` file and replace these lines:
```
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=your.email@gmail.com
```

With your actual details:
```
SENDER_EMAIL=youractual@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=youractual@gmail.com
```

### Step 3: Test Email System
Run this command to test:
```bash
python test_email.py
```

## 📬 What You'll Get Email Alerts For

### 🚀 Bot Events
- ✅ Bot starts up
- 🛑 Bot shuts down
- ⚠️ Bot errors

### 📊 Trading Signals
- 📈 **BUY Signal Detected** - When SMA/RSI indicates buying opportunity
- 📉 **SELL Signal Detected** - When SMA/RSI indicates selling opportunity

### 💰 Position Management
- 🟢 **Position Opened** - When bot actually buys Bitcoin
- 🔴 **Position Closed** - When bot sells (profit/loss/stop-loss)
- 📊 **Profit/Loss Summary** - Performance details

### Example Email Subject Lines:
- `🤖 Bitcoin Bot: BUY Signal Detected!`
- `🤖 Bitcoin Bot: Position Opened - Bought 0.001 BTC`
- `🤖 Bitcoin Bot: Position Closed - Profit: $23.45`

## 🔧 Alternative Email Providers

### Outlook/Hotmail
```
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

### Yahoo Mail
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## 🧪 Testing Your Setup
1. **First Test**: `python test_email.py` - Tests email sending
2. **Integration Test**: `python trading_bot.py` - See startup email
3. **Full Test**: Let bot run - you'll get signal emails

## 🎯 Next Steps
Once email is working:
1. ✅ Email notifications are ready
2. 🔧 We can make your trading strategy more aggressive
3. 📊 Monitor your bot's performance via email alerts

---
**🔒 Security Note**: Never share your .env file - it contains your API keys and passwords!
