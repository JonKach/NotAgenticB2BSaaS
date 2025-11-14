# Backend

FastAPI-based backend for NotAgenticB2BSaaS with AI API integration capabilities.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - HTTP client for AI API calls

## Features

- RESTful API endpoints
- CORS configuration for frontend communication
- AI service integration structure
- Environment-based configuration
- Ready for AI API integrations (OpenAI, Anthropic, Google, etc.)

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Development

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

- Swagger documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── routers/
│   │   └── ai_router.py
│   ├── services/
│   │   └── ai_service.py
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### AI Endpoints
- `POST /api/ai/generate` - Generate AI response
- `GET /api/ai/models` - List available AI models
- `GET /api/ai/status` - Check AI service status

## Adding AI API Integrations

The `AIService` class in `app/services/ai_service.py` is designed to handle AI API calls. To integrate with specific AI providers:

1. Add your API key to `.env`
2. Implement the API call in `ai_service.py`
3. Use the service methods in your routers

Example providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
