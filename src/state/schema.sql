-- market_cache: Latest coin data
CREATE TABLE IF NOT EXISTS market_cache (
    ticker VARCHAR PRIMARY KEY,
    sector VARCHAR,
    metrics_json JSON,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- trade_history: All executed trades
CREATE TABLE IF NOT EXISTS trade_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticker VARCHAR NOT NULL,
    entry_p DECIMAL(18,8),
    exit_p DECIMAL(18,8),
    fas_score DECIMAL(5,2),
    pnl DECIMAL(18,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- system_config: Bot configuration
CREATE TABLE IF NOT EXISTS system_config (
    param_name VARCHAR PRIMARY KEY,
    param_value VARCHAR NOT NULL,
    is_locked BOOLEAN DEFAULT FALSE
);

-- ops_ledger: Profit tax & bills
CREATE TABLE IF NOT EXISTS ops_ledger (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    amount DECIMAL(18,8) NOT NULL,
    category VARCHAR NOT NULL, -- 'profit_tax' | 'bill_payment' | 'reserve'
    description VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- eval_history: Quarterly/annual evaluations
CREATE TABLE IF NOT EXISTS eval_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    period_type VARCHAR NOT NULL, -- 'micro' | 'quarterly' | 'annual'
    period_start DATE,
    period_end DATE,
    roi_actual DECIMAL(8,4),
    roi_target DECIMAL(8,4),
    met_target BOOLEAN,
    config_snapshot JSON,
    action_taken VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
