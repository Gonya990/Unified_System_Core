# Unified System Core - Development Guide

This is the central routing guide for the Modern Software Engineering skills
and AI agent framework.

---

## Project Structure & Logic

Refer to [SYSTEM_MAP.md](file:///Users/macbook/Documents/Unified_System/SYSTEM_MAP.md)
for the full logical layout.

- `Career/`: Personal and professional development assets.
- `Management/`: Project planning, tasks (Beads), and logs.
- **AI Bot**: Located in `Projects/AI_Core`.
- **Sync Logic**: `Scripts/Orchestration/full_sync.sh` links states.
- `Scripts/Orchestration/`: Core system-wide automation.
- `Scripts/Production_Factory/`: Video and content generation pipeline.
- `Reports/Archived_Status/`: History of system audits and fix reports.
- `Infra/`: Infrastructure setup and environment configurations.
- `Local_Dev/`: Transient development files (Cache, Venv, Media).

---

## Communication Guidelines

**Primary Preference**:

- **English Translation Protocol**: Answer in **English**. If the original source or intent was in Russian, add the tag **[russian]** at the beginning of the response. DO NOT include the original Russian text.
- **Context**: Ensure technical terms are clear and context is preserved.

---

## Quick Navigation

### Skills Framework

**Location**: `skills/`

- **Learning Pillar**: `iterative-development`, `feedback-driven-design`,
  `experimental-workflow`, `deployment-pipeline-designer`, `empirical-measurement`
- **Complexity Pillar**: `separation-of-concerns-enforcer`, `modularity-architect`,
  `cohesion-coach`, `abstraction-patterns`, `coupling-minimizer`
- **Supporting Skills**: `refactoring-mastery`, `high-performance-simplicity`,
  `frontend-aesthetics`, `youth-brand-ux`
- **Architecture Skills**: `python-hexagonal-development`, `python-test-strategy`

**Index**: `skills/README.md`

---

### Agent Framework

**Location**: `.claude/agents/`

- **Discovery**: `code-explorer`, `api-discoverer`, `dependency-mapper`
- **Architecture**: `code-architect`, `hexagonal-architecture-guardian`,
  `performance-optimizer`
- **Implementation**: `implementer`, `bug-fixer`
- **Review/Test**: `code-reviewer`, `tdd-cycle-driver`
- **Coordination**: `code-quality-coordinator`, `devops-workflow-orchestrator`
- **DevOps**: `security-hardening-worker`, `performance-optimization-worker`
- **UI/UX**: `senior-ui-ux-designer`

**Index**: `.claude/agents/README.md`

---

### Orchestration Guidelines

**Location**: `docs/agent-guidelines/`

| Document | Purpose |
|----------|---------|
| `velocity-principles.md` | Agent speed optimization |
| `orchestration-principles.md` | Multi-agent coordination |
| `agent-capability-patterns.md` | Agent types and boundaries |
| `context-management.md` | Token efficiency |
| `feedback-optimization.md` | Fast feedback loops |
| `parallel-execution-patterns.md` | Concurrent execution |
| `orchestration-metrics.md` | DORA metrics |
| `IMPLEMENTATION.md` | 5 orchestration patterns |

**Templates**: `docs/agent-guidelines/templates/`
**Test Results**: `docs/agent-guidelines/test-results/`

---

### Programming Patterns

**Location**: `docs/patterns/`

| Category | Patterns |
|----------|----------|
| `workflows/` | tdd-workflow, trunk-based-development |
| `architecture/` | hexagonal-architecture |
| `tooling/` | uv-package-manager, pydantic-patterns, pytest-patterns |

---

## Subagent Orchestration

### Level 0: Direct Tools (< 5 seconds)

```bash
Read file              # Direct Read tool
Grep pattern          # Direct Grep tool
```

### Level 1: Single Subagent (< 60 seconds)

```yaml
Task: "Find authentication patterns"
Agent: code-explorer
```

### Level 2: Sequential Pipeline (< 180 seconds)

```yaml
Pipeline:
  1. code-explorer → understand patterns
  2. code-architect → design blueprint
  3. implementer → implement with tests
  4. code-reviewer → review quality
```

### Level 3: Parallel Execution (< 90 seconds)

```yaml
Parallel:
  - code-explorer(module=auth)
  - code-explorer(module=billing)
Then: Synthesize results
```

### Level 4: Hierarchical Coordination (< 300 seconds)

```yaml
Flow:
  1. code-quality-coordinator discovers scope
  2. Spawns workers in parallel
  3. Aggregates results
```

---

## Two Pillars Always Active

```yaml
learning:
  - iterate (small batches)
  - feedback (fast at all levels)
  - experiment (hypothesis-driven)
  - measure (DORA metrics)

complexity:
  - separate_concerns (essential vs accidental)
  - modularize (clear boundaries)
  - maintain_cohesion (related together)
  - minimize_coupling (loose between modules)
```

---

## Tool Commands

```bash
# UV Package Manager
uv sync                           # Setup
uv run pytest tests/ -v           # Run tests
uv run ruff check src/            # Lint
uv run mypy src/                  # Type check

# TDD Cycle
uv run pytest tests/test_x.py::test_y -v   # Single test
uv run pytest --cov=src           # Coverage
```

---

## Directory Structure

```text
Unified_System_Core/
├── .claude/
│   └── agents/           # 16 AI agent definitions
├── skills/               # 18 programming skills (by pillar)
├── docs/
│   ├── agent-guidelines/ # Orchestration framework
│   └── patterns/         # Programming patterns
└── CLAUDE.md             # This file
```

---

## Agent Mail Identity

All configuration is in `.env` (see `.env.example` for template):

| Variable | Description |
|----------|-------------|
| `AGENT_MAIL_NAME` | Persistent agent name (e.g., VioletCastle) |
| `AGENT_MAIL_PROGRAM` | Agent program (claude-code) |
| `AGENT_MAIL_MODEL` | Model identifier |
| `AGENT_MAIL_PROJECT` | Billboard project path (shared by all agents) |
| `AGENT_MAIL_SERVER` | MCP server URL (unified-home-core-cloud) |

See `.claude/commands/sync-mail.md` for full workflow and agent registry.

---

**Based on**: "Modern Software Engineering" by Dave Farley

<firebase_prompts hash="f9c861cf">
<!-- Firebase Tools Context - Auto-generated, do not edit -->
# Firebase CLI Context

<project-structure>
```
project/
├── firebase.json          # Main configuration
├── .firebaserc           # Project aliases
├── firestore.rules       # Security rules
├── functions/            # Cloud Functions
├── public/               # Hosting files
└── firebase-debug.log    # Created when CLI commands fail
```
</project-structure>

## Common Commands

<example>
```bash
# Initialize new features
firebase init hosting
firebase init functions
firebase init firestore

# Deploy everything or specific services

firebase deploy
firebase deploy --only hosting
firebase deploy --only functions:processOrder,functions:sendEmail
firebase deploy --except functions

# Switch between projects

firebase use staging
firebase use production
```
</example>

## Local Development

<example>
```bash
# Start all emulators
firebase emulators:start

# Start specific emulators
firebase emulators:start --only functions,firestore

# Common emulator URLs
# Emulator UI: http://localhost:4000
# Functions: http://localhost:5001
# Firestore: http://localhost:8080
# Hosting: http://localhost:5000
````

</example>

## Debugging Failed Commands

<example>
```bash
# When any firebase command fails
cat firebase-debug.log    # Contains detailed error traces

# Common fixes for errors in debug log

firebase login --reauth # Fix authentication errors
firebase use # Fix wrong project errors

````
</example>

## Complete Workflow Example

<example>
```bash
# Clone and setup a Firebase project
git clone https://github.com/example/my-app
cd my-app

# Initialize Firebase in existing project
firebase init

# Start local development
firebase emulators:start

# Make changes, then deploy to staging
firebase use staging
firebase deploy

# Deploy to production
firebase use production
firebase deploy --only hosting,firestore
````

</example>

## Service Detection in firebase.json

<example>
```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
  },
  "functions": {
    "source": "functions",
    "runtime": "nodejs20"
  },
  "firestore": {
    "rules": "firestore.rules",
    "indexes": "firestore.indexes.json"
  },
  "emulators": {
    "functions": { "port": 5001 },
    "firestore": { "port": 8080 },
    "hosting": { "port": 5000 }
  }
}
```
</example>


# Firebase Functions Context (SDK 6.0.0+)

Always use v2 functions for new development. Use v1 only for Analytics, basic Auth, and Test Lab triggers.

For SDK versions before 6.0.0, add `/v2` to import paths (e.g., `firebase-functions/v2/https`).

## Function Imports (SDK 6.0.0+)

<example>
```typescript
// HTTPS functions
import {onRequest, onCall} from 'firebase-functions/https';

