# 📱 iPhone Access Setup Guide
## How to Access Your Trading Bot from iPhone

### 🚀 **Overview**
Your trading bot will have two ways to access it from your iPhone:

1. **📱 Native Mobile App** (React Native - Recommended)
2. **🌐 Web Browser** (Simple alternative)

---

## 📱 **Option 1: Native Mobile App (Recommended)**

### **Prerequisites:**
1. **iPhone with iOS 13+**
2. **Expo Go app** (free from App Store)
3. **PC/Mac for development** (this computer)

### **Step 1: Install Expo Go on iPhone**
1. Open **App Store** on your iPhone
2. Search for **"Expo Go"**
3. Install the free Expo Go app
4. Keep your iPhone and PC on the **same WiFi network**

### **Step 2: Configure Mobile App for Your Setup**

Your mobile app is already created! It just needs to know where to connect:

#### **For Local PC Testing (Before Heroku):**
Your BotAPI.js currently points to Heroku, but for local testing, we need your PC's IP:

```javascript
// Current setting (in BotAPI.js line 19):
this.baseURL = 'https://your-app-name.herokuapp.com';

// For local testing, change to:
this.baseURL = 'http://YOUR_PC_IP:5000';
```

#### **For Heroku Cloud (After Deployment):**
```javascript
// After Heroku deployment:
this.baseURL = 'https://your-actual-heroku-app-name.herokuapp.com';
```

### **Step 3: Find Your PC's IP Address**
Run this command to find your PC's IP:
```powershell
ipconfig | findstr IPv4
```

### **Step 4: Start Mobile App Development Server**
```powershell
cd mobile_app
npm start
```

### **Step 5: Connect iPhone**
1. A QR code will appear in your terminal
2. Open **Expo Go** on your iPhone
3. Tap **"Scan QR Code"**
4. Point camera at the QR code
5. Your trading bot app will load on iPhone! 🎉

---

## 🌐 **Option 2: Web Browser Access**

### **Simple Web Interface** (Alternative if mobile app has issues)

Your mobile API server also serves a basic web interface:

#### **For Local PC:**
1. Start your bot: `python mobile_api_server.py`
2. On iPhone Safari: `http://YOUR_PC_IP:5000`

#### **For Heroku Cloud:**
1. Deploy to Heroku
2. On iPhone Safari: `https://your-app-name.herokuapp.com`

---

## 🔧 **Quick Setup Commands**

Let me help you get started right now:

### **Find Your PC IP:**
```powershell
ipconfig | findstr IPv4
```

### **Update Mobile App for Local Testing:**
We need to update your BotAPI.js with your actual PC IP address.

### **Start Local API Server:**
```powershell
python mobile_api_server.py
```

### **Start Mobile App:**
```powershell
cd mobile_app
npm start
```

---

## 📊 **What You'll See on iPhone**

Your mobile app has 4 main screens:

### **1. 📊 Dashboard**
- Bot status (running/stopped)
- Portfolio overview
- Quick start/stop controls
- Recent trading activity

### **2. 💰 Portfolio**
- Total portfolio value
- Individual coin holdings
- Profit/loss tracking
- Performance charts

### **3. 📈 Trades**
- Recent trade history
- Win/loss statistics
- Trade performance metrics

### **4. ⚙️ Settings**
- Bot configuration
- Risk management settings
- Emergency stop controls
- Notifications preferences

---

## 🛠️ **Troubleshooting**

### **Can't Connect to Bot:**
1. Ensure PC and iPhone on same WiFi
2. Check Windows Firewall (allow port 5000)
3. Verify bot is running: `python mobile_api_server.py`

### **Expo Go Issues:**
1. Restart Expo Go app
2. Clear Expo cache: `npm start --clear`
3. Try different WiFi network

### **API Connection Errors:**
1. Check your PC's IP address hasn't changed
2. Restart mobile API server
3. Check bot logs for errors

---

## 🚀 **Next Steps**

1. **Test Locally First:**
   - Get mobile app working with your PC
   - Test all features before cloud deployment
   - Verify emergency stop works

2. **Deploy to Heroku:**
   - Use the `deploy_to_cloud.ps1` script
   - Update mobile app with Heroku URL
   - Test cloud connection

3. **Go Live:**
   - Start with paper trading
   - Monitor closely for first 24 hours
   - Gradually increase trading amounts

---

Would you like me to help you find your PC's IP address and update the mobile app configuration right now?
