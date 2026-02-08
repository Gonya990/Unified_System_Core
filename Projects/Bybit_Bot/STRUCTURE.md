Bybit_Bot/
├── services/
│   ├── ingestion/
│   │   ├── main.py          # Service A: WebSocket collector
│   │   └── Dockerfile
│   ├── alpha/
│   │   ├── strategy.py      # Service B: Signal generation (Delta Neutral)
│   │   └── Dockerfile
│   ├── execution/
│   │   ├── orders.py        # Service C: Batch execution + Leader Election
│   │   └── Dockerfile
│   ├── risk/
│   │   ├── guardian.py      # Service D: Pre-trade risk validation
│   │   └── Dockerfile
│   └── compliance/
│       ├── schema.sql       # Service E: DB Schema (DAC8)
│       ├── logger.py        # Transaction logger
│       └── Dockerfile
├── k8s/
│   ├── ai_agent_deployment.yaml  # GPU MIG Agent
│   ├── execution_deployment.yaml # Leader-elected executor
│   ├── secrets.yaml
│   └── configmap.yaml
└── common/
    └── proto/               # Redis Streams / gRPC
