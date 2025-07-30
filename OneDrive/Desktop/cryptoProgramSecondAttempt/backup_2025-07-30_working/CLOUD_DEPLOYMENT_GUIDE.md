# Cloud Deployment Guide
## Deploy Your Trading Bot to the Cloud (No PC Required!)

This guide will help you deploy your trading bot to the cloud so you can control it from your iPhone without needing your PC running 24/7.

## ☁️ Cloud Platform Options

### Option 1: Heroku (Recommended - Free Tier Available)
- ✅ Easy setup with free tier
- ✅ Automatic scaling 
- ✅ Built-in monitoring
- ✅ Custom domains

### Option 2: Railway 
- ✅ Modern platform
- ✅ Simple deployment
- ✅ Good free tier
- ✅ Fast performance

### Option 3: DigitalOcean App Platform
- ✅ Reliable infrastructure
- ✅ Multiple regions
- ✅ Competitive pricing

---

## 🚀 Quick Deploy to Heroku

### Step 1: Prepare Your Files
All necessary files are already created:
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Lists all dependencies
- ✅ `cloud_trading_bot.py` - Cloud-optimized bot
- ✅ `mobile_api_server.py` - API server with cloud detection

### Step 2: Create Heroku Account
1. Go to [heroku.com](https://heroku.com)
2. Sign up for free account
3. Download Heroku CLI from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

### Step 3: Deploy to Heroku

Open PowerShell in your project folder and run:

```powershell
# Login to Heroku
heroku login

# Create new Heroku app (replace 'your-bot-name' with unique name)
heroku create your-trading-bot-app

# Set environment variables for your exchange API
heroku config:set EXCHANGE_API_KEY="your_actual_api_key"
heroku config:set EXCHANGE_SECRET="your_actual_secret" 
heroku config:set EXCHANGE_PASSPHRASE="your_passphrase_if_needed"

# Set other bot configurations
heroku config:set BOT_MODE="live"
heroku config:set MAX_PORTFOLIO_VALUE="1000"
heroku config:set RISK_LEVEL="medium"

# Push to Heroku (this deploys your bot)
git init
git add .
git commit -m "Initial bot deployment"
heroku git:remote -a your-trading-bot-app
git push heroku main

# Start the bot
heroku ps:scale web=1 worker=1
```

### Step 4: Get Your App URL
After deployment, your app will be available at:
`https://your-trading-bot-app.herokuapp.com`

### Step 5: Update Mobile App
Edit `mobile_app/src/services/BotAPI.js`:

```javascript
// Change this line:
this.baseURL = 'http://192.168.1.100:5000';

// To your Heroku URL:
this.baseURL = 'https://your-trading-bot-app.herokuapp.com';
```

---

## 🚂 Alternative: Deploy to Railway

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub account

### Step 2: Deploy via Web Interface
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your repository
4. Railway will auto-detect and deploy

### Step 3: Set Environment Variables
In Railway dashboard:
- `EXCHANGE_API_KEY` = your_actual_api_key
- `EXCHANGE_SECRET` = your_actual_secret
- `BOT_MODE` = live

Your app will be at: `https://your-app-name.up.railway.app`

---

## 📱 Configure Mobile App for Cloud

### Update BotAPI.js
In `mobile_app/src/services/BotAPI.js`, uncomment the appropriate line:

```javascript
// For Heroku:
this.baseURL = 'https://your-trading-bot-app.herokuapp.com';

// For Railway:
this.baseURL = 'https://your-app-name.up.railway.app';
```

### Test Mobile App
1. Start your mobile app: `cd mobile_app && npm start`
2. Open Expo Go app on iPhone
3. Scan QR code to test connection

---

## ⚙️ Environment Variables Guide

Set these on your cloud platform:

### Required API Keys:
```
EXCHANGE_API_KEY=your_exchange_api_key
EXCHANGE_SECRET=your_exchange_secret_key
EXCHANGE_PASSPHRASE=your_passphrase (if using Coinbase Pro)
```

### Bot Configuration:
```
BOT_MODE=live                    # or 'paper' for testing
MAX_PORTFOLIO_VALUE=1000         # Maximum USD to trade
RISK_LEVEL=medium               # low, medium, high
EMAIL_ALERTS=true               # Enable email notifications
PORTFOLIO_PROTECTION=true       # Enable safety features
MAX_DRAWDOWN=15                # Maximum loss percentage
```

### Optional Settings:
```
NOTIFICATION_EMAIL=your@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_app_password
```

---

## 🔒 Security Best Practices

### API Key Security:
- ✅ Always use environment variables, never hardcode keys
- ✅ Use read-only API keys when possible
- ✅ Enable IP restrictions on exchange API keys
- ✅ Monitor API usage regularly

### Bot Protection:
- ✅ Enable portfolio protection (built-in)
- ✅ Set reasonable maximum drawdown limits
- ✅ Start with small amounts for testing
- ✅ Monitor via mobile app regularly

---

## 📊 Monitoring Your Cloud Bot

### Heroku Monitoring:
```powershell
# View live logs
heroku logs --tail

# Check bot status
heroku ps

# Scale workers if needed
heroku ps:scale worker=1
```

### Via Mobile App:
- 📱 Real-time portfolio tracking
- 📱 Trade history and performance
- 📱 Start/stop bot controls
- 📱 Emergency stop functionality

---

## 🆘 Troubleshooting

### Common Issues:

**Bot not starting:**
```powershell
heroku logs --tail
```
Check for missing environment variables or API key issues.

**Mobile app can't connect:**
- Verify cloud URL in BotAPI.js
- Check if Heroku app is running: `heroku ps`
- Test API directly: visit `https://your-app.herokuapp.com/api/status`

**Trading not working:**
- Verify API keys are correct
- Check exchange account has sufficient balance
- Ensure API permissions include trading

### Getting Help:
- Check Heroku logs: `heroku logs --tail`
- Monitor via mobile app dashboard
- Test with paper trading first (`BOT_MODE=paper`)

---

## 💰 Cost Estimates

### Heroku:
- **Free Tier**: 550 hours/month (enough for testing)
- **Basic**: $7/month (24/7 operation)
- **Standard**: $25/month (more memory, better performance)

### Railway:
- **Free Tier**: $5 credit monthly
- **Pro**: $20/month unlimited usage

### Recommendation:
Start with free tiers for testing, upgrade to paid plans for 24/7 live trading.

---

## ✅ Deployment Checklist

- [ ] Cloud platform account created
- [ ] Environment variables configured
- [ ] Bot deployed and running
- [ ] Mobile app URL updated
- [ ] Test trades working (use paper mode first)
- [ ] Portfolio protection enabled
- [ ] Email notifications configured (optional)
- [ ] Mobile app connected and functional

**🎉 Congratulations! Your bot is now running 24/7 in the cloud!**

You can now:
- Control your bot from anywhere via iPhone app
- Trade automatically without PC running
- Monitor performance in real-time
- Emergency stop from mobile if needed

---

## 🔄 Next Steps

1. **Test Everything**: Start with paper trading to verify setup
2. **Monitor Closely**: Watch first few live trades carefully  
3. **Optimize Settings**: Adjust risk parameters based on performance
4. **Scale Up**: Increase trading amounts as confidence grows

Your trading bot is now truly mobile and independent! 📱🤖💰
