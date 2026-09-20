# Finora: Enterprise Financial Intelligence

**Finora** is a premium, AI-powered financial intelligence platform designed for B2B and enterprise use cases. It tracks transactions, analyzes department-level spending behavior, and provides real-time, mathematically accurate financial insights via a grounded AI Copilot.

Unlike standard LLM wrappers, Finora uses a **Deterministic Analytics Engine** connected to the AI via **Function Calling**. This ensures the AI never hallucinates balances, math, or financial history.

## 🚀 Key Features

*   **Financial Dashboard:** Real-time metrics including Total Balance, Monthly Revenue/Expenses, and Net Savings Rate with dynamic Area and Bar charts.
*   **System Intelligence Engine:**
    *   *Recurring Expense Detection:* Automatically identifies software subscriptions, payroll, and recurring vendor bills.
    *   *Anomaly Detection:* Statistically isolates highly unusual spending spikes using moving averages and standard deviations.
    *   *Month-over-Month Comparisons:* Tracks granular changes in category spending over time.
*   **Grounded AI Copilot (FinoraAI):** Powered by Groq's high-speed inference and the `gpt-oss-20b` model. The Copilot translates natural language into structured API queries, fetching real backend data. It renders responses in beautiful, native Markdown (including tables) thanks to `react-markdown` and `@tailwindcss/typography`.
*   **Enterprise Department Management:** Track budgets and balances across distinct departments (Engineering, HR, Sales, Executive).
*   **Premium UX/UI:** Built with React, Tailwind CSS, and Recharts. Features micro-animations, skeleton loaders, and a responsive mobile sidebar with a sleek, polished SaaS aesthetic.

## 🛠️ Technology Stack

### Frontend
*   React 18 + TypeScript + Vite
*   Tailwind CSS (Styling + Typography plugin)
*   Recharts (Data Visualization)
*   Lucide React (Icons)
*   React-Markdown (Rich Text AI Responses)

### Backend
*   Python 3.12
*   FastAPI (Web Framework)
*   PostgreSQL (Database)
*   SQLAlchemy 2.0 (ORM) + Alembic (Migrations)
*   Groq API (AI Inference & Tool Calling)
*   Docker & Docker Compose (Orchestration)

## 🏗️ Architecture

Finora follows a strict **Service-Oriented Architecture** with the Repository Pattern:
1.  **Routers (`api/routers/`)**: Handles HTTP requests, validation, and JWT verification.
2.  **Services (`services/`)**: Contains all core business logic, deterministic analytics, and AI orchestration.
3.  **Repositories (`repositories/`)**: Manages all SQLAlchemy database transactions and queries.

## 🏃‍♂️ Running Locally

### Prerequisites
*   Docker Desktop installed and running
*   Node.js (v18+)

### 1. Environment Setup
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
*Note: You must add a valid `GROQ_API_KEY` to your root `.env` file for the FinoraAI Copilot to function.*

### 2. Start the Backend (Docker)
The Docker configuration is heavily optimized with a `.dockerignore` file for rapid builds, and automatically runs Alembic migrations and database seeding on startup.
```bash
docker compose up --build -d
```
The backend API will be available at `http://localhost:8000`.

### 3. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

### 4. Explore the Demo
Simply click the **"Explore Demo"** button on the Login page to instantly authenticate into a seeded enterprise account containing a full 12 months of realistic B2B financial data.

## ☁️ Production Deployment

Finora is completely configured for cloud deployment:
*   **Frontend**: Ready for deployment on Vercel or Netlify.
*   **Backend**: Includes a `render.yaml` for instant Web Service and PostgreSQL deployment on Render. The `Dockerfile` natively handles DB migrations and seeding on production startup.
