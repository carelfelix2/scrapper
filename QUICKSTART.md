# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Docker (Recommended)

```bash
# 1. Clone/navigate to project
cd scrapper

# 2. Copy environment variables
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python -c "
from app.core.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Database initialized successfully!')
"

# 5. Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
# Login with: demo@scrapper.com / demo123
```

### Option 2: Local Development

#### Prerequisites
```bash
# Check Python version
python --version  # Should be 3.11+

# Check Node version
node --version   # Should be 18+

# Check PostgreSQL
psql --version   # Should be 15+

# Check Redis
redis-cli --version  # Should be 7+
```

#### Backend Setup
```bash
# 1. Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cd ..
cp .env.example .env

# 4. Initialize database
python backend/main.py
# Wait for server to start, then Ctrl+C

# 5. Run FastAPI
cd backend
python main.py
# API will be at http://localhost:8000
```

#### Workers Setup
```bash
# 1. Create virtual environment
cd workers
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Celery worker
celery -A celery_config worker --loglevel=info
```

#### Frontend Setup
```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Start development server
npm run dev
# Frontend will be at http://localhost:3000
```

## 📊 Using the Application

### 1. Login
- URL: http://localhost:3000/login
- Email: demo@scrapper.com
- Password: demo123

### 2. Create Your First Scraping Task
1. Go to Dashboard
2. Click "Create Task" tab
3. Select Platform: Shopee
4. Select Task Type: Keyword Search
5. Enter Keyword: "iPhone 15"
6. Click "Start Scraping"

### 3. Monitor Tasks
- Go to "Tasks" tab to see task status
- Page auto-refreshes every 5 seconds
- Click task to view details

### 4. View Products
- Dashboard shows scraped products
- Products table shows all data
- Click on product to see details and price history

### 5. Export Data
- Click export button on products table
- Choose CSV or Excel format
- File downloads automatically

## 🔧 Common Tasks

### Reset Database
```bash
# Using Docker
docker-compose down -v
docker-compose up -d

# Local
psql -U scrapper -d scrapper_db -f database/schema.sql
```

### View Logs
```bash
# Backend logs
docker-compose logs -f backend

# Worker logs
docker-compose logs -f celery_worker

# API documentation
http://localhost:8000/api/docs
```

### Stop Services
```bash
# Docker
docker-compose down

# Local: Ctrl+C in each terminal
```

## 📁 Key Files to Know

```
scrapper/
├── .env                    # Configuration (create from .env.example)
├── docker-compose.yml      # Docker setup
├── README.md              # Full documentation
│
├── frontend/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   └── package.json      # Dependencies
│
├── backend/
│   ├── main.py           # FastAPI app
│   ├── celery_app.py     # Task configuration
│   ├── requirements.txt   # Dependencies
│   └── app/
│       ├── models/       # Database models
│       ├── routers/      # API endpoints
│       ├── schemas/      # Data schemas
│       └── services/     # Business logic
│
└── workers/
    ├── scrapers/         # Scraping logic
    ├── celery_config.py  # Celery setup
    └── requirements.txt  # Dependencies
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000
kill -9 <PID>

# Or use different port
FRONTEND_PORT=3001 docker-compose up -d
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection string in .env
# Should be: postgresql://scrapper:password@localhost:5432/scrapper_db
```

### Celery Task Not Running
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Check Celery worker is running
docker-compose logs celery_worker

# Check task broker URL
# Should be: redis://localhost:6379/0
```

### Frontend Shows Blank Page
```bash
# Check API URL
# Open browser console (F12)
# Check network tab for API calls

# In .env:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Learning Resources

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Database
- View schema: `database/schema.sql`
- Query explorer: Use pgAdmin on http://localhost:5050

### Code Examples
- Login endpoint: `backend/app/routers/auth.py`
- Create task: `frontend/components/forms/task-form.tsx`
- Scraper: `workers/scrapers/shopee_scraper.py`

## 🚀 Next Steps

### For Users
1. ✅ Try creating a scraping task
2. ✅ Export scraped data
3. ✅ Set up price alerts
4. ✅ Create collections

### For Developers
1. Read `docs/ARCHITECTURE.md` for system design
2. Read `docs/DEVELOPMENT.md` for development guide
3. Check `backend/app/routers/` for API patterns
4. Check `frontend/components/` for UI patterns

### For Deployment
1. Read `docker-compose.prod.yml` for production setup
2. Configure environment variables
3. Set up SSL certificates
4. Configure domain and DNS
5. Set up monitoring and logging

## 💡 Pro Tips

- Use API documentation at `/api/docs` to test endpoints
- Browser DevTools (F12) for frontend debugging
- Docker logs for troubleshooting: `docker-compose logs -f service-name`
- Redis CLI for cache inspection: `redis-cli keys '*'`
- Database queries: Connect with `psql` client

## ❓ FAQ

**Q: Can I use different platforms?**
A: Yes, modify Dockerfile and add new scraper in `workers/scrapers/`

**Q: How do I add more workers?**
A: Modify `docker-compose.yml` and duplicate celery_worker service

**Q: Can I deploy to AWS/GCP?**
A: Yes, use docker-compose.prod.yml as base and adjust for your platform

**Q: How do I add authentication?**
A: Implement user registration in `backend/app/routers/auth.py`

**Q: How do I monitor performance?**
A: Add monitoring with Prometheus/Grafana or use cloud provider tools

---

**Happy Scraping! 🎉**

For more detailed information, check the [README.md](README.md) and [DEVELOPMENT.md](docs/DEVELOPMENT.md).
