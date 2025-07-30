# Multi-Currency Trading Bot

A sophisticated cryptocurrency trading bot that supports simultaneous trading of multiple digital assets using individual strategies and risk management parameters.

## 🚀 Features

### Multi-Currency Support
- **Bitcoin (BTC/USD)** - Your proven performer
- **Ethereum (ETH/USD)** - Popular altcoin with higher volatility
- **Solana (SOL/USD)** - High-growth potential
- **Cardano (ADA/USD)** - Alternative blockchain platform
- **Polkadot (DOT/USD)** - Interoperability focused

### Advanced Portfolio Management
- **Individual Risk Parameters** - Each currency has its own take profit/stop loss
- **Position Size Management** - Configurable USD amounts per currency
- **Concurrent Position Limits** - Control how many positions can be open
- **USD Reserve Management** - Maintain minimum cash reserves
- **Portfolio Allocation Limits** - Prevent over-concentration

### Smart Trading Logic
- **SMA Strategy per Currency** - 3/8 SMA crossover signals
- **Market Condition Checks** - Validate market health before trading
- **Dynamic Position Sizing** - Adjust based on available funds
- **Automatic Rebalancing** - Continuously monitor and execute

## 📁 File Structure

### Core Multi-Currency Files
- **`multi_currency_bot.py`** - Main multi-currency trading bot
- **`multi_currency_config.py`** - Enhanced configuration management
- **`multi_currency_manager.py`** - Portfolio management utility
- **`migration_assistant.py`** - Single to multi-currency migration

### Configuration Files
- **`.env.multi_currency_template`** - Complete configuration template
- **`.env`** - Your active configuration (you create this)

### Legacy Single-Currency Files (Still Available)
- **`simple_live_bot.py`** - Your current Bitcoin-only bot
- **`config.py`** - Original single-currency configuration

## 🔧 Quick Start

### Option 1: Conservative Approach (Recommended for First-Time)
Enable just BTC and ETH trading:

```bash
# 1. Copy and configure your .env file
cp .env.multi_currency_template .env

# 2. Edit .env and set:
BTC_ENABLED=True
ETH_ENABLED=True
SOL_ENABLED=False
ADA_ENABLED=False
DOT_ENABLED=False

# 3. Set your funding
MIN_USD_RESERVE=50.0
BTC_POSITION_SIZE=45.0
ETH_POSITION_SIZE=40.0

# 4. Start in testing mode first
ENABLE_TRADING=False

# 5. Run the bot
python multi_currency_bot.py
```

**Minimum Funding Required:** $135 ($45 + $40 + $50 reserve)

### Option 2: Use Migration Assistant
```bash
python migration_assistant.py
```
Follow the interactive prompts to migrate from your current single-currency setup.

### Option 3: Use Management Utility
```bash
python multi_currency_manager.py
```
Get recommendations based on your budget and preferences.

## ⚙️ Configuration Guide

### Currency Configuration Format
Each currency follows this pattern in `.env`:

```env
# Currency Configuration
{CURRENCY}_ENABLED=True/False
{CURRENCY}_POSITION_SIZE=USD_amount
{CURRENCY}_TAKE_PROFIT=percentage
{CURRENCY}_STOP_LOSS=percentage
{CURRENCY}_TIMEFRAME=15m
{CURRENCY}_MIN_BALANCE=minimum_balance
{CURRENCY}_SHORT_SMA=3
{CURRENCY}_LONG_SMA=8
```

### Example Multi-Currency Setup
```env
# Bitcoin (Conservative)
BTC_ENABLED=True
BTC_POSITION_SIZE=45.0
BTC_TAKE_PROFIT=2.0
BTC_STOP_LOSS=0.5

# Ethereum (Moderate)
ETH_ENABLED=True
ETH_POSITION_SIZE=40.0
ETH_TAKE_PROFIT=2.5
ETH_STOP_LOSS=0.7

# Solana (Aggressive)
SOL_ENABLED=True
SOL_POSITION_SIZE=35.0
SOL_TAKE_PROFIT=3.0
SOL_STOP_LOSS=1.0
```

## 💰 Funding Requirements

### Budget-Based Recommendations

#### Small Budget ($100-200)
- Enable: BTC only or BTC + ETH
- Position sizes: $25-45 each
- Keep higher USD reserves (30-40%)

#### Medium Budget ($200-500)
- Enable: BTC + ETH + 1 altcoin
- Position sizes: $40-60 each
- Moderate USD reserves (20-25%)

#### Large Budget ($500+)
- Enable: All desired currencies
- Position sizes: $50-100 each
- Standard USD reserves (15-20%)

### Risk Management Calculator
```bash
python multi_currency_manager.py
# Select option 2: "Analyze Portfolio Requirements"
```

## 🔄 Migration from Single-Currency

If you're currently using the single-currency `simple_live_bot.py`:

### Automatic Migration
```bash
python migration_assistant.py
```

### Manual Migration
1. **Backup your current .env**
   ```bash
   cp .env .env.backup
   ```

2. **Create multi-currency .env**
   ```bash
   cp .env.multi_currency_template .env
   ```

3. **Transfer your API credentials**
   - Copy COINBASE_API_KEY
   - Copy COINBASE_API_SECRET  
   - Copy COINBASE_PASSPHRASE

4. **Configure currencies**
   - Set BTC_ENABLED=True (your current trading)
   - Enable additional currencies as desired
   - Adjust position sizes based on budget

