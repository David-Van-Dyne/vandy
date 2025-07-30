#!/usr/bin/env python3
"""
Enhanced Configuration Management for Crypto Trading Bot
Loads settings from .env file and provides configuration to all modules
"""

import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class EnhancedConfig:
    """Enhanced configuration with multi-currency support"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        
        # =============================================================================
        # EXCHANGE CREDENTIALS
        # =============================================================================
        self.COINBASE_API_KEY = os.getenv('COINBASE_API_KEY', '')
        self.COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET', '')
        self.COINBASE_PASSPHRASE = os.getenv('COINBASE_PASSPHRASE', '')
        
        # =============================================================================
        # EXCHANGE SETTINGS
        # =============================================================================
        self.EXCHANGE = os.getenv('EXCHANGE', 'coinbase')
        self.SANDBOX_MODE = os.getenv('SANDBOX_MODE', 'False').lower() == 'true'
        self.ENABLE_TRADING = os.getenv('ENABLE_TRADING', 'True').lower() == 'true'
        
        # =============================================================================
        # TRADING PARAMETERS
        # =============================================================================
        self.CHECK_INTERVAL_MINUTES = float(os.getenv('CHECK_INTERVAL_MINUTES', '1'))
        self.MIN_USD_RESERVE = float(os.getenv('MIN_USD_RESERVE', '50.0'))
        self.TIMEFRAME = os.getenv('TIMEFRAME', '15m')  # Default timeframe for all pairs
        
        # =============================================================================
        # RISK MANAGEMENT
        # =============================================================================
        self.MAX_TOTAL_POSITION_SIZE = float(os.getenv('MAX_TOTAL_POSITION_SIZE', '200.0'))
        self.MAX_CONCURRENT_POSITIONS = int(os.getenv('MAX_CONCURRENT_POSITIONS', '3'))
        self.EMERGENCY_STOP_LOSS_PERCENT = float(os.getenv('EMERGENCY_STOP_LOSS_PERCENT', '10.0'))
        self.MAX_SINGLE_POSITION_PERCENT = float(os.getenv('MAX_SINGLE_POSITION_PERCENT', '30.0'))
        self.MAX_SPREAD_PERCENT = float(os.getenv('MAX_SPREAD_PERCENT', '0.5'))  # 0.5% max spread
        
        # =============================================================================
        # TRADING PAIRS CONFIGURATION
        # =============================================================================
        self.TRADING_PAIRS = ['BTC/USD', 'ETH/USD', 'DOGE/USD', 'AVAX/USD', 'BCH/USD']
        
        # Bitcoin settings
        self.BTC_ENABLED = os.getenv('BTC_ENABLED', 'True').lower() == 'true'
        self.BTC_POSITION_SIZE = float(os.getenv('BTC_POSITION_SIZE', '45.0'))
        self.BTC_TAKE_PROFIT = float(os.getenv('BTC_TAKE_PROFIT', '2.0'))
        self.BTC_STOP_LOSS = float(os.getenv('BTC_STOP_LOSS', '0.5'))
        self.BTC_TIMEFRAME = os.getenv('BTC_TIMEFRAME', '15m')
        
        # Ethereum settings
        self.ETH_ENABLED = os.getenv('ETH_ENABLED', 'True').lower() == 'true'
        self.ETH_POSITION_SIZE = float(os.getenv('ETH_POSITION_SIZE', '40.0'))
        self.ETH_TAKE_PROFIT = float(os.getenv('ETH_TAKE_PROFIT', '2.5'))
        self.ETH_STOP_LOSS = float(os.getenv('ETH_STOP_LOSS', '0.7'))
        self.ETH_TIMEFRAME = os.getenv('ETH_TIMEFRAME', '15m')
        
        # =============================================================================
        # NOTIFICATION SETTINGS
        # =============================================================================
        self.ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'False').lower() == 'true'
        self.ENABLE_TELEGRAM_NOTIFICATIONS = os.getenv('ENABLE_TELEGRAM_NOTIFICATIONS', 'False').lower() == 'true'
        
        # Email settings
        self.EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        self.EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        self.EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', '')
        
        # =============================================================================
        # VALIDATION
        # =============================================================================
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical configuration settings"""
        
        # Check if API credentials are provided
        if not self.COINBASE_API_KEY or self.COINBASE_API_KEY == 'YOUR_REAL_API_KEY_HERE':
            logger.warning("⚠️ Coinbase API credentials not configured - API will run in mock mode")
            self.credentials_available = False
        else:
            logger.info("✅ Coinbase API credentials found")
            self.credentials_available = True
        
        # Validate trading parameters
        if self.MAX_TOTAL_POSITION_SIZE <= 0:
            raise ValueError("MAX_TOTAL_POSITION_SIZE must be greater than 0")
        
        if self.MIN_USD_RESERVE < 0:
            raise ValueError("MIN_USD_RESERVE cannot be negative")
        
        logger.info(f"📊 Configuration loaded: {len(self.TRADING_PAIRS)} trading pairs, "
                   f"Trading: {'Enabled' if self.ENABLE_TRADING else 'Disabled'}, "
                   f"Mode: {'Sandbox' if self.SANDBOX_MODE else 'Live'}")
    
    def get_exchange_config(self):
        """Get exchange configuration for ccxt"""
        config = {
            'apiKey': self.COINBASE_API_KEY,
            'secret': self.COINBASE_API_SECRET,
            'sandbox': self.SANDBOX_MODE,
            'enableRateLimit': True,
        }
        
        # Only add passphrase if it exists (not needed for newer Coinbase Advanced Trade)
        if self.COINBASE_PASSPHRASE:
            config['passphrase'] = self.COINBASE_PASSPHRASE
            
        return config
    
    def get_pair_config(self, symbol):
        """Get configuration for specific trading pair"""
        base_currency = symbol.split('/')[0]
        
        config_map = {
            'BTC': {
                'enabled': self.BTC_ENABLED,
                'position_size': self.BTC_POSITION_SIZE,
                'take_profit': self.BTC_TAKE_PROFIT,
                'stop_loss': self.BTC_STOP_LOSS,
                'timeframe': self.BTC_TIMEFRAME
            },
            'ETH': {
                'enabled': self.ETH_ENABLED,
                'position_size': self.ETH_POSITION_SIZE,
                'take_profit': self.ETH_TAKE_PROFIT,
                'stop_loss': self.ETH_STOP_LOSS,
                'timeframe': self.ETH_TIMEFRAME
            }
        }
        
        # Default configuration for other pairs
        default_config = {
            'enabled': True,
            'position_size': 30.0,
            'take_profit': 2.0,
            'stop_loss': 0.8,
            'timeframe': '15m'
        }
        
        return config_map.get(base_currency, default_config)
    
    def is_credentials_configured(self):
        """Check if API credentials are properly configured"""
        return (self.COINBASE_API_KEY and 
                self.COINBASE_API_KEY != 'YOUR_REAL_API_KEY_HERE' and
                self.COINBASE_API_SECRET and 
                self.COINBASE_API_SECRET != 'YOUR_REAL_SECRET_HERE')
                # Note: passphrase not required for newer Coinbase Advanced Trade API

# Create global config instance
config = EnhancedConfig()

# For easy importing
__all__ = ['EnhancedConfig', 'config']
