# AI Q&A Application

A full-stack application that enables users to ask questions and receive AI-powered responses, featuring a React frontend and FastAPI backend with SQLite database for conversation history.

## Features

### Core Features

- AI-powered question answering with automatic retries
- Persistent conversation history with SQLite
- Clean, responsive UI with loading states
- Rate limiting (5 requests/minute per IP)
- Paginated history view
- Error handling with user-friendly messages

### Technical Stack

- Frontend: React + Vite
- Backend: FastAPI + SQLite
- AI: Hugging Face API
- Async support with aiohttp
- CORS enabled for development

## Quick Start

### Backend Setup

1. Clone and navigate to project:

```bash
git clone <repository-url>
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install fastapi uvicorn python-dotenv aiohttp slowapi
```

4. Create .env file:

```bash
# backend/.env
HUGGINGFACE_API_KEY=your_huggingface_token_here
```

5. Initialize database:

```bash
python -c "from app.database import init_db; init_db()"
```

6. Start backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm run dev
```

## API Reference

### Authentication

No authentication required for development. Rate limiting applied per IP.

### Endpoints

#### Ask Question

```bash
POST http://localhost:8000/ask
Content-Type: application/json

{
    "question": "What is FastAPI?"
}
```

#### Get History

```bash
GET http://localhost:8000/history?page=1&page_size=10
```

#### Health Check

```bash
GET http://localhost:8000/health
```

## Development Commands

### Backend Commands

```bash
# Start server
uvicorn app.main:app --reload

# Run with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Reset database
rm backend/qa_history.db
python -c "from app.database import init_db; init_db()"
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new dependency
npm install package-name
```

## Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # Database models
│   │   ├── database.py      # DB configuration
│   │   └── ai_service.py    # AI integration
│   ├── .env                 # Environment variables
│   └── qa_history.db        # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   ├── App.css         # Styles
│   │   └── components/     # React components
│   ├── public/
│   └── index.html
```

## Common Issues & Solutions

### Backend Issues

1. Database Errors:

```bash
# Reset database
rm backend/qa_history.db
python -c "from app.database import init_db; init_db()"
```

2. CORS Issues:

```python
# Check in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. AI Model Loading:

- Application automatically retries with backoff
- Check Hugging Face API key in .env

### Frontend Issues

1. Connection Errors:

```bash
# Verify backend URL in App.jsx
const API_URL = 'http://localhost:8000'
```

2. Build Issues:

```bash
# Clean install
rm -rf node_modules
npm install
```

## Environment Variables

### Backend (.env)

```
HUGGINGFACE_API_KEY=your_api_key_here
```

### Frontend (optional)

```
VITE_API_URL=http://localhost:8000
```

## Database Schema

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - feel free to use this project for learning and development.