5. **Test first**
   ```bash
   ENABLE_TRADING=False
   python multi_currency_bot.py
   ```

## 🧪 Testing and Validation

### Step 1: Connection Testing
```bash
python multi_currency_manager.py
# Select option 1: "Test Currency Connections"
```

### Step 2: Dry Run
Set `ENABLE_TRADING=False` in your `.env` and run:
```bash
python multi_currency_bot.py
```
This will show signals and intended actions without placing real trades.

### Step 3: Live Trading
When ready, set `ENABLE_TRADING=True` and run:
```bash
python multi_currency_bot.py
```

## 📊 Monitoring and Management

### Real-Time Portfolio View
The bot provides continuous portfolio updates:
```
💼 PORTFOLIO SUMMARY - 14:30:15
--------------------------------------------------
💵 USD: $123.45 (Available: $73.45)
₿ BTC: 0.000374 ($45.12) 🟢 OPEN
₿ ETH: 0.000000 ($0.00) 🔵 CLOSED
💰 Total Portfolio: $168.57
```

### Management Commands
```bash
# Check current positions
python multi_currency_manager.py
# Select option 3: "Show Current Positions"

# Analyze requirements
python multi_currency_manager.py  
# Select option 2: "Analyze Portfolio Requirements"

# Get configuration recommendations
python multi_currency_manager.py
# Select option 4: "Get Configuration Recommendations"
```

## 🛡️ Risk Management Features

### Position Limits
- **MAX_CONCURRENT_POSITIONS**: Limit open positions
- **MAX_TOTAL_POSITION_SIZE**: Cap total investment
- **MIN_USD_RESERVE**: Maintain cash buffer

### Individual Currency Risk
- **Take Profit %**: Lock in gains automatically
- **Stop Loss %**: Limit downside risk
- **Position Size**: Control exposure per currency

### Portfolio Risk
- **Emergency Stop Loss**: Portfolio-wide protection
- **Allocation Limits**: Prevent over-concentration
- **Dynamic Sizing**: Adjust positions based on available funds

## 🔧 Advanced Configuration

### Custom Currency Addition
To add a new currency (e.g., MATIC/USD):

1. **Add to multi_currency_config.py**:
   ```python
   'MATIC/USD': {
       'enabled': os.getenv('MATIC_ENABLED', 'False').lower() == 'true',
       'position_size_usd': float(os.getenv('MATIC_POSITION_SIZE', '25.0')),
       # ... other parameters
   }
   ```

2. **Add to .env**:
   ```env
   MATIC_ENABLED=True
   MATIC_POSITION_SIZE=25.0
   MATIC_TAKE_PROFIT=4.0
   MATIC_STOP_LOSS=1.5
   ```

### Strategy Customization
Each currency can have different SMA parameters:
```env
BTC_SHORT_SMA=3    # Fast signals
BTC_LONG_SMA=8

ETH_SHORT_SMA=5    # Slower, more stable signals  
ETH_LONG_SMA=15
```

## 🚨 Safety Guidelines

### Before Going Live
1. **Test thoroughly** with ENABLE_TRADING=False
2. **Start small** with 1-2 currencies only
3. **Monitor closely** for first few trades
4. **Have sufficient funding** for all enabled currencies
5. **Understand the risks** of each currency

### Risk Warnings
- **High Volatility**: Cryptocurrency markets are extremely volatile
- **24/7 Markets**: Prices can change rapidly at any time
- **Multiple Exposures**: More currencies = more risk vectors
- **Funding Requirements**: Ensure adequate USD for all positions
- **Technical Risk**: Bot malfunctions could result in losses

### Emergency Procedures
```bash
# Stop all trading immediately
# Set in .env:
ENABLE_TRADING=False

# Or use emergency stop script
python tests_and_debug/emergency_stop.py
```

## 📈 Performance Tracking

### Built-in Metrics
- Individual currency P&L
- Portfolio-wide performance
- Trade frequency per currency
- Success rate by currency

### External Tracking
Consider keeping a trading journal to track:
- Entry/exit prices and reasons
- Market conditions during trades
- Strategy performance over time
- Funding requirements vs. actual usage

## 🔄 Switching Between Bots

### Use Single-Currency Bot
```bash
python simple_live_bot.py  # Your original Bitcoin-only bot
```

### Use Multi-Currency Bot
```bash
python multi_currency_bot.py  # New multi-currency bot
```

Both bots can use the same exchange account and API credentials. They share the same underlying exchange manager and strategy components.

## 🆘 Troubleshooting

### Common Issues

#### "Insufficient USD" Errors
- Check your USD balance
- Reduce position sizes
- Increase MIN_USD_RESERVE
- Disable some currencies

#### Currency Not Trading
- Verify currency is enabled in .env
- Check minimum balance requirements
- Ensure sufficient USD available
- Verify API supports the trading pair

#### Connection Issues
```bash
python multi_currency_manager.py
# Select option 1: "Test Currency Connections"
```

### Getting Help
1. Check the error messages in the bot output
2. Run the management utility for diagnostics
3. Review your .env configuration
4. Test individual components

## 📞 Support Files

- **Migration Assistant**: `migration_assistant.py`
- **Management Utility**: `multi_currency_manager.py`  
- **Configuration Template**: `.env.multi_currency_template`
- **Test Scripts**: All files in `tests_and_debug/` folder

---

**⚠️ IMPORTANT**: Always test new configurations with `ENABLE_TRADING=False` before risking real money. Cryptocurrency trading involves substantial risk of loss.
