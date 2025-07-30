# CRYPTO TRADING BOT MOBILE APP SETUP

## Prerequisites
1. Install Node.js (https://nodejs.org/)
2. Install Expo CLI: `npm install -g @expo/cli`
3. Install the Expo Go app on your iPhone from the App Store

## Setup Instructions

### 1. Install Dependencies
```bash
cd mobile_app
npm install
```

### 2. Configure API Connection
1. Find your PC's IP address:
   - Windows: Open Command Prompt and run `ipconfig`
   - Look for "IPv4 Address" under your network adapter
   - Example: 192.168.1.100

2. Update the API connection:
   - Open `src/services/BotAPI.js`
   - Replace `192.168.1.100` with your actual PC's IP address
   - Example: `this.baseURL = 'http://192.168.1.105:5000';`

### 3. Start the API Server on Your PC
```bash
# In your main bot directory
pip install flask flask-cors
python mobile_api_server.py
```

### 4. Start the Mobile App
```bash
cd mobile_app
npm start
```

### 5. Connect Your iPhone
1. Make sure your iPhone and PC are on the same WiFi network
2. Open Expo Go app on your iPhone
3. Scan the QR code shown in your terminal/browser
4. The app will load on your phone!

## App Features

📱 **Dashboard Screen**
- Real-time bot status
- Portfolio overview
- Top profit opportunities
- Bot control buttons (Start/Stop/Emergency Stop)

📊 **Portfolio Screen**
- Total portfolio value and P&L
- Performance chart
- Active positions with profit/loss
- Portfolio protection status

📈 **Trades Screen**
- Trading statistics and win rate
- Recent trade history
- Open orders
- Today's trading summary

⚙️ **Settings Screen**
- Trading controls (Enable/Disable)
- Risk management settings
- Notification preferences
- Bot information and status

## Building for iPhone (Optional)

### Option 1: Development Build (Recommended)
```bash
# Install EAS CLI
npm install -g eas-cli

# Configure your build
eas build:configure

# Build for iOS
eas build --platform ios
```

### Option 2: App Store Distribution
1. You'll need an Apple Developer account ($99/year)
2. Configure app signing in EAS
3. Build and submit to App Store

## Troubleshooting

**App won't connect to bot:**
- Verify your PC's IP address is correct in BotAPI.js
- Make sure both devices are on same WiFi network
- Check that mobile_api_server.py is running
- Try accessing http://YOUR_PC_IP:5000/health in your phone's browser

**Expo app crashes:**
- Clear Expo cache: `expo start -c`
- Restart the Metro bundler
- Check for JavaScript errors in console

**Build errors:**
- Run `npm install` to ensure all dependencies are installed
- Update Expo SDK: `expo install --fix`

## Next Steps

1. **Test the connection** - Make sure the app can connect to your PC
2. **Customize the UI** - Modify colors, layouts, add features
3. **Add push notifications** - Get alerts when trades execute
4. **Deploy to cloud** - Move your bot to a VPS for 24/7 operation

## Notes

- The app includes mock data so it works even when disconnected
- Your bot will continue running on your PC independently
- The mobile app is just a remote control interface
- All trading still happens through your existing bot code

Enjoy your mobile trading bot controller! 🚀📱
