# NotAgenticB2BSaaS

A sprint hackathon project developed for the 2025 Anthropic X Penn Hackathon.

## Overview

A full-stack B2B SaaS application with React frontend and FastAPI backend, designed for AI-powered business solutions.

## Project Structure

```
NotAgenticB2BSaaS/
├── frontend/          # React + MaterialUI frontend
│   ├── src/
│   │   ├── components/
│   │   ├── theme/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
└── README.md
```

## Tech Stack

### Frontend
- **React** - JavaScript UI library
- **Material-UI (MUI)** - Component library with global theming
- **Vite** - Build tool and dev server

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - HTTP client for AI API integrations

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Features

### Frontend
- Global MaterialUI theme with custom styling
- Responsive component structure (NavBar, Main, Footer)
- Clean and modern UI design

### Backend
- RESTful API architecture
- AI service integration structure
- CORS configured for frontend communication
- Ready for AI API integrations (OpenAI, Anthropic, etc.)

## Development

See individual README files in `frontend/` and `backend/` directories for detailed development instructions.

## License

ISC
