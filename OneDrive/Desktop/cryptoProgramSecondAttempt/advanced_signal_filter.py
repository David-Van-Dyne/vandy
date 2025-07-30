"""
Advanced Signal Filter
Filters and validates trading signals to improve accuracy
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AdvancedSignalFilter:
    """Advanced signal filtering and validation"""
    
    def __init__(self):
        """Initialize the signal filter"""
        self.min_signal_strength = 50  # Lower threshold for more opportunities
        self.max_signals_per_hour = 3
        self.recent_signals = []
        logger.info("Advanced signal filter initialized")
    
    def filter_signals(self, signals: List[Dict[str, Any]], symbol: str, 
                      df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Filter signals based on advanced criteria"""
        filtered_signals = []
        
        try:
            for signal in signals:
                if self._validate_signal(signal, symbol, df):
                    filtered_signals.append(signal)
            
            if filtered_signals:
                logger.info(f"Filtered {len(signals)} -> {len(filtered_signals)} signals for {symbol}")
            
            return filtered_signals
            
        except Exception as e:
            logger.error(f"Error filtering signals: {e}")
            return signals
    
    def _validate_signal(self, signal: Dict[str, Any], symbol: str, df: pd.DataFrame) -> bool:
        """Validate individual signal"""
        try:
            # Check signal strength
            strength = signal.get('strength', 0)
            if strength < self.min_signal_strength:
                return False
            
            # Check recent price volatility
            if len(df) >= 10:
                recent_volatility = df['close'].tail(10).pct_change().std() * 100
                if recent_volatility > 5.0:  # Too volatile
                    return False
            
            # Check if we haven't had too many recent signals
            if len(self.recent_signals) >= self.max_signals_per_hour:
                return False
            
            # Add to recent signals
            self.recent_signals.append({
                'symbol': symbol,
                'signal': signal.get('signal'),
                'timestamp': signal.get('timestamp')
            })
            
            # Keep only recent signals (last hour)
            if len(self.recent_signals) > self.max_signals_per_hour:
                self.recent_signals = self.recent_signals[-self.max_signals_per_hour:]
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating signal: {e}")
            return False
