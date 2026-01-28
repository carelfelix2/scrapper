# Development Guide

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Step 1: Clone Repository
```bash
git clone <repo-url>
cd scrapper
```

### Step 2: Backend Setup

#### Using Docker (Recommended)
```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait for services to start
sleep 5

# Create database
docker-compose exec postgres createdb -U scrapper scrapper_db

# Import schema
docker-compose exec postgres psql -U scrapper -d scrapper_db < database/schema.sql
```

#### Local Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your local database credentials

# Initialize database
psql -U scrapper -d scrapper_db -f database/schema.sql

# Run migrations (if using Alembic)
alembic upgrade head
```

#### Start Backend
```bash
cd backend
python main.py
# API will be available at http://localhost:8000
```

### Step 3: Workers Setup

```bash
cd workers

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Celery worker
celery -A celery_config worker --loglevel=info
```

### Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend will be available at http://localhost:3000
```

## Project Structure Details

### Backend Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── celery_app.py          # Celery configuration
├── requirements.txt       # Python dependencies
├── app/
│   ├── core/
│   │   ├── config.py      # Settings from environment
│   │   ├── database.py    # SQLAlchemy setup
│   │   └── security.py    # JWT and auth utilities
│   ├── models/
│   │   └── models.py      # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py     # Pydantic request/response schemas
│   ├── routers/
│   │   ├── auth.py        # /api/v1/auth routes
│   │   ├── tasks.py       # /api/v1/tasks routes
│   │   └── products.py    # /api/v1/products routes
│   ├── services/
│   │   └── scraping_service.py  # Business logic
│   └── middleware/
│       └── (custom middleware)
└── tests/
    └── (test files)
```

### Workers Structure
```
workers/
├── celery_config.py       # Celery app configuration
├── requirements.txt       # Python dependencies
├── scrapers/
│   ├── base_scraper.py    # Base class with Playwright setup
│   ├── shopee_scraper.py  # Shopee-specific implementation
│   ├── tiktok_scraper.py  # TikTok-specific implementation
│   └── tokopedia_scraper.py
└── utils/
    ├── proxy_manager.py   # Proxy rotation
    └── user_agent.py      # User-agent management
```

### Frontend Structure
```
frontend/
├── app/
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   ├── login/
│   │   └── page.tsx       # Login page
│   └── dashboard/
│       ├── layout.tsx     # Dashboard layout
│       └── page.tsx       # Dashboard page
├── components/
│   ├── ui/                # Shadcn UI components
│   ├── layout/            # Header, sidebar
│   ├── forms/             # Task form
│   ├── tasks/             # Tasks list
│   ├── products/          # Products table
│   └── analytics/         # Charts and graphs
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities
├── store/                 # Zustand stores
├── types/                 # TypeScript types
└── styles/                # CSS files
```

## Database Management

### Migrations with Alembic

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Manual Schema Updates
```bash
# Connect to database
psql -U scrapper -d scrapper_db

# Run SQL file
\i database/schema.sql

# View tables
\dt

# Describe table
\d products
```

## API Development

### Adding a New Endpoint

1. **Create router file** (`backend/app/routers/new_feature.py`):
```python
from fastapi import APIRouter, Depends
from app.core.database import get_db

router = APIRouter(prefix="/api/v1/new-feature", tags=["New Feature"])

@router.get("/")
async def list_items(db = Depends(get_db)):
    # Implementation
    pass
```

2. **Add schema** (`backend/app/schemas/schemas.py`):
```python
from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
```

3. **Add service** (`backend/app/services/new_service.py`):
```python
class ItemService:
    @staticmethod
    def get_items(db):
        # Business logic
        pass
```

4. **Include router** in `main.py`:
```python
from app.routers import new_feature
app.include_router(new_feature.router)
```

## Frontend Development

### Adding a New Component

1. **Create component file** (`frontend/components/feature/item.tsx`):
```typescript
"use client"

export function Item() {
  return (
    <div>Item Component</div>
  )
}
```

2. **Add TypeScript types** (`frontend/types/index.ts`):
```typescript
export interface Item {
  id: number
  name: string
}
```

3. **Create custom hook** (`frontend/hooks/useItem.ts`):
```typescript
export const useItem = () => {
  // Hook logic
}
```

## Testing

### Backend Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest backend/tests/

# With coverage
pytest --cov=app backend/tests/
```

### Frontend Testing
```bash
# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# With coverage
npm test -- --coverage
```

## Debugging

### Backend
```bash
# Enable debug mode in .env
FASTAPI_DEBUG=true

# Debug with VS Code
# Add breakpoint and use Python debugger
# Or use: python -m pdb main.py
```

### Frontend
```bash
# Use browser DevTools
# F12 -> Console tab
# Or add console.log statements

# Use React DevTools browser extension
```

### Database
```bash
# Enable query logging in .env
# Or check logs: docker-compose logs postgres
```

## Common Commands

### Docker
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f celery_worker

# Stop services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Database
```bash
# Backup
pg_dump -U scrapper scrapper_db > backup.sql

# Restore
psql -U scrapper scrapper_db < backup.sql

# Connect
psql -U scrapper -d scrapper_db
```

### Redis
```bash
# Connect
redis-cli

# Monitor commands
monitor

# Check keys
keys *

# Clear database
flushdb
```

## Best Practices

### Code Quality
- Follow PEP 8 (Python)
- Follow ESLint config (JavaScript/TypeScript)
- Use type hints (Python) and TypeScript
- Write docstrings/comments for complex logic
- Keep functions small and focused

### Performance
- Use database indexes effectively
- Implement caching for frequently accessed data
- Use async/await for I/O operations
- Optimize database queries (explain analyze)
- Monitor and profile bottlenecks

### Security
- Never commit secrets to version control
- Validate all user inputs
- Use parameterized queries
- Implement rate limiting
- Regular security audits

## Environment Variables Reference

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# FastAPI
FASTAPI_ENV=development
FASTAPI_DEBUG=true
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Scraping
PLAYWRIGHT_HEADLESS=true
BROWSER_TIMEOUT=30000
PROXY_LIST=proxy1,proxy2
```

---

For more details on specific components, see their individual documentation files.
