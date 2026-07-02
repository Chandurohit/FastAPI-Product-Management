# Telusko Trac - FastAPI + React Inventory Management

A professional, scalable, production-ready inventory management system built with FastAPI and React.

## Project Architecture

This project is structured according to the Single Responsibility Principle, separating route handling, business logic, database queries, and data validation into distinct layers.

### Directory Structure

```
D:/fastAPI-demo-recording/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── products.py          # Route definitions for v1 products API
│   ├── core/
│   │   ├── config.py                # Environment configuration loading via Pydantic Settings
│   │   ├── logging.py               # Structured logging configuration
│   │   └── security.py              # Placeholders for future authentication utils
│   ├── database/
│   │   ├── base.py                  # Declarative SQLAlchemy Base
│   │   └── session.py               # SQLAlchemy database session & engine creation
│   ├── models/
│   │   └── product_model.py         # SQLAlchemy database models
│   ├── schemas/
│   │   └── product_schema.py        # Pydantic validation schemas
│   ├── repositories/
│   │   └── product_repository.py    # Database query operations (CRUD)
│   ├── services/
│   │   └── product_service.py       # Core business logic layer
│   ├── utils/
│   │   ├── constants.py             # Reusable constants
│   │   └── helpers.py               # Reusable utility functions
│   ├── dependencies.py              # FastAPI dependency injection functions (e.g. get_db)
│   └── main.py                      # FastAPI App initialization & lifespan setup
├── frontend/
│   └── src/
│       ├── api/
│       │   └── apiClient.js         # Axios API client instance
│       ├── components/
│       │   └── TaglineSection/
│       │       ├── TaglineSection.js  # Tagline React component
│       │       └── TaglineSection.css # Styling for Tagline component
│       ├── styles/
│       │   ├── App.css              # Main App styling
│       │   └── index.css            # Root stylesheet
│       ├── App.js                   # Application root component
│       └── index.js                 # React root mounting script
├── main.py                          # Compatibility bridge to run app (uvicorn main:app)
├── database.py                      # Compatibility bridge for database module
├── database_models.py              # Compatibility bridge for SQLAlchemy models
├── models.py                        # Compatibility bridge for Pydantic schemas
├── .env                             # Local environment configuration file (ignored by Git)
├── .env.example                     # Reference template for environment configuration
└── requirements.txt                 # Backend dependencies list
```

## Technology Stack

* **Backend**: FastAPI, SQLAlchemy ORM, Pydantic, PostgreSQL
* **Frontend**: React (Create React App), Axios, CSS
* **Deployment Compatibility**: Render & Vercel compatible

## Running the Application Locally

### Backend Setup

1. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv myenv
   # On Windows:
   myenv\Scripts\activate
   # On Linux/macOS:
   source myenv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your actual settings (like `DATABASE_URL`):
   ```bash
   cp .env.example .env
   ```

4. **Run the Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```

2. **Install npm dependencies**:
   ```bash
   npm install
   ```

3. **Run the React Dev Server**:
   ```bash
   npm start
   ```
   The application will load at `http://localhost:3000`.
