"""
Enhanced Trading Strategy
Combines multiple indicators for improved signal accuracy
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from enhanced_config import config

logger = logging.getLogger(__name__)

# Strategy parameters
SHORT_SMA_PERIOD = 10
LONG_SMA_PERIOD = 20
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
VOLUME_MA_PERIOD = 20
VOLATILITY_PERIOD = 14

class EnhancedStrategy:
    """Enhanced trading strategy with multiple indicators"""
    
    def __init__(self, data_provider):
        """Initialize the enhanced strategy"""
        self.data_provider = data_provider
        
        # Strategy parameters
        self.short_sma = SHORT_SMA_PERIOD
        self.long_sma = LONG_SMA_PERIOD
        self.rsi_period = RSI_PERIOD
        self.rsi_oversold = RSI_OVERSOLD
        self.rsi_overbought = RSI_OVERBOUGHT
        self.volume_ma_period = VOLUME_MA_PERIOD
        self.volatility_period = VOLATILITY_PERIOD
        
        # Signal strength thresholds
        self.min_signal_strength = 60
        self.strong_signal_threshold = 75
        
        logger.info("Enhanced strategy initialized with optimized parameters")
    
    def calculate_sma(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_volatility(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate price volatility (standard deviation)"""
        return data.pct_change().rolling(window=period).std() * 100
    
    def calculate_volume_profile(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate volume profile indicators"""
        if 'volume' not in df.columns:
            return {'volume_trend': 0, 'volume_ratio': 1.0}
        
        volume_sma = self.calculate_sma(df['volume'], self.volume_ma_period)
        current_volume = df['volume'].iloc[-1]
        avg_volume = volume_sma.iloc[-1]
        
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        volume_trend = 1 if volume_ratio > 1.2 else (-1 if volume_ratio < 0.8 else 0)
        
        return {
            'volume_trend': volume_trend,
            'volume_ratio': volume_ratio
        }
    
    def analyze_price_action(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze price action patterns"""
        close = df['close']
        high = df['high']
        low = df['low']
        
        # Recent price movement
        recent_change = ((close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]) * 100
        
        # Support and resistance levels
        recent_high = high.tail(20).max()
        recent_low = low.tail(20).min()
        current_price = close.iloc[-1]
        
        # Position in range
        range_position = (current_price - recent_low) / (recent_high - recent_low) if recent_high != recent_low else 0.5
        
        return {
            'recent_change': recent_change,
            'range_position': range_position,
            'near_resistance': range_position > 0.8,
            'near_support': range_position < 0.2,
            'recent_high': recent_high,
            'recent_low': recent_low
        }
    
    def generate_signals(self, df: pd.DataFrame, symbol: str = "") -> List[Dict[str, Any]]:
        """Generate trading signals based on multiple indicators"""
        if len(df) < max(self.long_sma, self.rsi_period, self.volume_ma_period):
            logger.warning(f"Insufficient data for {symbol}: {len(df)} bars")
            return []
        
        try:
            # Calculate indicators
            close = df['close']
            sma_short = self.calculate_sma(close, self.short_sma)
            sma_long = self.calculate_sma(close, self.long_sma)
            rsi = self.calculate_rsi(close, self.rsi_period)
            volatility = self.calculate_volatility(close, self.volatility_period)
            
            # Get current values
            current_price = close.iloc[-1]
            current_sma_short = sma_short.iloc[-1]
            current_sma_long = sma_long.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_volatility = volatility.iloc[-1]
            
            # Volume analysis
            volume_profile = self.calculate_volume_profile(df)
            
            # Price action analysis
            price_action = self.analyze_price_action(df)
            
            # Signal generation
            signals = []
            
            # Buy signal conditions
            buy_conditions = [
                current_sma_short > current_sma_long,  # Short SMA above long SMA
                current_rsi < 70,  # Not overbought
                current_rsi > 35,  # Not too oversold
                not price_action['near_resistance'],  # Not near resistance
                current_volatility < 5.0  # Not too volatile
            ]
            
            # Sell signal conditions
            sell_conditions = [
                current_sma_short < current_sma_long,  # Short SMA below long SMA
                current_rsi > 30,  # Not oversold
                current_rsi < 65,  # Not too overbought
                not price_action['near_support'],  # Not near support
                current_volatility < 5.0  # Not too volatile
            ]
            
            # Calculate signal strength
            buy_strength = self._calculate_signal_strength(
                df, 'buy', current_rsi, volume_profile, price_action, current_volatility
            )
            
            sell_strength = self._calculate_signal_strength(
                df, 'sell', current_rsi, volume_profile, price_action, current_volatility
            )
            
            # Generate buy signal
            if sum(buy_conditions) >= 4 and buy_strength >= self.min_signal_strength:
                signals.append({
                    'symbol': symbol,
                    'signal': 'buy',
                    'price': current_price,
                    'strength': buy_strength,
                    'rsi': current_rsi,
                    'sma_short': current_sma_short,
                    'sma_long': current_sma_long,
                    'volatility': current_volatility,
                    'volume_ratio': volume_profile['volume_ratio'],
                    'conditions_met': sum(buy_conditions),
                    'timestamp': df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
                })
            
            # Generate sell signal
            if sum(sell_conditions) >= 4 and sell_strength >= self.min_signal_strength:
                signals.append({
                    'symbol': symbol,
                    'signal': 'sell',
                    'price': current_price,
                    'strength': sell_strength,
                    'rsi': current_rsi,
                    'sma_short': current_sma_short,
                    'sma_long': current_sma_long,
                    'volatility': current_volatility,
                    'volume_ratio': volume_profile['volume_ratio'],
                    'conditions_met': sum(sell_conditions),
                    'timestamp': df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
                })
            
            if signals:
                logger.info(f"Generated {len(signals)} signals for {symbol}")
                for signal in signals:
                    logger.info(f"  Signal: {signal['signal'].upper()} - Strength: {signal['strength']:.1f}")
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating signals for {symbol}: {e}")
            return []
    
    def _calculate_signal_strength(self, df: pd.DataFrame, signal_type: str, 
                                 current_rsi: float, volume_profile: Dict, 
                                 price_action: Dict, volatility: float) -> float:
        """Calculate signal strength score (0-100)"""
        strength = 50  # Base strength
        
        try:
            # RSI contribution
            if signal_type == 'buy':
                if 40 <= current_rsi <= 60:
                    strength += 15
                elif 30 <= current_rsi < 40:
                    strength += 10
                elif current_rsi < 30:
                    strength += 5
            else:  # sell
                if 40 <= current_rsi <= 60:
                    strength += 15
                elif 60 < current_rsi <= 70:
                    strength += 10
                elif current_rsi > 70:
                    strength += 5
            
            # Volume contribution
            volume_ratio = volume_profile.get('volume_ratio', 1.0)
            if volume_ratio > 1.5:
                strength += 10
            elif volume_ratio > 1.2:
                strength += 5
            elif volume_ratio < 0.8:
                strength -= 5
            
            # Volatility contribution
            if volatility < 2.0:
                strength += 10
            elif volatility < 3.0:
                strength += 5
            elif volatility > 5.0:
                strength -= 10
            
            # Price action contribution
            if signal_type == 'buy' and price_action.get('range_position', 0.5) < 0.3:
                strength += 10
            elif signal_type == 'sell' and price_action.get('range_position', 0.5) > 0.7:
                strength += 10
            
            # Recent momentum
            recent_change = price_action.get('recent_change', 0)
            if signal_type == 'buy' and recent_change > 2:
                strength += 5
            elif signal_type == 'sell' and recent_change < -2:
                strength += 5
            
            # Ensure strength is within bounds
            strength = max(0, min(100, strength))
            
        except Exception as e:
            logger.warning(f"Error calculating signal strength: {e}")
            strength = 50
        
        return strength
    
    def get_dynamic_stop_loss(self, entry_price: float, signal_type: str, 
                            volatility: float) -> float:
        """Calculate dynamic stop loss based on volatility"""
        base_stop_loss = 0.02  # 2% base stop loss
        
        # Adjust based on volatility
        if volatility > 3.0:
            volatility_multiplier = 1.5
        elif volatility > 2.0:
            volatility_multiplier = 1.2
        else:
            volatility_multiplier = 1.0
        
        dynamic_stop_loss = base_stop_loss * volatility_multiplier
        
        # Apply the stop loss
        if signal_type == 'buy':
            stop_price = entry_price * (1 - dynamic_stop_loss)
        else:
            stop_price = entry_price * (1 + dynamic_stop_loss)
        
        return stop_price
    
    def get_dynamic_take_profit(self, entry_price: float, signal_type: str, 
                              signal_strength: float) -> float:
        """Calculate dynamic take profit based on signal strength"""
        base_take_profit = 0.03  # 3% base take profit
        
        # Adjust based on signal strength
        if signal_strength > 65:  # Lower threshold for more trades
            strength_multiplier = 1.5
        elif signal_strength > 70:
            strength_multiplier = 1.2
        else:
            strength_multiplier = 1.0
        
        dynamic_take_profit = base_take_profit * strength_multiplier
        
        # Apply the take profit
        if signal_type == 'buy':
            target_price = entry_price * (1 + dynamic_take_profit)
        else:
            target_price = entry_price * (1 - dynamic_take_profit)
        
        return target_price
