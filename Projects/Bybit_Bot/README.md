# Bybit V5 Trading Bot Architecture (2026 Edition)

## Overview

A microservices-based, delta-neutral funding arbitrage bot designed for high fault tolerance, low latency, and full compliance with **DAC8** (EU Directive on Administrative Cooperation).

## Architecture

1. **Service A (Ingestion):** WebSocket client for Bybit V5 Linear Public stream. Produces `market_data` to Redis Streams.
2. **Service B (Alpha Engine):** Consumes `market_data`, performs ML-based funding rate prediction, calculates APR/Break-even metrics. Produces `signals`.
3. **Service C (Execution Engine):** Consumes `orders_validated`, manages Leader Election (Single Writer via K8s Leases), executes Batch Orders on Bybit. Produces `execution_reports`.
4. **Service D (Risk Guard):** Middleware. Consumes `signals`, validates leveraging, notional size, and daily loss limits. Produces `orders_validated`.
5. **Service E (Compliance Logger):** Consumes `execution_reports`, persistence in TimescaleDB.

## DAC8 Compliance (Rigor)

Every trade execution report logs:

- `order_id` (Exchange native)
- `asset_pair` (ISO/Standard)
- `fair_market_value` (FMV in FIAT at execution time)
- `fee_currency` & `fee_amount`
- `timestamp` (UTC, microsecond precision)

## Tech Stack

- **Messaging:** Redis Streams (Reliable Delivery) / gRPC (Internal IPC)
- **Database:** PostgreSQL + TimescaleDB (Time-series optimization)
- **Deployment:** K8s with NVIDIA MIG (GPU isolation for ML)
- **AI/ML:** Scikit-learn Linear Regression Overlay for FR Prediction.

## Quick Start

```bash
# Apply K8s Config
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/execution_deployment.yaml
# ... other deployments
```
