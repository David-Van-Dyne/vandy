# ENHANCED MULTI-CURRENCY BOT - CORE FILE STRUCTURE
# These are the essential files for your working bot system

## CORE BOT FILES (Required)
✅ enhanced_multi_currency_bot.py     # Main bot with dynamic position sizing + portfolio protection + profit optimization
✅ exchange_manager_jwt.py            # Coinbase Advanced Trade API (JWT auth)
✅ enhanced_strategy.py              # Multi-indicator trading strategy
✅ profit_optimizer.py               # Advanced profit optimization (NEW)
✅ advanced_signal_filter.py         # Multi-timeframe signal filtering (NEW)
✅ sma_rsi_strategy.py               # Legacy SMA/RSI strategy (backup)
✅ data_provider.py                  # Market data fetching
✅ config.py                         # Base configuration settings
✅ enhanced_config.py                # Enhanced strategy configuration + portfolio protection
✅ multi_currency_config.py          # Static fallback configuration
✅ dynamic_config.json               # Dynamic 8-currency configuration
✅ start_bot.bat                     # Bot startup script

## SAFETY & TESTING FILES (Important)
✅ test_position_protection.py       # Position safety testing
✅ test_enhanced_strategy.py         # Strategy testing
✅ test_portfolio_protection.py      # Portfolio protection testing

## CONFIGURATION & DEPENDENCIES
✅ .env                              # API keys and environment variables
✅ requirements.txt                  # Python package dependencies

## OPTIONAL UTILITY FILES (can keep or move)
⚪ quick_status.py                   # Check bot status
⚪ status_check.py                   # System status check
⚪ test_bot_init.py                  # Configuration testing (created today)
⚪ test_config_loading.py            # Configuration validation

## DIRECTORIES
📁 .venv/                           # Python virtual environment
📁 tests_and_debug/                 # Testing and debugging scripts
📁 __pycache__/                     # Python bytecode cache (auto-generated)

## DOCUMENTATION (keep for reference)
📄 DYNAMIC_TRADING_README.md        # Documentation
📄 EMAIL_SETUP_GUIDE.md            # Email notification setup
📄 MULTI_CURRENCY_README.md        # Multi-currency documentation

## FILES TO REMOVE/ARCHIVE
❌ All other .py files are legacy versions
❌ Empty .log files 
❌ Backup .env files
❌ Old exchange_manager versions
❌ Legacy bot versions (auto_bot, trading_bot, etc.)

Your current working system only needs the ✅ files above!
