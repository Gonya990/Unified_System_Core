-- Compliance Logging Schema (DAC8 Directive Compliant)
-- Directive on Administrative Cooperation (8th amendment)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.compliance_trades (
    internal_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp_utc TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_id VARCHAR(100) UNIQUE NOT NULL,
    asset_pair VARCHAR(20) NOT NULL,    -- e.g. BTC/USDT
    trade_side VARCHAR(10) NOT NULL,    -- BUY/SELL
    executed_qty DECIMAL(36, 18),      -- Crypto precision
    price_executed DECIMAL(36, 18),
    fmv_fiat_value DECIMAL(36, 2),     -- Fair Market Value in USD/EUR
    fee_amount DECIMAL(36, 18),
    fee_currency VARCHAR(10),
    counterparty_id VARCHAR(255) DEFAULT 'Bybit_V5_UTA',
    tx_hash VARCHAR(255),               -- If on-chain
    metadata JSONB                      -- Raw response for audit
);

CREATE INDEX idx_trade_timestamp ON public.compliance_trades(timestamp_utc);
CREATE INDEX idx_trade_asset ON public.compliance_trades(asset_pair);
