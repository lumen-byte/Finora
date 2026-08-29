# Finora

**Finora** is a premium, AI-powered financial intelligence platform designed to track transactions, analyze spending behavior, and provide real-time, mathematically accurate financial insights via a grounded AI Copilot.

Unlike standard LLM wrappers, Finora uses a **Deterministic Analytics Engine** connected to the AI via **Function Calling**. This ensures the AI never hallucinates balances, math, or financial history.

## 🚀 Features

*   **Financial Dashboard:** Real-time metrics including Total Balance, Monthly Income/Expenses, and Savings Rate with dynamic Area charts.
*   **System Intelligence Engine:**
    *   *Recurring Detection:* Automatically identifies subscriptions, rent, and recurring bills.
    *   *Anomaly Detection:* Statistically isolates highly unusual spending spikes using moving averages and standard deviations.
    *   *Month-over-Month Comparisons:* Tracks granular changes in category spending over time.
*   **Grounded AI Copilot:** Powered by Groq (Qwen 27B), the Copilot translates natural language into structured API queries, fetching real backend data to construct accurate, non-hallucinated answers.
*   **Transaction Management:** Full filtering (Income/Expense, Date Ranges, Search) with clean, paginated data tables.
*   **Premium UX/UI:** Built with React, Tailwind CSS, and Recharts. Features micro-animations, skeleton loaders, and a responsive mobile sidebar.

## 🛠️ Tech Stack

### Frontend
*   React 18 + TypeScript + Vite
*   Tailwind CSS (Styling)
*   Recharts (Data Visualization)
*   Lucide React (Icons)
*   Axios (API Client)

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
Copy the example environment files:
```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```
*Note: You must add a valid `GROQ_API_KEY` to your root `.env` file for the AI Copilot to function.*

### 2. Start the Backend (Docker)
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
Click the **"Explore Demo"** button on the landing page to instantly log in to a seeded demo account containing 6 months of realistic financial data.
