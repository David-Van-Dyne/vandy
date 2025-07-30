"""
Enhanced Profit Optimizer with Dynamic Scaling
Optimizes entry points, position sizes, and automatically reinvests profits for compound growth
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProfitOptimizer:
    """Enhanced profit optimizer with dynamic scaling and compound growth"""
    
    def __init__(self):
        """Initialize the enhanced profit optimizer"""
        self.min_profit_threshold = 0.5  # Minimum expected profit %
        self.max_risk_per_trade = 2.0    # Maximum risk per trade %
        
        # Dynamic scaling parameters
        self.initial_portfolio_value = 0.0
        self.portfolio_growth_history = []
        self.performance_multiplier = 1.0
        self.profit_reinvestment_rate = 0.75  # 75% of profits reinvested
        self.max_position_scaling = 3.0  # Max 3x initial position sizes
        
        # Performance tracking for dynamic adjustment
        self.recent_trades = []
        self.win_rate = 0.0
        self.avg_profit_per_trade = 0.0
        self.last_optimization = datetime.now()
        
        logger.info("Enhanced Profit optimizer with dynamic scaling initialized")
    
    def initialize_baseline(self, initial_portfolio_value: float):
        """Set the initial portfolio baseline for growth tracking"""
        self.initial_portfolio_value = initial_portfolio_value
        self.portfolio_growth_history = [initial_portfolio_value]
        logger.info(f"[DATA] Portfolio baseline set: ${initial_portfolio_value:.2f}")
    
    def update_portfolio_growth(self, current_portfolio_value: float):
        """Track portfolio growth over time for dynamic scaling"""
        if self.initial_portfolio_value == 0:
            self.initial_portfolio_value = current_portfolio_value
        
        self.portfolio_growth_history.append(current_portfolio_value)
        
        # Keep only last 100 values for performance
        if len(self.portfolio_growth_history) > 100:
            self.portfolio_growth_history = self.portfolio_growth_history[-100:]
        
        # Calculate growth percentage
        growth_percentage = ((current_portfolio_value - self.initial_portfolio_value) / 
                           self.initial_portfolio_value) * 100
        
        # Update performance multiplier based on growth
        self.performance_multiplier = max(1.0, min(self.max_position_scaling, 
                                                  1.0 + (growth_percentage / 100)))
        
        logger.info(f"[UP] Portfolio growth: {growth_percentage:.1f}% | "
                   f"Performance multiplier: {self.performance_multiplier:.2f}x")
    
    def calculate_dynamic_position_size(self, signal_strength: float, 
                                      available_usd: float, 
                                      base_position_size: float,
                                      volatility: float = 1.0) -> float:
        """Calculate dynamic position size with profit reinvestment scaling"""
        try:
            # Base calculation from original method
            base_percentage = 0.2  # 20% base
            
            # Signal strength adjustment (50-100 scale)
            strength_multiplier = max(0, (signal_strength - 50) / 50)  # 0 to 1
            strength_adjustment = strength_multiplier * 0.1  # Up to 10% additional
            
            # Volatility adjustment (lower volatility = larger position)
            volatility_adjustment = max(0, (5 - volatility) / 50)  # Up to 10% additional
            
            # NEW: Performance-based scaling
            performance_adjustment = (self.performance_multiplier - 1.0) * 0.15  # Up to 15% more
            
            # NEW: Win rate bonus (if we have enough data)
            win_rate_bonus = 0.0
            if len(self.recent_trades) >= 5:
                win_rate_bonus = max(0, (self.win_rate - 0.5) * 0.1)  # Up to 5% more for >50% win rate
            
            # Calculate final percentage
            final_percentage = (base_percentage + strength_adjustment + 
                              volatility_adjustment + performance_adjustment + win_rate_bonus)
            final_percentage = min(final_percentage, 0.5)  # Max 50% of available USD
            
            # Apply to available USD
            calculated_size = available_usd * final_percentage
            
            # Ensure we don't exceed the scaled base position size
            max_scaled_size = base_position_size * self.performance_multiplier
            final_size = min(calculated_size, max_scaled_size)
            
            logger.info(f"[MONEY] Dynamic position: ${final_size:.2f} "
                       f"(base: ${base_position_size:.2f}, "
                       f"multiplier: {self.performance_multiplier:.2f}x, "
                       f"final %: {final_percentage:.1%})")
            
            return final_size
            
        except Exception as e:
            logger.error(f"Error calculating dynamic position size: {e}")
            return base_position_size  # Fallback to base size
    
    def optimize_entry_with_scaling(self, signals: List[Dict[str, Any]], symbol: str, 
                                   available_usd: float, pair_config: Dict[str, Any],
                                   current_portfolio_value: float) -> List[Dict[str, Any]]:
        """Enhanced signal optimization with dynamic scaling"""
        optimized_signals = []
        
        try:
            # Update portfolio tracking
            self.update_portfolio_growth(current_portfolio_value)
            
            for signal in signals:
                # Get base position size from config
                base_position_size = pair_config.get('position_size', 50.0)
                
                # Calculate dynamic position size
                dynamic_size = self.calculate_dynamic_position_size(
                    signal.get('strength', 50),
                    available_usd,
                    base_position_size,
                    signal.get('volatility', 1.0)
                )
                
                # Enhanced risk/reward calculation
                expected_return = self._calculate_expected_return(signal, dynamic_size)
                max_risk = self._calculate_max_risk(signal, dynamic_size)
                
                # Add comprehensive optimization data
                optimized_signal = signal.copy()
                optimized_signal.update({
                    'optimized_size': dynamic_size,
                    'base_size': base_position_size,
                    'scaling_multiplier': self.performance_multiplier,
                    'expected_return': expected_return,
                    'max_risk': max_risk,
                    'risk_reward_ratio': expected_return / max_risk if max_risk > 0 else 2.0,
                    'profit_potential': expected_return,
                    'portfolio_allocation': (dynamic_size / current_portfolio_value) * 100,
                    'confidence_score': self._calculate_confidence_score(signal),
                    'scaled_score': signal.get('strength', 50) * self.performance_multiplier
                })
                
                optimized_signals.append(optimized_signal)
            
            if optimized_signals:
                logger.info(f"[OK] Optimized {len(optimized_signals)} signals for {symbol} "
                           f"with {self.performance_multiplier:.2f}x scaling")
            
            return optimized_signals
            
        except Exception as e:
            logger.error(f"Error optimizing signals with scaling: {e}")
            return signals
    
    def _calculate_expected_return(self, signal: Dict, position_size: float) -> float:
        """Calculate expected return based on signal strength and position size"""
        base_return_rate = 0.025  # 2.5% base expected return
        strength_bonus = (signal.get('strength', 50) - 50) / 50 * 0.015  # Up to 1.5% bonus
        performance_bonus = (self.performance_multiplier - 1.0) * 0.01  # Performance scaling
        
        total_return_rate = base_return_rate + strength_bonus + performance_bonus
        return position_size * total_return_rate
    
    def _calculate_max_risk(self, signal: Dict, position_size: float) -> float:
        """Calculate maximum risk based on signal and position"""
        base_risk_rate = 0.015  # 1.5% base risk
        volatility_risk = signal.get('volatility', 1.0) * 0.005  # Volatility adjustment
        
        total_risk_rate = base_risk_rate + volatility_risk
        return position_size * total_risk_rate
    
    def _calculate_confidence_score(self, signal: Dict) -> float:
        """Calculate confidence score for the signal"""
        base_confidence = signal.get('strength', 50) / 100  # 0.5 to 1.0
        
        # Boost confidence based on recent performance
        performance_boost = min(0.2, (self.performance_multiplier - 1.0) * 0.1)
        win_rate_boost = max(0, (self.win_rate - 0.5) * 0.4) if len(self.recent_trades) >= 5 else 0
        
        final_confidence = min(1.0, base_confidence + performance_boost + win_rate_boost)
        return final_confidence
    
    def record_trade_result(self, symbol: str, entry_price: float, exit_price: float, 
                           position_size: float, trade_type: str):
        """Record trade results for performance tracking"""
        try:
            pnl = 0.0
            if trade_type.lower() == 'buy':
                pnl = (exit_price - entry_price) / entry_price * position_size
            else:
                pnl = (entry_price - exit_price) / entry_price * position_size
            
            trade_result = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'pnl': pnl,
                'profit_percent': (pnl / position_size) * 100,
                'position_size': position_size,
                'was_profitable': pnl > 0
            }
            
            self.recent_trades.append(trade_result)
            
            # Keep only last 50 trades
            if len(self.recent_trades) > 50:
                self.recent_trades = self.recent_trades[-50:]
            
            # Update performance metrics
            self._update_performance_metrics()
            
            logger.info(f"[LOG] Trade recorded: {symbol} PnL: ${pnl:.2f} "
                       f"({trade_result['profit_percent']:.2f}%)")
            
        except Exception as e:
            logger.error(f"Error recording trade result: {e}")
    
    def _update_performance_metrics(self):
        """Update performance metrics from recent trades"""
        if not self.recent_trades:
            return
        
        # Calculate win rate
        profitable_trades = sum(1 for trade in self.recent_trades if trade['was_profitable'])
        self.win_rate = profitable_trades / len(self.recent_trades)
        
        # Calculate average profit per trade
        total_pnl = sum(trade['pnl'] for trade in self.recent_trades)
        self.avg_profit_per_trade = total_pnl / len(self.recent_trades)
        
        logger.info(f"[DATA] Performance update - Win rate: {self.win_rate:.1%}, "
                   f"Avg profit: ${self.avg_profit_per_trade:.2f}")
    
    def get_scaling_recommendations(self, current_portfolio_value: float) -> Dict[str, Any]:
        """Get recommendations for position scaling and risk adjustment"""
        if self.initial_portfolio_value == 0:
            return {"status": "baseline_not_set"}
        
        growth_percent = ((current_portfolio_value - self.initial_portfolio_value) / 
                         self.initial_portfolio_value) * 100
        
        recommendations = {
            "portfolio_growth": f"{growth_percent:.1f}%",
            "current_multiplier": f"{self.performance_multiplier:.2f}x",
            "recommended_action": self._get_scaling_action(growth_percent),
            "risk_level": self._assess_risk_level(),
            "reinvestment_amount": current_portfolio_value * self.profit_reinvestment_rate
        }
        
        return recommendations
    
    def _get_scaling_action(self, growth_percent: float) -> str:
        """Determine recommended scaling action based on growth"""
        if growth_percent < -10:
            return "REDUCE_RISK: Consider smaller positions"
        elif growth_percent < 0:
            return "MAINTAIN: Keep current strategy"
        elif growth_percent < 20:
            return "SCALE_MODEST: Increase positions by 10-20%"
        elif growth_percent < 50:
            return "SCALE_SIGNIFICANT: Increase positions by 30-50%"
        else:
            return "SCALE_AGGRESSIVE: Maximum scaling active"
    
    def _assess_risk_level(self) -> str:
        """Assess current risk level based on performance"""
        if self.win_rate > 0.7 and self.avg_profit_per_trade > 0:
            return "LOW_RISK: Excellent performance"
        elif self.win_rate > 0.5 and self.avg_profit_per_trade > 0:
            return "MODERATE_RISK: Good performance"
        elif self.win_rate > 0.4:
            return "ELEVATED_RISK: Mixed performance"
        else:
            return "HIGH_RISK: Poor recent performance"
            logger.error(f"Error optimizing signals: {e}")
            return signals
    
    def calculate_optimal_position_size(self, signal_strength: float, 
                                      available_usd: float, 
                                      volatility: float) -> float:
        """Calculate optimal position size based on signal strength and volatility"""
        try:
            # Base position size as percentage of available USD
            base_percentage = 0.2  # 20% base
            
            # Adjust based on signal strength (50-100 scale)
            strength_multiplier = (signal_strength - 50) / 50  # 0 to 1
            strength_adjustment = strength_multiplier * 0.1  # Up to 10% additional
            
            # Adjust based on volatility (lower volatility = larger position)
            volatility_adjustment = max(0, (5 - volatility) / 50)  # Up to 10% additional
            
            # Calculate final percentage
            final_percentage = base_percentage + strength_adjustment + volatility_adjustment
            final_percentage = min(final_percentage, 0.4)  # Max 40%
            
            return available_usd * final_percentage
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return available_usd * 0.2  # Default to 20%
