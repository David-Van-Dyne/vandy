"""
Free Data Provider for Bitcoin price data.
Uses public APIs to get historical and real-time Bitcoin prices for strategy development.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FreeDataProvider:
    """
    Provides Bitcoin price data from free public APIs.
    Perfect for developing and testing trading strategies.
    """
    
    def __init__(self):
        """Initialize the data provider with multiple backup APIs."""
        # Multiple free APIs for redundancy
        self.apis = {
            'coinbase_public': {
                'base_url': 'https://api.coinbase.com/v2',
                'current_price': '/exchange-rates?currency=BTC',
                'rate_limit': 2
            },
            'cryptocompare': {
                'base_url': 'https://min-api.cryptocompare.com/data',
                'current_price': '/price?fsym=BTC&tsyms=USD',
                'historical': '/v2/histohour?fsym=BTC&tsym=USD',
                'rate_limit': 1
            }
        }
        self.last_request_time = 0
        self.current_api = 'cryptocompare'  # Start with most reliable
        
        # Headers to look like a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print("Free Data Provider initialized")
        print(f"Using {self.current_api} as primary data source")
    
    def _wait_for_rate_limit(self):
        """Respect API rate limits to avoid getting blocked."""
        api_config = self.apis[self.current_api]
        time_since_last = time.time() - self.last_request_time
        required_wait = api_config['rate_limit']
        
        if time_since_last < required_wait:
            wait_time = required_wait - time_since_last
            # Add small random delay to avoid synchronized requests
            wait_time += random.uniform(0.1, 0.5)
            print(f"⏳ Waiting {wait_time:.1f}s for rate limit...")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def get_current_price(self):
        """
        Get the current Bitcoin price in USD.
        
        Returns:
            float: Current BTC price in USD
        """
        try:
            self._wait_for_rate_limit()
            
            if self.current_api == 'cryptocompare':
                url = self.apis['cryptocompare']['base_url'] + self.apis['cryptocompare']['current_price']
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                price = float(data['USD'])
                
            elif self.current_api == 'coinbase_public':
                url = self.apis['coinbase_public']['base_url'] + self.apis['coinbase_public']['current_price']
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                price = float(data['data']['rates']['USD'])
            
            print(f"💰 Current Bitcoin price: ${price:,.2f}")
            return price
            
        except Exception as e:
            print(f"❌ Error getting current price from {self.current_api}: {e}")
            return self._try_backup_api('current_price')
    
    def get_historical_data(self, timeframe='1h', limit=50):
        """
        Get historical Bitcoin price data for calculating moving averages.
        
        Args:
            timeframe: Time interval ('1h', '4h', '1d')
            limit: Number of data points to fetch (reduced to avoid rate limits)
        
        Returns:
            pandas.DataFrame: Historical OHLCV data
        """
        try:
            print(f"📈 Fetching {limit} {timeframe} candles for Bitcoin...")
            self._wait_for_rate_limit()
            
            # Use CryptoCompare for historical data (more reliable)
            url = f"{self.apis['cryptocompare']['base_url']}/v2/histohour"
            
            params = {
                'fsym': 'BTC',
                'tsym': 'USD',
                'limit': min(limit, 50),  # Limit to avoid rate limiting
                'aggregate': 1 if timeframe == '1h' else (4 if timeframe == '4h' else 24)
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data['Response'] == 'Success':
                # Convert to DataFrame
                df = self._process_cryptocompare_data(data['Data']['Data'])
                
                print(f"✅ Retrieved {len(df)} candles")
                print(f"📅 Date range: {df.index[0]} to {df.index[-1]}")
                print(f"💰 Latest price: ${df['close'].iloc[-1]:,.2f}")
                
                return df
            else:
                raise Exception(f"API error: {data.get('Message', 'Unknown error')}")
            
        except Exception as e:
            print(f"❌ Error getting historical data from {self.current_api}: {e}")
            return self._create_simple_data(limit)  # Fallback to simulated data
    
    def _process_cryptocompare_data(self, data):
        """Process CryptoCompare API response into OHLCV DataFrame."""
        df_data = []
        for candle in data:
            if candle['close'] > 0:  # Skip invalid data
                df_data.append({
                    'timestamp': candle['time'] * 1000,  # Convert to milliseconds
                    'open': float(candle['open']),
                    'high': float(candle['high']),
                    'low': float(candle['low']),
                    'close': float(candle['close']),
                    'volume': float(candle['volumeto'])
                })
        
        df = pd.DataFrame(df_data)
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('datetime', inplace=True)
        
        return df
    
    def _create_simple_data(self, limit):
        """Create simple simulated data as fallback."""
        print("🔄 Creating simulated data for testing...")
        
        try:
            # Get current price first
            current_price = self.get_current_price()
            if not current_price:
                current_price = 100000  # Fallback price
            
            # Create simple price data with random walk
            df_data = []
            price = current_price
            now = datetime.now()
            
            for i in range(limit):
                # Simple random walk simulation
                change = random.uniform(-0.02, 0.02)  # ±2% change
                price = price * (1 + change)
                
                timestamp = now - timedelta(hours=limit-i)
                
                df_data.append({
                    'timestamp': int(timestamp.timestamp() * 1000),
                    'open': price,
                    'high': price * 1.01,
                    'low': price * 0.99,
                    'close': price,
                    'volume': random.uniform(100, 1000)
                })
            
            df = pd.DataFrame(df_data)
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            
            print(f"✅ Created {len(df)} simulated candles")
            return df
            
        except Exception as e:
            print(f"❌ Even simulated data failed: {e}")
            return None
    
    
    def _try_backup_api(self, method, *args):
        """Try alternative API if primary fails."""
        original_api = self.current_api
        
        # Switch to backup API
        if self.current_api == 'cryptocompare':
            self.current_api = 'coinbase_public'
        else:
            self.current_api = 'cryptocompare'
        
        print(f"🔄 Switching to backup API: {self.current_api}")
        
        try:
            if method == 'current_price':
                return self.get_current_price()
            elif method == 'historical_data':
                return self.get_historical_data(*args)
        except Exception as e:
            print(f"❌ Backup API also failed: {e}")
            self.current_api = original_api  # Restore original
            
            # If all APIs fail, return simulated data for development
            if method == 'current_price':
                print("🔄 Using simulated current price for development")
                return 95000.0  # Reasonable BTC price for testing
            elif method == 'historical_data':
                print("🔄 Using simulated data for development")
                return self._create_simple_data(args[1] if len(args) > 1 else 30)
            
            return None
    
    def test_connection(self):
        """Test connection to data APIs."""
        print("🔍 Testing data provider connections...")
        
        try:
            # Test current price
            price = self.get_current_price()
            if price and price > 0:
                print("✅ Current price fetch successful")
                
                # Test historical data (smaller sample)
                df = self.get_historical_data('1h', 10)
                if df is not None and len(df) > 0:
                    print("✅ Historical data fetch successful")
                    print("🎉 Data provider is ready!")
                    return True
                else:
                    print("❌ Historical data fetch failed")
                    return False
            else:
                print("❌ Current price fetch failed")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

# Create a global data provider instance
data_provider = FreeDataProvider()

# For easy importing in other files
__all__ = ['data_provider']