// Firestore triggers
import {onDocumentCreated, onDocumentUpdated, onDocumentDeleted} from 'firebase-functions/firestore';

// RTDB triggers
import {onValueCreated, onValueWritten, onValueUpdated, onValueDeleted} from 'firebase-functions/database';

// Scheduled functions
import {onSchedule} from 'firebase-functions/scheduler';

// Storage triggers
import {onObjectFinalized, onObjectDeleted} from 'firebase-functions/storage';

// Pub/Sub triggers
import {onMessagePublished} from 'firebase-functions/pubsub';

// Blocking Auth triggers
import {beforeUserCreated, beforeUserSignedIn} from 'firebase-functions/identity';

// Test Lab triggers
import {onTestMatrixCompleted} from 'firebase-functions/testLab';

// Deferred initialization
import {onInit} from 'firebase-functions';

// Structured logging
import {logger} from 'firebase-functions';

// Configuration
import {defineString, defineInt, defineSecret} from 'firebase-functions/params';
import * as params from 'firebase-functions/params';

// Note: For SDK versions before 6.0.0, add /v2 to import paths:
// import {onRequest} from 'firebase-functions/v2/https';

````
</example>

## v1 Functions (Analytics & Basic Auth Only)

<example>
```typescript
// Use v1 ONLY for these triggers
import * as functionsV1 from 'firebase-functions/v1';
import {logger} from 'firebase-functions';

// Analytics triggers (v1 only)
export const onPurchase = functionsV1.analytics.event('purchase').onLog((event) => {
  logger.info('Purchase event', {
    value: event.params?.value,
    currency: event.params?.currency
  });
});

// Basic Auth triggers (v1 only)
export const onUserCreate = functionsV1.auth.user().onCreate((user) => {
  logger.info('User created', { uid: user.uid, email: user.email });
  // Initialize user profile...
});

export const onUserDelete = functionsV1.auth.user().onDelete((user) => {
  logger.info('User deleted', { uid: user.uid });
  // Cleanup user data...
});
````

</example>

## Environment Configuration

<example>
```typescript
import {defineString, defineInt, defineSecret} from 'firebase-functions/params';
import * as params from 'firebase-functions/params';
import {onRequest} from 'firebase-functions/https';
import {logger} from 'firebase-functions';

