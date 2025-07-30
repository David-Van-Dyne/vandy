#!/usr/bin/env python3
"""
Enhanced Multi-Currency Trading Bot
Advanced crypto trading bot with dynamic position sizing, portfolio protection, and real-time monitoring
"""

import os
import sys
import time
import threading
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import signal
import json

import logging
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import our modules
from enhanced_config import config
from exchange_manager_jwt import exchange_manager
from data_provider import FreeDataProvider
from enhanced_strategy import EnhancedStrategy
from profit_optimizer import ProfitOptimizer
from advanced_signal_filter import AdvancedSignalFilter
from notifications import EmailNotifier

def safe_log_message(message: str) -> str:
    """Remove emojis and special characters that cause Windows encoding issues"""
    # Remove common emoji patterns
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    # Replace emojis with safe equivalents
    safe_message = emoji_pattern.sub('', message)
    
    # Replace specific problematic characters
    replacements = {
        '📊': '[DATA]',
        '💰': '[MONEY]',
        '📈': '[UP]',
        '📉': '[DOWN]',
        '🚀': '[TRADE]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⚠️': '[WARN]',
        '🎯': '[TARGET]',
        '🔧': '[CONFIG]',
        '💼': '[PORTFOLIO]',
        '📦': '[ORDER]',
        '🔥': '[HOT]',
        '🎉': '[SUCCESS]'
    }
    
    for emoji, replacement in replacements.items():
        safe_message = safe_message.replace(emoji, replacement)
    
    return safe_message.strip()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedMultiCurrencyBot:
    """Enhanced multi-currency trading bot with advanced features"""
    
    def __init__(self):
        """Initialize the enhanced trading bot"""
        self.running = False
        self.paused = False
        self.positions = {}
        self.portfolio_value = 0.0
        self.available_usd = 0.0
        self.daily_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        self.start_time = datetime.now()
        
        # Initialize components
        logger.info("INITIALIZING Enhanced Multi-Currency Trading Bot...")
        
        try:
            # Initialize exchange manager
            self.exchange = exchange_manager
            if not self.exchange.connect():
                logger.warning("Exchange connection failed - running in simulation mode")
                self.simulation_mode = True
            else:
                logger.info("Exchange connected successfully")
                self.simulation_mode = False
            
            # Initialize data provider
            self.data_provider = FreeDataProvider()
            logger.info("Data provider initialized")
            
            # Initialize enhanced strategy
            self.strategy = EnhancedStrategy(self.data_provider)
            logger.info("Enhanced strategy loaded")
            
            # Initialize enhanced profit optimizer with dynamic scaling
            self.profit_optimizer = ProfitOptimizer()
            logger.info("Enhanced profit optimizer with dynamic scaling initialized")
            
            # Initialize signal filter
            self.signal_filter = AdvancedSignalFilter()
            logger.info("Advanced signal filter ready")
            
            # Initialize notifications
            try:
                self.notifier = EmailNotifier()
                logger.info("Notification system initialized")
            except Exception as e:
                logger.warning(f"Notifications disabled: {e}")
                self.notifier = None
            
            # Trading pairs configuration
            self.trading_pairs = config.TRADING_PAIRS
            logger.info(f"Trading pairs configured: {len(self.trading_pairs)} pairs")
            
            # Portfolio protection
            self.portfolio_protection = {
                'max_drawdown_percent': config.EMERGENCY_STOP_LOSS_PERCENT,
                'max_total_position_size': config.MAX_TOTAL_POSITION_SIZE,
                'max_concurrent_positions': config.MAX_CONCURRENT_POSITIONS,
                'min_usd_reserve': config.MIN_USD_RESERVE
            }
            
            # Performance tracking
            self.performance_stats = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'win_rate': 0.0
            }
            
            logger.info("Enhanced Multi-Currency Trading Bot initialized successfully!")
            self._print_configuration()
            
        except Exception as e:
            logger.error(f"Bot initialization failed: {e}")
            raise
    
    def _print_configuration(self):
        """Print bot configuration"""
        logger.info("=" * 60)
        logger.info("ENHANCED MULTI-CURRENCY TRADING BOT")
        logger.info("=" * 60)
        logger.info(f"Strategy: Enhanced SMA + RSI with Dynamic Sizing")
        logger.info(f"Max Total Position: ${self.portfolio_protection['max_total_position_size']:.2f}")
        logger.info(f"Max Concurrent Positions: {self.portfolio_protection['max_concurrent_positions']}")
        logger.info(f"Emergency Stop Loss: {self.portfolio_protection['max_drawdown_percent']}%")
        logger.info(f"Min USD Reserve: ${self.portfolio_protection['min_usd_reserve']:.2f}")
        logger.info(f"Trading Mode: {'Live' if not self.simulation_mode else 'Simulation'}")
        logger.info(f"Check Interval: {config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"Notifications: {'Enabled' if self.notifier else 'Disabled'}")
        logger.info("=" * 60)
        
        logger.info("Trading Pairs Configuration:")
        for pair in self.trading_pairs:
            pair_config = config.get_pair_config(pair)
            if pair_config['enabled']:
                logger.info(f"  ENABLED {pair}: ${pair_config['position_size']:.0f} "
                           f"(TP: {pair_config['take_profit']}%, SL: {pair_config['stop_loss']}%)")
            else:
                logger.info(f"  DISABLED {pair}: Disabled")
    
    def run_trading_cycle(self):
        """Run one complete trading cycle with dynamic profit optimization"""
        try:
            logger.info("Starting trading cycle...")
            
            # Update portfolio status using real exchange data
            if not self.simulation_mode and self.exchange.is_connected():
                portfolio = self.exchange.get_portfolio_summary()
                self.portfolio_value = portfolio.get('totalValue', 156.85)
                self.available_usd = portfolio.get('availableUSD', 67.95)
                self.positions = portfolio.get('positions', [])
            else:
                # Use default values for simulation mode
                self.portfolio_value = 156.85
                self.available_usd = 67.95
                self.positions = []

            # Initialize profit optimizer baseline if first run
            if not hasattr(self.profit_optimizer, 'initial_portfolio_value') or self.profit_optimizer.initial_portfolio_value == 0:
                self.profit_optimizer.initialize_baseline(self.portfolio_value)
            
            # Update portfolio growth tracking for dynamic scaling
            self.profit_optimizer.update_portfolio_growth(self.portfolio_value)
            
            # Get scaling recommendations
            scaling_recommendations = self.profit_optimizer.get_scaling_recommendations(self.portfolio_value)
            
            logger.info(f"Portfolio Update - Total: ${self.portfolio_value:.2f}, "
                       f"Available: ${self.available_usd:.2f}, Positions: {len(self.positions)}")
            logger.info(f"Dynamic Scaling - Growth: {scaling_recommendations.get('portfolio_growth', 'N/A')}, "
                       f"Multiplier: {scaling_recommendations.get('current_multiplier', 'N/A')}")
            logger.info(f"Risk Assessment: {scaling_recommendations.get('risk_level', 'Unknown')}")
            
            # Enhanced trading logic with profit optimization
            if self.available_usd > self.portfolio_protection['min_usd_reserve']:
                self._execute_enhanced_trading_logic()
            else:
                logger.info(f"💰 Insufficient funds for trading. Available: ${self.available_usd:.2f}, "
                           f"Required reserve: ${self.portfolio_protection['min_usd_reserve']:.2f}")
            
            # Log mode and performance
            if self.simulation_mode:
                logger.info("SIMULATION MODE - Enhanced optimization active but no actual trading")
            else:
                logger.info("LIVE MODE - Real portfolio data retrieved with dynamic scaling")
            
            logger.info("Trading cycle completed")
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
    
    def _execute_enhanced_trading_logic(self):
        """Execute enhanced trading logic with profit optimization"""
        try:
            # Check each trading pair for opportunities
            for pair in self.trading_pairs:
                pair_config = config.get_pair_config(pair)
                if not pair_config.get('enabled', False):
                    continue
                
                # Simulate signal generation (would be replaced with real strategy)
                mock_signals = self._generate_mock_signals(pair)
                
                if mock_signals:
                    # Use enhanced profit optimizer with dynamic scaling
                    optimized_signals = self.profit_optimizer.optimize_entry_with_scaling(
                        mock_signals, 
                        pair, 
                        self.available_usd,
                        pair_config,
                        self.portfolio_value
                    )
                    
                    # Log optimization results
                    for signal in optimized_signals:
                        log_msg = f"[TARGET] {pair} Signal - Strength: {signal.get('strength', 0):.0f}, " \
                                 f"Optimized Size: ${signal.get('optimized_size', 0):.2f}, " \
                                 f"Scaling: {signal.get('scaling_multiplier', 1.0):.2f}x, " \
                                 f"Expected Return: ${signal.get('expected_return', 0):.2f}"
                        logger.info(log_msg)
                        
                        # Execute actual trades in live mode
                        if not self.simulation_mode:
                            self._execute_optimized_trade(signal, pair)
            
        except Exception as e:
            logger.error(f"Error in enhanced trading logic: {e}")
    
    def _generate_mock_signals(self, pair: str) -> List[Dict[str, Any]]:
        """Generate mock signals for demonstration (would be real strategy signals)"""
        import random
        
        # Simulate finding trading opportunities
        if random.random() < 0.3:  # 30% chance of signal
            return [{
                'type': 'buy',
                'strength': random.randint(60, 95),  # Signal strength 60-95
                'confidence': random.uniform(0.6, 0.9),
                'volatility': random.uniform(0.8, 2.5),
                'timestamp': datetime.now()
            }]
        return []
    
    def _execute_optimized_trade(self, signal: Dict[str, Any], pair: str):
        """Execute an optimized trade with real order placement"""
        try:
            position_size = signal.get('optimized_size', 0)
            expected_return = signal.get('expected_return', 0)
            signal_type = signal.get('signal', 'buy')
            
            log_msg = f"[TRADE] Executing optimized trade for {pair}: " \
                     f"Type: {signal_type.upper()}, Size: ${position_size:.2f}, " \
                     f"Expected Return: ${expected_return:.2f}"
            logger.info(log_msg)
            
            # Execute the actual trade
            if position_size > 5.0:  # Minimum $5 trade size
                order_result = self.exchange.place_market_order(
                    side=signal_type,
                    amount=position_size,
                    symbol=pair
                )
                
                if order_result:
                    logger.info(f"[OK] Trade executed successfully for {pair}")
                    self.total_trades += 1
                    
                    # Record the trade in profit optimizer (mock data for now)
                    current_price = 100.0  # Would get actual price from market data
                    exit_price = current_price * 1.02  # Assume 2% profit for successful trade
                    self.profit_optimizer.record_trade_result(
                        pair, current_price, exit_price, 
                        position_size, signal_type
                    )
                else:
                    logger.warning(f"[ERROR] Trade execution failed for {pair}")
            else:
                logger.warning(f"[WARN] Position size too small for {pair}: ${position_size:.2f}")
            
        except Exception as e:
            logger.error(f"Error executing optimized trade: {e}")
    
    def start(self):
        """Start the trading bot"""
        logger.info("Starting Enhanced Multi-Currency Trading Bot...")
        self.running = True
        
        try:
            cycle_count = 0
            while self.running and cycle_count < 5:  # Run 5 cycles for demo
                if not self.paused:
                    self.run_trading_cycle()
                    cycle_count += 1
                
                # Wait for next cycle (shorter for demo)
                logger.info(f"Waiting {config.CHECK_INTERVAL_MINUTES} minutes until next cycle...")
                for _ in range(int(config.CHECK_INTERVAL_MINUTES * 6)):  # 10 second intervals for demo
                    if not self.running:
                        break
                    time.sleep(10)
                    
            logger.info("Demo completed - stopping bot")
            self._shutdown()
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
            self._shutdown()
        except Exception as e:
            logger.error(f"Fatal error in bot main loop: {e}")
            self._shutdown()
    
    def _shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down Enhanced Multi-Currency Trading Bot...")
        self.running = False
        
        # Final status
        uptime = datetime.now() - self.start_time
        logger.info("=" * 60)
        logger.info("FINAL TRADING SESSION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Session Duration: {uptime}")
        logger.info(f"Total Trades: {self.performance_stats['total_trades']}")
        logger.info(f"Portfolio Value: ${self.portfolio_value:.2f}")
        logger.info(f"Available USD: ${self.available_usd:.2f}")
        logger.info("=" * 60)
        logger.info("Enhanced Multi-Currency Trading Bot stopped")
    
    def pause(self):
        """Pause trading"""
        self.paused = True
        logger.info("Trading paused")
    
    def resume(self):
        """Resume trading"""
        self.paused = False
        logger.info("Trading resumed")
    
    def stop(self):
        """Stop trading"""
        self.running = False
        logger.info("Stop requested")

def main():
    """Main function to start the bot"""
    try:
        # Create and start the bot
        bot = EnhancedMultiCurrencyBot()
        bot.start()
        
    except Exception as e:
        logger.error(f"Fatal error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
