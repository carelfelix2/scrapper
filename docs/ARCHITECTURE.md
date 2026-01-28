# Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                           │
│              (Next.js Frontend - Port 3000)                │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────────────────────┐
│              API Gateway / Reverse Proxy                    │
│                    (nginx optional)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┴─────────────┐
    │                          │
┌───▼─────────────────┐  ┌────▼──────────────────┐
│   FastAPI Backend   │  │  Task Queue Message  │
│   (Port 8000)       │  │  Broker - Redis      │
│                     │  │  (Port 6379)         │
│ • Authentication    │  └────┬──────────────────┘
│ • API Routes        │       │
│ • Business Logic    │       │
│ • Database ORM      │       │
└──────┬──────────────┘       │
       │                      │
       │ SQL Queries      ┌───▼──────────────────┐
       │                  │  Celery Workers      │
       │                  │                      │
       │                  │ • Shopee Scraper     │
       │                  │ • TikTok Scraper     │
       │                  │ • Background Tasks   │
       │                  └────────┬─────────────┘
       │                           │
┌──────▼──────────────────────────▼──────────────────────┐
│          PostgreSQL Database (Port 5432)              │
│                                                        │
│  Tables:                                              │
│  • users                • scraping_tasks             │
│  • products             • price_history              │
│  • collections          • alerts                     │
│  • api_keys             • audit_logs                │
└────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Scraping Task Flow
```
User creates task → API validates → Task stored in DB
    → Celery task created → Worker fetches task
    → Playwright browser launched → Website scraped
    → Data processed and saved → Database updated
    → Frontend polls for status → Results displayed
```

### 2. Product Data Flow
```
Raw scraped data → Validation → Transform to schema
    → Deduplicate (platform + external_id) → Store in DB
    → Create price history snapshot → Update statistics
    → Trigger alerts if applicable → Notify user
```

## Authentication Flow

```
User submits credentials → Backend validates → JWT token created
    → Token stored in localStorage → Token sent with each request
    → Backend validates token → Grant access to protected routes
    → Token refresh before expiry → User stays logged in
```

## Scraping Process

```
Task initiated with platform & keyword/URL
    ↓
Browser context created with random user-agent
    ↓
Random proxy selected (if configured)
    ↓
Anti-bot detection scripts injected
    ↓
Page loaded and waited for content
    ↓
Product selectors queried and parsed
    ↓
Data extracted and normalized
    ↓
Duplicates checked using unique constraint
    ↓
Results stored in database with task_id
    ↓
Price history snapshot created
    ↓
Task marked as completed/failed
```

## Performance Considerations

### Database Optimization
- **Indexes on frequently queried columns**: user_id, platform, status
- **JSONB queries**: Efficient for flexible data structures
- **Connection pooling**: Manage multiple concurrent connections
- **Read replicas**: Offload analytics queries

### Celery Optimization
- **Task prefetching**: Worker grabs one task at a time
- **Task timeouts**: Prevent hanging tasks
- **Result backend expiry**: Clean old task results
- **Task routing**: Send tasks to specific workers

### Frontend Optimization
- **Code splitting**: Load pages on demand
- **API caching**: Store recent requests
- **Pagination**: Limit data per request
- **Lazy loading**: Load images/data when visible

## Scalability Strategy

### Horizontal Scaling
1. **Multiple FastAPI instances** behind load balancer
2. **Multiple Celery workers** for task processing
3. **Redis cluster** for cache/broker redundancy
4. **PostgreSQL read replicas** for analytics

### Vertical Scaling
1. Increase database connection pool
2. Increase worker memory for browser processes
3. Increase API server resources
4. Optimize database queries

## Error Handling

### Task Failures
- Retry with exponential backoff
- Log detailed error messages
- Update task status to "failed"
- Notify user with error details

### Database Failures
- Connection pooling with auto-retry
- Fallback to read replicas
- Circuit breaker pattern
- Health checks

### API Errors
- Validation errors: 400 Bad Request
- Auth errors: 401 Unauthorized
- Permission errors: 403 Forbidden
- Not found: 404
- Server errors: 500+ with logging

## Security Architecture

### Authentication
- JWT tokens with expiry
- Refresh token rotation
- Secure token storage (httpOnly cookies)

### Authorization
- Role-based access control (RBAC)
- User-scoped data isolation
- API key validation

### Data Protection
- HTTPS/TLS encryption
- Database encryption at rest
- Sensitive data masking in logs
- Input validation and sanitization

---

For detailed implementation, refer to individual component documentation.
