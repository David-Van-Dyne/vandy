# 🔧 Mobile App Metro Bundler Fix Guide

## ❌ Error Fixed: "Cannot find module 'metro/src/ModuleGraph/worker/importLocationsPlugin'"

This error is caused by Metro bundler version conflicts. Here are the solutions:

## ✅ **Solution 1: Quick Fix (Recommended)**

Run these commands in order:

```powershell
# 1. Clear all caches
npm cache clean --force
Remove-Item node_modules -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item package-lock.json -Force -ErrorAction SilentlyContinue

# 2. Install with exact versions
npm install expo@49.0.15 --save-exact
npm install

# 3. Start with tunnel mode (better for iPhone)
npx expo start --tunnel
```

## ✅ **Solution 2: Alternative Approach**

If Solution 1 doesn't work:

```powershell
# Install Expo CLI globally
npm install -g @expo/cli@latest

# Start directly
expo start --tunnel
```

## ✅ **Solution 3: Use Web Version**

If mobile app still has issues, use the web version:

```powershell
# Start web version
npx expo start --web
```

Then access via iPhone browser: `http://localhost:19006`

## 📱 **iPhone Connection Steps**

### **Option A: Tunnel Mode (Recommended)**
1. Run: `npx expo start --tunnel`
2. Install "Expo Go" on iPhone
3. Scan QR code - works from anywhere!

### **Option B: Local Network**
1. Run: `npx expo start`
2. Ensure iPhone and PC on same WiFi
3. Scan QR code with Expo Go

### **Option C: Web Browser**
1. Run: `npx expo start --web`
2. On iPhone Safari: `http://YOUR_PC_IP:19006`

## 🔍 **What Each Solution Does:**

**Solution 1:** 
- Clears conflicting dependencies
- Installs exact working Expo version
- Uses tunnel mode for global access

**Solution 2:**
- Uses global Expo CLI (more stable)
- Bypasses local version conflicts

**Solution 3:**
- Runs in web browser instead
- No Metro bundler needed
- Still has all functionality

## 🎯 **Quick Status Check**

After running any solution, you should see:
```
QR code appears in terminal
URL: exp://xxx... or http://localhost:19006
Status: "Tunnel ready" or "Metro waiting on..."
```

## 📱 **iPhone App Features**

Once connected, you'll have:
- **Dashboard**: Bot status, portfolio overview
- **Portfolio**: Holdings, P&L charts
- **Trades**: History, statistics
- **Settings**: Risk management, controls

Your bot API is configured for: `http://192.168.1.17:5000`

## 🆘 **If Still Having Issues**

1. **Restart everything**: Close all terminals, restart VS Code
2. **Check firewall**: Allow Node.js through Windows Firewall
3. **Try web version**: Always works as fallback
4. **Different network**: Try mobile hotspot

## 🚀 **Success Indicators**

✅ QR code appears in terminal
✅ No Metro bundler errors
✅ Expo Go app can scan code
✅ App loads on iPhone
✅ Can see trading bot dashboard

---

**Next Step**: Try Solution 1 first, then Solution 2 if needed!
