# AI Governance & Model Risk Management Platform

A full-stack application for managing AI model inventories, assessing model risks, reviewing approvals, and maintaining audit records through a centralized governance workflow.

## Overview

As organizations increasingly adopt AI systems, they need a structured way to track models, evaluate potential risks, manage approvals, and maintain accountability.

The **AI Governance & Model Risk Management Platform** provides a centralized application to support these activities. It combines a FastAPI backend, a React frontend, and PostgreSQL for data persistence.

The project demonstrates how software engineering concepts such as role-based access control, REST APIs, database modeling, authentication, approval workflows, and audit logging can be applied to AI governance.

## Key Features

- **AI Model Inventory:** Register and retrieve AI model records through REST APIs.
- **Risk Assessment:** Calculate an illustrative risk score using impact and likelihood inputs.
- **Approval Workflow:** Support reviewer decisions such as approve, reject, and request changes.
- **Role-Based Access Control:** Define roles for analysts, reviewers, administrators, auditors, and model owners.
- **Authentication:** Secure API access using JWT-based authentication and password hashing.
- **Audit Logging:** Record application-level events related to governance activities.
- **Database Persistence:** Store users, models, risk assessments, approvals, and audit records in PostgreSQL.
- **Containerized Setup:** Use Docker Compose to run the application services locally.

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React, TypeScript, Vite |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, Argon2 password hashing |
| API | REST |
| Containerization | Docker, Docker Compose |

## Architecture

```text
              React + TypeScript
                      |
                      | REST API
                      |
                 FastAPI Backend
                      |
        +-------------+-------------+
        |             |             |
   Authentication  Governance   Audit Logging
        |           Workflows        |
        |             |              |
        +-------------+--------------+
                      |
                  SQLAlchemy
                      |
                  PostgreSQL
```

## Project Structure

```text
ai-governance-model-risk-platform/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── dependencies/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── App.tsx
│   │   └── style.css
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

*The structure above represents the main application areas; individual filenames may vary as the project evolves.*

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.10+
- Node.js and npm
- Docker Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/vishuuu09/ai-governance-model-risk-platform.git

cd ai-governance-model-risk-platform
```

### 2. Configure Environment Variables

Create your local environment file using the example:

```bash
cp .env.example .env
```

On Windows PowerShell, you can use:

```powershell
Copy-Item .env.example .env
```

Update the environment variables in `.env` according to your local setup. Use a strong secret key and never commit your actual `.env` file.

### 3. Start the Database

From the project root:

```bash
docker compose up -d db
```

### 4. Run the Backend

Open a terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 5. Run the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal.

## Security Considerations

- Passwords are hashed rather than stored as plain text.
- JWT-based authentication is used for protected API access.
- Role-based authorization restricts access to selected operations.
- Environment variables are used for application configuration.
- Self-approval is restricted in the approval workflow.

This project is a development-stage implementation. Audit logging is application-level and should not be considered tamper-proof. Additional security hardening is required before production deployment.

## Current Scope and Limitations

The current implementation focuses on core governance workflows and application architecture.

The risk score is illustrative and is not a validated regulatory or enterprise model-risk scoring methodology. The application is not certified for regulatory compliance.

Additional work is needed for production deployment, automated tests, database migrations, comprehensive governance controls, advanced reporting, and expanded administrative workflows.

## Future Enhancements

- AI model lifecycle monitoring
- Explainability and bias evaluation modules
- Compliance control mapping
- Advanced risk analytics and dashboards
- Automated testing and CI/CD integration
- Database migrations using Alembic
- Enhanced audit integrity and reporting
- Cloud deployment and monitoring

## Learning Outcomes

This project explores practical implementation of:

- Full-stack application development
- REST API design using FastAPI
- Database design and ORM integration
- JWT authentication and role-based authorization
- Workflow and approval management
- Audit event tracking
- Docker-based development environments

## Author

**Sai Vishal Mittapalli**

GitHub: [@vishuuu09](https://github.com/vishuuu09)

Project Repository: [AI Governance & Model Risk Management Platform](https://github.com/vishuuu09/ai-governance-model-risk-platform)
