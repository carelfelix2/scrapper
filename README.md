# Scrapper - Web Scraping SaaS Platform

A comprehensive web scraping platform for Indonesian e-commerce and social commerce, featuring real-time tracking of trending products, price movements, and market insights.

## 🎯 Overview

Scrapper is a production-ready SaaS platform built with:
- **Frontend**: Next.js 14+ with Tailwind CSS and Shadcn UI
- **Backend**: FastAPI with async support
- **Scraping**: Playwright with proxy rotation and user-agent switching
- **Database**: PostgreSQL with JSONB support
- **Task Queue**: Redis + Celery for background jobs

### Target Platforms
- Shopee Indonesia
- Tokopedia
- TikTok Shop

## 📁 Project Structure

```
scrapper/
├── frontend/               # Next.js application
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utility functions
│   ├── store/            # Zustand stores
│   ├── styles/           # Global CSS
│   └── types/            # TypeScript types
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── core/        # Config, database, security
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   └── middleware/  # Custom middleware
│   ├── main.py          # FastAPI app entry point
│   └── celery_app.py    # Celery configuration
├── workers/             # Background job workers
│   ├── scrapers/        # Scraper implementations
│   │   ├── base_scraper.py
│   │   ├── shopee_scraper.py
│   │   └── tiktok_scraper.py
│   ├── utils/           # Helper utilities
│   └── celery_config.py
├── database/            # Database migrations
│   └── schema.sql       # PostgreSQL schema
├── docker-compose.yml   # Container orchestration
└── README.md           # This file
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Quick Start with Docker

1. **Clone and setup environment**
   ```bash
   cd scrapper
   cp .env.example .env
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize database**
   ```bash
   docker-compose exec backend psql -U scrapper -d scrapper_db -f /schema.sql
   ```

4. **Access services**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Workers Setup

```bash
cd workers
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
celery -A tasks worker --loglevel=info
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🔐 Authentication

### Demo Credentials
- **Email**: demo@scrapper.com
- **Password**: demo123

## 📚 API Documentation

### Authentication Endpoints

#### Login
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
```

#### Get Current User
```bash
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>
```

### Scraping Task Endpoints

#### Create Scraping Task
```bash
POST /api/v1/tasks
Headers: Authorization: Bearer <token>
{
  "platform": "shopee",
  "task_type": "keyword_search",
  "input_data": {
    "keyword": "iPhone 15"
  }
}
```

#### Get Task Status
```bash
GET /api/v1/tasks/{task_id}
Headers: Authorization: Bearer <token>
```

#### List Tasks
```bash
GET /api/v1/tasks?skip=0&limit=10
Headers: Authorization: Bearer <token>
```

### Products Endpoints

#### List Products
```bash
GET /api/v1/products?platform=shopee&skip=0&limit=20
Headers: Authorization: Bearer <token>
```

#### Get Product Details
```bash
GET /api/v1/products/{product_id}
Headers: Authorization: Bearer <token>
```

#### Get Price History
```bash
GET /api/v1/products/{product_id}/history?limit=50
Headers: Authorization: Bearer <token>
```

#### Search Products
```bash
GET /api/v1/products/search/{query}?skip=0&limit=20
Headers: Authorization: Bearer <token>
```

## 🗄️ Database Schema

### Key Tables

#### Users
- User account and authentication data
- Subscription management
- API keys and tokens

#### ScrapingTasks
- Scraping job records
- Status tracking
- Celery task ID mapping
- Input parameters and results

#### Products
- Scraped product data
- Platform-specific information
- Status and categorization
- Links to scraping tasks

#### PriceHistory
- Historical price tracking
- Discount and rating changes
- Timestamped snapshots

#### Collections
- User's watchlists and collections
- Product grouping
- Public/private access

#### Alerts
- Price drop alerts
- Stock availability alerts
- Custom threshold monitoring

## 🛠️ Key Features

### 1. Dashboard
- Real-time task monitoring
- Product statistics
- Quick access to all features
- Dark mode interface

### 2. Scraper Management
- URL scraping
- Keyword search
- Shop monitoring
- Task scheduling

### 3. Data Table
- Sortable columns
- Filterable results
- Pagination support
- Export functionality

### 4. Analytics
- Price trend charts
- Platform distribution
- Rating analysis
- Sold count tracking

### 5. Export System
- CSV export
- Excel export
- Custom date ranges
- Filtered exports

## 📊 Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Shadcn UI
- **Icons**: Lucide React
- **Charts**: Recharts
- **State Management**: Zustand
- **API Client**: Axios

### Backend
- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Cache**: Redis
- **Auth**: JWT with python-jose

### Scraping
- **Browser Automation**: Playwright
- **Proxy Management**: Custom rotation
- **User-Agent Switching**: Random selection
- **Stealth Scripts**: Anti-detection measures

## 🔧 Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/scrapper_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key

# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Scraping
PLAYWRIGHT_HEADLESS=true
BROWSER_TIMEOUT=30000
PROXY_LIST=http://proxy1.com,http://proxy2.com
```

## 📈 Scaling Considerations

### Database
- Use read replicas for analytics queries
- Implement connection pooling
- Regular index maintenance
- Archive old data periodically

### Workers
- Scale Celery workers horizontally
- Implement rate limiting per IP
- Use task priorities
- Monitor queue depth

### Frontend
- Deploy to CDN
- Implement caching headers
- Optimize bundle size
- Use lazy loading

## 🔒 Security Best Practices

- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use environment variables for secrets
- Regular security audits
- Monitor API access logs
- Implement CORS properly
- Use secure database connections

## 🧪 Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

## 📝 API Rate Limiting

- Standard: 1000 requests/hour
- Premium: 10000 requests/hour
- Enterprise: Unlimited

## 🐛 Troubleshooting

### Celery Tasks Not Running
1. Check Redis connection: `redis-cli ping`
2. Check Celery worker logs: `docker-compose logs celery_worker`
3. Verify database connection

### Database Connection Issues
1. Check PostgreSQL running: `docker-compose ps postgres`
2. Verify credentials in `.env`
3. Check network connectivity

### Scraping Failures
1. Verify proxy configuration
2. Check browser timeout settings
3. Review scraper logs for specific errors

## 📦 Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Configure HTTPS/TLS
- [ ] Setup proper logging
- [ ] Configure backups
- [ ] Setup monitoring
- [ ] Configure rate limiting
- [ ] Setup error tracking (Sentry)
- [ ] Configure email notifications

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📄 License

Proprietary - All rights reserved

## 👥 Support

For support, contact: support@scrapper.com

## 🗺️ Roadmap

- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Machine learning insights
- [ ] API webhooks
- [ ] Custom scraping rules
- [ ] Scheduled scraping
- [ ] Price prediction
- [ ] Competitor analysis

---

**Version**: 0.1.0  
**Last Updated**: January 2024
