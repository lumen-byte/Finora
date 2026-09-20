# Finora: Enterprise Financial Intelligence Engine

**Live Application:** [https://finora-lumenbyte1.vercel.app/](https://finora-lumenbyte1.vercel.app/)
**Source Code:** [https://github.com/lumen-byte/Finora](https://github.com/lumen-byte/Finora)

*Finora is an enterprise-grade financial intelligence engine that bridges deterministic financial analytics with a mathematically grounded Large Language Model.*

## Problem Statement & Solution

Traditional financial dashboards provide static historical data, forcing operators into manual spreadsheet analysis to extract actionable insights. Conversely, introducing standard Large Language Models (LLMs) to financial data inherently introduces the risk of mathematical hallucinations and data fabrication—a critical failure in enterprise contexts.

Finora resolves this dichotomy. It decouples computational analytics from natural language inference. All mathematical operations and data aggregations are executed by a strict Deterministic Analytics Engine. The LLM is restricted entirely to a routing and presentation layer via Function Calling, enabling operators to query financial states conversationally while maintaining absolute mathematical certainty.

## Core Platform Overview

Finora is a robust, AI-augmented financial intelligence platform engineered for enterprise and B2B workflows. It aggregates transactional data, executes deterministic analyses on department-level spending behaviors, and interfaces with a grounded LLM to surface real-time, mathematically validated insights.

The platform distinguishes itself from standard LLM wrappers by leveraging a strict Function Calling architecture. Analytical computation is isolated within the Deterministic Analytics Engine; the LLM acts solely as a natural language routing layer and presentation interface, mathematically guaranteeing that the system never hallucinates balances, transaction histories, or statistical aggregations.

## System Architecture

Finora is built on a decoupled, service-oriented architecture designed for scalability and strict separation of concerns.

### Frontend Client
- **Framework:** React 18 with TypeScript, orchestrated by Vite.
- **State & Routing:** Context-driven state management with React Router for SPA navigation.
- **Data Visualization:** Recharts for dynamic rendering of high-density time-series financial data.
- **LLM Rendering:** Integrated `react-markdown` and `remark-gfm` pipelines to safely parse and style structured AI responses, including tabular data and inline tool-execution badges.
- **Styling:** Utility-first styling via Tailwind CSS, enforcing a strict design system and typography hierarchy.

### Backend API
- **Framework:** Python 3.12 executing FastAPI under ASGI (Uvicorn).
- **Data Persistence:** PostgreSQL 15+, interfaced via SQLAlchemy 2.0 (ORM) with Alembic for deterministic schema migrations.
- **Design Pattern:** Strict Repository-Service pattern. Data access logic (Repositories) is entirely decoupled from business logic and LLM orchestration (Services).
- **Inference Layer:** Interoperable with OpenAI-compatible endpoints (currently optimized for Groq's high-throughput `openai/gpt-oss-20b` endpoint), strictly enforcing JSON-schema function definitions.

## Core Analytics Modules

- **Temporal Trend Analysis:** Calculates month-over-month (MoM) deltas and normalizes historical spending vectors across distinct departments (e.g., Engineering, Human Resources, Executive).
- **Recurring Signature Detection:** Iterates over historical transactional graphs to identify recurring frequency patterns, isolating SaaS subscriptions, payroll, and infrastructural overhead.
- **Statistical Anomaly Isolation:** Employs standard deviation thresholds and moving averages against categorized expense vectors to detect statistically significant spending spikes in real-time.

## Infrastructure & Deployment

### Local Orchestration
The local development environment is containerized via Docker and Docker Compose. The build context is optimized via `.dockerignore` for minimal image footprints.
Upon container initialization, the entrypoint executes:
1. Alembic schema upgrades to ensure database parity.
2. An idempotent seeding pipeline that generates 12 months of structured B2B transactional data.
3. The Uvicorn ASGI server.

To spin up the local cluster:
```bash
# 1. Configure the environment
cp .env.example .env
cp frontend/.env.example frontend/.env

# 2. Initialize the backend cluster
docker compose up --build -d

# 3. Initialize the frontend client
cd frontend
npm install
npm run dev
```

### Production CI/CD
- **Frontend Distribution:** The React client is optimized for Edge deployment (e.g., Vercel, Netlify) via static artifact generation.
- **Backend Infrastructure:** The API and PostgreSQL instances are configured for stateless PaaS deployment (e.g., Render, Railway) utilizing native Dockerfile builds and managed PostgreSQL instances.

## Authentication & Access
The platform utilizes stateless JWT authentication. A pre-configured demonstration protocol allows immediate access to the seeded enterprise dataset without requiring explicit user registration, facilitating rapid evaluation of the analytical engine.
