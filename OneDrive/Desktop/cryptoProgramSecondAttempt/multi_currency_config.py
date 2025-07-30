"""
Multi-Currency Configuration Manager
Extended configuration for managing multiple cryptocurrency trading pairs
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MultiCurrencyConfig:
    """Configuration class for multi-currency trading bot"""
    
    def __init__(self):
        """Initialize multi-currency configuration"""
        self._load_base_config()
        self._load_currency_configs()
        self._load_risk_management()
        self._validate_config()
    
    def _load_base_config(self):
        """Load base exchange and API configuration"""
        self.COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
        self.COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')
        self.COINBASE_PASSPHRASE = os.getenv('COINBASE_PASSPHRASE')
        self.EXCHANGE = os.getenv('EXCHANGE', 'coinbase')
        self.SANDBOX_MODE = os.getenv('SANDBOX_MODE', 'True').lower() == 'true'
        self.ENABLE_TRADING = os.getenv('ENABLE_TRADING', 'False').lower() == 'true'
        
        # Global settings
        self.CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '1'))
        self.MIN_USD_RESERVE = float(os.getenv('MIN_USD_RESERVE', '50.0'))
    
    def _load_currency_configs(self):
        """Load individual currency trading configurations"""
        
        # Default configurations for supported currencies
        self.CURRENCY_CONFIGS = {
            'BTC/USD': {
                'enabled': os.getenv('BTC_ENABLED', 'True').lower() == 'true',
                'position_size_usd': float(os.getenv('BTC_POSITION_SIZE', '45.0')),
                'take_profit_percent': float(os.getenv('BTC_TAKE_PROFIT', '2.0')),
                'stop_loss_percent': float(os.getenv('BTC_STOP_LOSS', '0.5')),
                'timeframe': os.getenv('BTC_TIMEFRAME', '15m'),
                'min_balance': float(os.getenv('BTC_MIN_BALANCE', '0.00001')),
                'short_sma': int(os.getenv('BTC_SHORT_SMA', '3')),
                'long_sma': int(os.getenv('BTC_LONG_SMA', '8'))
            },
            'ETH/USD': {
                'enabled': os.getenv('ETH_ENABLED', 'True').lower() == 'true',
                'position_size_usd': float(os.getenv('ETH_POSITION_SIZE', '40.0')),
                'take_profit_percent': float(os.getenv('ETH_TAKE_PROFIT', '2.5')),
                'stop_loss_percent': float(os.getenv('ETH_STOP_LOSS', '0.7')),
                'timeframe': os.getenv('ETH_TIMEFRAME', '15m'),
                'min_balance': float(os.getenv('ETH_MIN_BALANCE', '0.001')),
                'short_sma': int(os.getenv('ETH_SHORT_SMA', '3')),
                'long_sma': int(os.getenv('ETH_LONG_SMA', '8'))
            },
            'SOL/USD': {
                'enabled': os.getenv('SOL_ENABLED', 'False').lower() == 'true',
                'position_size_usd': float(os.getenv('SOL_POSITION_SIZE', '35.0')),
                'take_profit_percent': float(os.getenv('SOL_TAKE_PROFIT', '3.0')),
                'stop_loss_percent': float(os.getenv('SOL_STOP_LOSS', '1.0')),
                'timeframe': os.getenv('SOL_TIMEFRAME', '15m'),
                'min_balance': float(os.getenv('SOL_MIN_BALANCE', '0.01')),
                'short_sma': int(os.getenv('SOL_SHORT_SMA', '3')),
                'long_sma': int(os.getenv('SOL_LONG_SMA', '8'))
            },
            'ADA/USD': {
                'enabled': os.getenv('ADA_ENABLED', 'False').lower() == 'true',
                'position_size_usd': float(os.getenv('ADA_POSITION_SIZE', '30.0')),
                'take_profit_percent': float(os.getenv('ADA_TAKE_PROFIT', '3.5')),
                'stop_loss_percent': float(os.getenv('ADA_STOP_LOSS', '1.2')),
                'timeframe': os.getenv('ADA_TIMEFRAME', '15m'),
                'min_balance': float(os.getenv('ADA_MIN_BALANCE', '1.0')),
                'short_sma': int(os.getenv('ADA_SHORT_SMA', '3')),
                'long_sma': int(os.getenv('ADA_LONG_SMA', '8'))
            },
            'DOT/USD': {
                'enabled': os.getenv('DOT_ENABLED', 'False').lower() == 'true',
                'position_size_usd': float(os.getenv('DOT_POSITION_SIZE', '25.0')),
                'take_profit_percent': float(os.getenv('DOT_TAKE_PROFIT', '4.0')),
                'stop_loss_percent': float(os.getenv('DOT_STOP_LOSS', '1.5')),
                'timeframe': os.getenv('DOT_TIMEFRAME', '15m'),
                'min_balance': float(os.getenv('DOT_MIN_BALANCE', '0.1')),
                'short_sma': int(os.getenv('DOT_SHORT_SMA', '3')),
                'long_sma': int(os.getenv('DOT_LONG_SMA', '8'))
            }
        }
    
    def _load_risk_management(self):
        """Load risk management settings"""
        self.MAX_TOTAL_POSITION_SIZE = float(os.getenv('MAX_TOTAL_POSITION_SIZE', '200.0'))
        self.MAX_CONCURRENT_POSITIONS = int(os.getenv('MAX_CONCURRENT_POSITIONS', '3'))
        self.EMERGENCY_STOP_LOSS_PERCENT = float(os.getenv('EMERGENCY_STOP_LOSS_PERCENT', '10.0'))
        
        # Portfolio allocation limits (as percentage of total USD)
        self.MAX_SINGLE_POSITION_PERCENT = float(os.getenv('MAX_SINGLE_POSITION_PERCENT', '30.0'))
        self.MAX_CRYPTO_ALLOCATION_PERCENT = float(os.getenv('MAX_CRYPTO_ALLOCATION_PERCENT', '80.0'))
    
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.COINBASE_API_KEY or not self.COINBASE_API_SECRET:
            raise ValueError("Missing Coinbase API credentials in .env file")
        
        # Validate that at least one currency is enabled
        enabled_currencies = [pair for pair, config in self.CURRENCY_CONFIGS.items() 
                            if config['enabled']]
        
        if not enabled_currencies:
            raise ValueError("No currencies enabled for trading")
        
        # Validate position sizes
        total_position_size = sum(config['position_size_usd'] 
                                for config in self.CURRENCY_CONFIGS.values() 
                                if config['enabled'])
        
        if total_position_size > self.MAX_TOTAL_POSITION_SIZE:
            print(f"⚠️ Warning: Total position size (${total_position_size}) exceeds maximum (${self.MAX_TOTAL_POSITION_SIZE})")
    
    def get_enabled_currencies(self) -> Dict[str, Dict[str, Any]]:
        """Get only the enabled currency configurations"""
        return {pair: config for pair, config in self.CURRENCY_CONFIGS.items() 
                if config['enabled']}
    
    def get_currency_config(self, pair: str) -> Dict[str, Any]:
        """Get configuration for a specific currency pair"""
        return self.CURRENCY_CONFIGS.get(pair, {})
    
    def print_config_summary(self):
        """Print a summary of the current configuration"""
        print("🔧 MULTI-CURRENCY BOT CONFIGURATION")
        print("=" * 50)
        print(f"📊 Mode: {'Sandbox' if self.SANDBOX_MODE else 'Live'}")
        print(f"💰 Min USD Reserve: ${self.MIN_USD_RESERVE}")
        print(f"🔄 Check Interval: {self.CHECK_INTERVAL_MINUTES} minute(s)")
        print(f"🛡️ Max Concurrent Positions: {self.MAX_CONCURRENT_POSITIONS}")
        print(f"💸 Max Total Position Size: ${self.MAX_TOTAL_POSITION_SIZE}")
        
        print(f"\n📈 ENABLED CURRENCIES:")
        enabled = self.get_enabled_currencies()
        for pair, config in enabled.items():
            print(f"   {pair}: ${config['position_size_usd']} | "
                  f"TP: {config['take_profit_percent']}% | "
                  f"SL: {config['stop_loss_percent']}%")
        
        if len(enabled) == 0:
            print("   ⚠️ No currencies enabled!")
        
        print("=" * 50)

# Create global config instance
multi_config = MultiCurrencyConfig()

# Backwards compatibility with existing single-currency config
class Config:
    """Backwards compatible config class"""
    def __init__(self):
        self.COINBASE_API_KEY = multi_config.COINBASE_API_KEY
        self.COINBASE_API_SECRET = multi_config.COINBASE_API_SECRET
        self.COINBASE_PASSPHRASE = multi_config.COINBASE_PASSPHRASE
        self.EXCHANGE = multi_config.EXCHANGE
        self.SANDBOX_MODE = multi_config.SANDBOX_MODE
        self.ENABLE_TRADING = multi_config.ENABLE_TRADING
        
        # Use BTC config for backwards compatibility
        btc_config = multi_config.get_currency_config('BTC/USD')
        self.TRADING_PAIR = 'BTC/USD'
        self.TRADE_AMOUNT = btc_config.get('position_size_usd', 45.0) / 100000  # Convert to BTC amount estimate
        self.CHECK_INTERVAL_MINUTES = multi_config.CHECK_INTERVAL_MINUTES
        self.SHORT_SMA_PERIOD = btc_config.get('short_sma', 3)
        self.LONG_SMA_PERIOD = btc_config.get('long_sma', 8)
        self.TIMEFRAME = btc_config.get('timeframe', '15m')
        self.MAX_OPEN_POSITIONS = 1
        self.MAX_POSITION_SIZE = btc_config.get('position_size_usd', 45.0)
        self.STOP_LOSS_PERCENT = btc_config.get('stop_loss_percent', 0.5)

# Create backwards compatible config instance
config = Config()