// Built-in params available automatically
const projectId = params.projectID;
const databaseUrl = params.databaseURL;
const bucket = params.storageBucket;
const gcpProject = params.gcloudProject;

// Custom params
const apiUrl = defineString('API_URL', {
  default: 'https://api.example.com'
});

const environment = defineString('ENVIRONMENT', {
  default: 'dev'
});

const apiKey = defineSecret('STRIPE_KEY');

// Using params directly in runtime configuration
export const processPayment = onRequest({
  secrets: [apiKey],
  memory: defineString('PAYMENT_MEMORY', { default: '1GiB' }),
  minInstances: environment.equals('production').thenElse(5, 0),
  maxInstances: environment.equals('production').thenElse(1000, 10)
}, async (req, res) => {
  logger.info('Processing payment', {
    project: projectId.value(),
    bucket: bucket.value(),
    env: environment.value()
  });

  const key = apiKey.value();
  const url = apiUrl.value();
  // Process payment...
});

````
</example>

## Deferred Initialization

<example>
```typescript
import {onInit} from 'firebase-functions';
import {onRequest} from 'firebase-functions/https';

let heavyClient: HeavySDK;

onInit(async () => {
  const {HeavySDK} = await import('./lib/heavy-sdk');
  heavyClient = new HeavySDK({
    // Expensive initialization...
  });
});

export const useHeavyClient = onRequest(async (req, res) => {
  const result = await heavyClient.process(req.body);
  res.json(result);
});
````

</example>

## Structured Logging

<example>
```typescript
import {logger} from 'firebase-functions';
import {onRequest} from 'firebase-functions/https';

interface OrderRequest {
  orderId: string;
  userId: string;
  amount: number;
}

export const processOrder = onRequest(async (req, res) => {
  const {orderId, userId, amount} = req.body as OrderRequest;

  logger.info("Processing order", {
    orderId,
    userId,
    amount
  });

  try {
    // Process...
    logger.log("Order complete", { orderId });
    res.json({ success: true });
  } catch (error) {
    logger.error("Order failed", {
      orderId,
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    });
    res.status(500).json({ error: "Processing failed" });
  }
});

````
</example>

## Development Commands

<example>
```bash
# TypeScript development
cd functions
npm install
npm run build        # Compile TypeScript

# Local development

firebase emulators:start --only functions

# Testing functions

npm test # Run unit tests
npm run serve # TypeScript watch + emulators

# Deployment

firebase deploy --only functions
firebase deploy --only functions:api,functions:onUserCreate

# Debugging

firebase functions:log
firebase functions:log --only api --lines=50

````

</example>

</firebase_prompts>