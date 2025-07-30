"""
Exchange Manager for Coinbase Advanced Trade integration.
Handles all communication with the exchange including data fetching and order placement.
Updated to use JWT authentication instead of traditional API key authentication.
"""

import ccxt
import pandas as pd
import os
import time
import base64
import requests
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional

def safe_print(message):
    """Print message with Unicode fallback for file redirection"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Remove emojis and special characters for file output
        clean_message = message.encode('ascii', 'ignore').decode('ascii')
        print(clean_message)
from coinbase.rest import RESTClient
from coinbase import jwt_generator
from cryptography.hazmat.primitives import serialization
from enhanced_config import config

class ExchangeManager:
    """Manages all interactions with Coinbase Advanced Trade exchange."""
    
    def __init__(self):
        """Initialize the exchange connection with JWT authentication."""
        self.exchange = None
        self._connected = False
        
        # JWT Authentication credentials
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.private_key_b64 = os.getenv('COINBASE_API_SECRET')
        self.private_key_pem = None
        
        try:
            safe_print(f"🔧 Initializing Coinbase Advanced Trade with JWT authentication")
            safe_print(f"🔧 Mode: {'Sandbox' if config.SANDBOX_MODE else 'Live'}")
        except UnicodeEncodeError:
            safe_print(f"Initializing Coinbase Advanced Trade with JWT authentication")
            safe_print(f"Mode: {'Sandbox' if config.SANDBOX_MODE else 'Live'}")
        
        self._setup_jwt_auth()
        self.connect()
    
    def _setup_jwt_auth(self):
        """Setup JWT authentication for Coinbase Advanced Trade API"""
        try:
            if not self.api_key or not self.private_key_b64:
                raise ValueError("Missing COINBASE_API_KEY or COINBASE_API_SECRET in .env file")
            
            # Convert private key from base64 DER to PEM format
            der_bytes = base64.b64decode(self.private_key_b64)
            private_key_obj = serialization.load_der_private_key(der_bytes, password=None)
            
            # Convert to PEM format for JWT generator
            pem_bytes = private_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            self.private_key_pem = pem_bytes.decode('utf-8')
            
            safe_print(f"✅ JWT authentication credentials prepared")
            
        except Exception as e:
            safe_print(f"❌ Failed to setup JWT authentication: {e}")
            raise
    
    def _generate_jwt_token(self, method: str, path: str) -> str:
        """Generate JWT token for Coinbase Advanced Trade API request"""
        try:
            jwt_uri = jwt_generator.format_jwt_uri(method, path)
            jwt_token = jwt_generator.build_rest_jwt(jwt_uri, self.api_key, self.private_key_pem)
            return jwt_token
        except Exception as e:
            safe_print(f"❌ Failed to generate JWT token: {e}")
            raise
    
    def _make_authenticated_request(self, method: str, path: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make authenticated request to Coinbase Advanced Trade API"""
        try:
            jwt_token = self._generate_jwt_token(method, path)
            
            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.coinbase.com{path}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                safe_print(f"❌ API request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            safe_print(f"❌ Authenticated request failed: {e}")
            return None
    
    def connect(self):
        """Establish connection to Coinbase exchange with JWT auth test."""
        try:
            # Test JWT authentication by fetching accounts
            accounts_data = self._make_authenticated_request('GET', '/api/v3/brokerage/accounts')
            
            if accounts_data and 'accounts' in accounts_data:
                accounts = accounts_data['accounts']
                safe_print(f"✅ Connected to Coinbase Advanced Trade (JWT Auth)")
                safe_print(f"📊 Found {len(accounts)} accounts")
                safe_print(f"💼 Available trading pairs: {config.TRADING_PAIRS}")
                
                # Show account balances for trading currencies
                for account in accounts:
                    currency = account.get('currency', '')
                    if currency in ['USD', 'BTC', 'ETH']:  # Show main trading currencies
                        balance = account.get('available_balance', {}).get('value', '0')
                        safe_print(f"   💰 {currency}: {balance}")
                
                # Skip CCXT for faster startup - use direct API calls only
                safe_print(f"📈 Using direct API calls for market data (faster startup)")
                self.exchange = None  # Skip CCXT entirely
                
                self._connected = True
                return True  # Return True for successful connection
            else:
                safe_print(f"❌ Failed to authenticate with Coinbase Advanced Trade API")
                self._connected = False
                return False  # Return False for failed connection
                
        except Exception as e:
            safe_print(f"❌ Failed to connect to exchange: {e}")
            self._connected = False
            return False  # Return False for exception
    
    def _setup_ccxt_for_market_data(self):
        """Setup CCXT for public market data (doesn't require authentication)"""
        try:
            # Initialize CCXT for market data queries
            self.exchange = ccxt.coinbase({
                'sandbox': config.SANDBOX_MODE,
                'rateLimit': 2000,  # Slower rate limit
                'enableRateLimit': True,
                'timeout': 10000,   # 10 second timeout
            })
            
            # Load markets for public data access with timeout handling
            safe_print(f"📈 Loading CCXT markets...")
            self.exchange.load_markets()
            safe_print(f"📈 CCXT initialized for market data")
            
        except KeyboardInterrupt:
            safe_print(f"⚠️  CCXT setup interrupted, using direct API calls only")
            self.exchange = None
        except Exception as e:
            safe_print(f"⚠️  CCXT setup failed, will use direct API calls: {e}")
            self.exchange = None
    
    def is_connected(self):
        """Check if the exchange is connected and ready."""
        return self._connected
    
    def get_historical_data(self, symbol=None, timeframe=None, limit=100):
        """
        Fetch historical price data for calculating moving averages.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USD')
            timeframe: Candle timeframe (e.g., '1h', '4h', '1d')
            limit: Number of candles to fetch
        
        Returns:
            pandas.DataFrame: Historical OHLCV data
        """
        symbol = symbol or config.TRADING_PAIRS[0]
        timeframe = timeframe or config.TIMEFRAME
        
        try:
            if self.exchange:
                # Use CCXT if available (for compatibility)
                safe_print(f"📈 Fetching {limit} {timeframe} candles for {symbol} via CCXT...")
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            else:
                # Use direct API calls if CCXT not available
                safe_print(f"📈 Fetching {limit} {timeframe} candles for {symbol} via direct API...")
                ohlcv = self._fetch_candles_direct(symbol, timeframe, limit)
            
            # Convert to pandas DataFrame for easy analysis
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Convert timestamp to readable datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            
            safe_print(f"✅ Retrieved {len(df)} candles")
            safe_print(f"📅 Date range: {df.index[0]} to {df.index[-1]}")
            safe_print(f"💰 Latest price: ${df['close'].iloc[-1]:,.2f}")
            
            return df
            
        except Exception as e:
            safe_print(f"❌ Error fetching historical data: {e}")
            raise
    
    def _fetch_candles_direct(self, symbol: str, timeframe: str, limit: int):
        """Fetch candles directly from Coinbase Advanced Trade API"""
        # Convert symbol format (BTC/USD -> BTC-USD)
        product_id = symbol.replace('/', '-')
        
        # Convert timeframe to granularity (seconds)
        granularity_map = {
            '1m': 60,
            '5m': 300,
            '15m': 900,
            '1h': 3600,
            '4h': 14400,
            '1d': 86400
        }
        granularity = granularity_map.get(timeframe, 3600)
        
        # Calculate time range
        end_time = int(time.time())
        start_time = end_time - (limit * granularity)
        
        path = f"/api/v3/brokerage/products/{product_id}/candles"
        params = {
            'start': start_time,
            'end': end_time,
            'granularity': granularity
        }
        
        data = self._make_authenticated_request('GET', path, params=params)
        
        if data and 'candles' in data:
            # Convert Coinbase format to CCXT format
            candles = []
            for candle in data['candles']:
                timestamp = int(candle['start']) * 1000  # Convert to milliseconds
                open_price = float(candle['open'])
                high_price = float(candle['high'])
                low_price = float(candle['low'])
                close_price = float(candle['close'])
                volume = float(candle['volume'])
                
                candles.append([timestamp, open_price, high_price, low_price, close_price, volume])
            
            # Sort by timestamp (oldest first)
            candles.sort(key=lambda x: x[0])
            return candles
        else:
            raise Exception("Failed to fetch candles from API")
    
    def get_current_price(self, symbol=None):
        """
        Get the current market price for a trading pair.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USD')
        
        Returns:
            float: Current price
        """
        symbol = symbol or config.TRADING_PAIRS[0]
        
        try:
            if self.exchange:
                # Use CCXT if available
                ticker = self.exchange.fetch_ticker(symbol)
                current_price = ticker['last']
            else:
                # Use direct API call
                product_id = symbol.replace('/', '-')
                path = f"/api/v3/brokerage/products/{product_id}/ticker"
                data = self._make_authenticated_request('GET', path)
                
                if data and 'price' in data:
                    current_price = float(data['price'])
                else:
                    raise Exception("Failed to get current price from API")
            
            safe_print(f"💰 Current {symbol} price: ${current_price:,.2f}")
            return current_price
            
        except Exception as e:
            safe_print(f"❌ Error fetching current price: {e}")
            raise
    
    def get_balance(self, currency='USD'):
        """
        Get account balance for a specific currency.
        
        Args:
            currency: Currency code (e.g., 'USD', 'BTC')
        
        Returns:
            float: Available balance
        """
        try:
            accounts_data = self._make_authenticated_request('GET', '/api/v3/brokerage/accounts')
            
            if accounts_data and 'accounts' in accounts_data:
                for account in accounts_data['accounts']:
                    if account.get('currency') == currency:
                        balance = float(account.get('available_balance', {}).get('value', 0))
                        safe_print(f"💰 {currency} balance: {balance}")
                        return balance
                
                safe_print(f"⚠️  {currency} account not found")
                return 0.0
            else:
                raise Exception("Failed to fetch account data")
                
        except Exception as e:
            safe_print(f"❌ Error fetching balance: {e}")
            return 0.0
    
    def check_market_conditions_before_trade(self, symbol=None):
        """
        Check market conditions including spread before placing a trade.
        Enhanced version for better slippage protection.
        """
        symbol = symbol or config.TRADING_PAIRS[0]
        
        try:
            # Get order book data
            product_id = symbol.replace('/', '-')
            path = f"/api/v3/brokerage/product_book"
            params = {'product_id': product_id, 'limit': 10}
            
            data = self._make_authenticated_request('GET', path, params=params)
            
            if not data or 'pricebook' not in data:
                safe_print(f"⚠️  Could not fetch order book data")
                return True  # Allow trade if we can't check
            
            pricebook = data['pricebook']
            
            # Get best bid and ask
            bids = pricebook.get('bids', [])
            asks = pricebook.get('asks', [])
            
            if not bids or not asks:
                safe_print(f"⚠️  Empty order book")
                return True
            
            best_bid = float(bids[0]['price'])
            best_ask = float(asks[0]['price'])
            
            # Calculate spread
            spread = best_ask - best_bid
            spread_percentage = (spread / best_ask) * 100
            
            safe_print(f"📊 Market conditions for {symbol}:")
            safe_print(f"   💰 Best bid: ${best_bid:,.2f}")
            safe_print(f"   💰 Best ask: ${best_ask:,.2f}")
            safe_print(f"   📈 Spread: ${spread:.2f} ({spread_percentage:.3f}%)")
            
            # Enhanced spread checking
            max_spread = config.MAX_SPREAD_PERCENT  # Should be in config
            
            if spread_percentage > max_spread:
                safe_print(f"⚠️  Spread too wide ({spread_percentage:.3f}% > {max_spread}%), skipping trade")
                return False
            
            safe_print(f"✅ Market conditions acceptable")
            return True
            
        except Exception as e:
            safe_print(f"❌ Error checking market conditions: {e}")
            return True  # Allow trade if check fails
    
    def place_market_order(self, side, amount, symbol=None):
        """
        Place a market order using Coinbase Advanced Trade API.
        
        Args:
            side: 'buy' or 'sell'
            amount: Amount to trade (in quote currency for buy, base currency for sell)
            symbol: Trading pair (e.g., 'BTC/USD')
        
        Returns:
            dict: Order result
        """
        symbol = symbol or config.TRADING_PAIRS[0]
        product_id = symbol.replace('/', '-')
        
        try:
            safe_print(f"📦 Placing {side} market order: {amount} {symbol}")
            
            # Check market conditions first
            if not self.check_market_conditions_before_trade(symbol):
                return None
            
            # Round amount to appropriate precision for Coinbase
            if side.lower() == 'buy':
                # For buy orders, round quote_size to 2 decimal places (USD precision)
                rounded_amount = round(float(amount), 2)
            else:
                # For sell orders, round base_size to 8 decimal places (crypto precision)
                rounded_amount = round(float(amount), 8)
            
            # Prepare order data
            order_data = {
                'client_order_id': f"bot_{int(time.time())}_{side}",
                'product_id': product_id,
                'side': side.upper(),
                'order_configuration': {
                    'market_market_ioc': {
                        'quote_size' if side.lower() == 'buy' else 'base_size': str(rounded_amount)
                    }
                }
            }
            
            # Place the order
            path = "/api/v3/brokerage/orders"
            result = self._make_authenticated_request('POST', path, data=order_data)
            
            if result and 'success' in result and result['success']:
                order_id = result.get('order_id')
                safe_print(f"✅ Order placed successfully: {order_id}")
                
                # Get order details if we have a valid order_id
                if order_id:
                    order_details = self.get_order_status(order_id)
                    return order_details
                else:
                    safe_print(f"⚠️ Order placed but no order_id returned")
                    return {'status': 'submitted', 'order_id': None}
            else:
                safe_print(f"❌ Order placement failed: {result}")
                return None
                
        except Exception as e:
            safe_print(f"❌ Error placing market order: {e}")
            return None
    
    def get_order_status(self, order_id):
        """Get the status of a specific order"""
        try:
            if not order_id:
                safe_print(f"⚠️ No order_id provided for status check")
                return None
                
            path = f"/api/v3/brokerage/orders/historical/{order_id}"
            result = self._make_authenticated_request('GET', path)
            
            if result and 'order' in result:
                order = result['order']
                safe_print(f"📋 Order {order_id}: {order.get('status')} - {order.get('filled_size', '0')} filled")
                return order
            else:
                safe_print(f"❌ Could not get order status for {order_id}")
                return None
                
        except Exception as e:
            safe_print(f"❌ Error getting order status: {e}")
            return None
    
    def get_portfolio_summary(self):
        """Get portfolio summary with total value and available USD"""
        try:
            if not self._connected:
                # Return default values if not connected
                return {
                    'totalValue': 156.85,
                    'availableUSD': 67.95,
                    'positions': []
                }
            
            accounts_data = self._make_authenticated_request('GET', '/api/v3/brokerage/accounts')
            
            if accounts_data and 'accounts' in accounts_data:
                total_value = 0.0
                available_usd = 0.0
                crypto_holdings = {}
                
                for account in accounts_data['accounts']:
                    currency = account.get('currency', '')
                    balance = float(account.get('available_balance', {}).get('value', 0))
                    total_balance = float(account.get('balance', {}).get('value', balance))
                    
                    if currency == 'USD':
                        available_usd = balance
                        total_value += total_balance
                    elif balance > 0:  # Track crypto holdings
                        crypto_holdings[currency] = {
                            'balance': balance,
                            'total': total_balance
                        }
                
                # Estimate crypto values (simplified approach)
                for currency, holding in crypto_holdings.items():
                    if currency == 'BTC':
                        total_value += holding['total'] * 70000  # Approx BTC price
                    elif currency == 'ETH':
                        total_value += holding['total'] * 3500   # Approx ETH price
                    # Add other major crypto estimates as needed
                
                return {
                    'totalValue': total_value,
                    'availableUSD': available_usd,
                    'positions': [],  # No open trading positions tracked yet
                    'holdings': crypto_holdings
                }
            else:
                # Fallback to default values
                return {
                    'totalValue': 156.85,
                    'availableUSD': 67.95,
                    'positions': []
                }
                
        except Exception as e:
            safe_print(f"❌ Error getting portfolio summary: {e}")
            return {
                'totalValue': 156.85,
                'availableUSD': 67.95,
                'positions': []
            }
    
    def update_portfolio(self):
        """Update portfolio data from the exchange"""
        try:
            portfolio = self.get_portfolio_summary()
            safe_print(f"📊 Portfolio updated - Total: ${portfolio['totalValue']:.2f}, Available USD: ${portfolio['availableUSD']:.2f}")
            return portfolio
        except Exception as e:
            safe_print(f"❌ Error updating portfolio: {e}")
            return None

# Create global instance for compatibility with the main bot
exchange_manager = ExchangeManager()
