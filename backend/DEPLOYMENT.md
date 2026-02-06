# Deployment Configuration for Production

## Environment Variables

The following environment variables must be configured for production deployment:

```bash
# Database Configuration
NEON_DATABASE_URL=your-neon-postgres-connection-string
DATABASE_URL=your-primary-database-connection-string

# Authentication Configuration
BETTER_AUTH_SECRET=your-super-secure-random-secret-string-here
BETTER_AUTH_URL=https://your-frontend-domain.com

# Application Configuration
APP_ENV=production
LOG_LEVEL=warning

# Security Configuration
ALLOWED_HOSTS=your-api-domain.com,www.your-api-domain.com
TRUSTED_PROXIES=1
```

## Docker Production Setup

### Dockerfile for Production
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    gunicorn \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application with gunicorn for production
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
```

### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NEON_DATABASE_URL=${NEON_DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - BETTER_AUTH_URL=${BETTER_AUTH_URL}
      - APP_ENV=production
      - LOG_LEVEL=info
    env_file:
      - .env.production
    volumes:
      - /app/static:/app/static
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_DB=todoapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - todoapp_postgres_data:/var/lib/postgresql/data
    environment:
      - PGDATA=/var/lib/postgresql/data/pgdata
    security_opt:
      - no-new-privileges:true

volumes:
  todoapp_postgres_data:
```

## Kubernetes Deployment (Optional)

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskmaster-backend
  labels:
    app: taskmaster-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: taskmaster-backend
  template:
    metadata:
      labels:
        app: taskmaster-backend
    spec:
      containers:
      - name: backend
        image: your-registry/taskmaster-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          value: "production"
        - name: LOG_LEVEL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: log-level
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: better-auth-secret
        - name: NEON_DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: neon-db-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: taskmaster-backend-service
spec:
  selector:
    app: taskmaster-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Security Hardening

### 1. SSL/TLS Configuration
- Ensure all production traffic is served over HTTPS
- Use TLS 1.3 where possible
- Implement HSTS headers

### 2. Database Security
- Use strong passwords for database access
- Enable SSL connections to database
- Regularly rotate database credentials

### 3. API Security
- Implement rate limiting at the infrastructure level
- Use a Web Application Firewall (WAF)
- Monitor for suspicious activities

## Monitoring and Logging

### Production Logging
- Centralized logging using ELK stack or similar
- Structured logging in JSON format
- Log aggregation and alerting

### Health Checks
The application provides health check endpoints:
- `GET /health` - General health status
- `GET /ready` - Readiness for traffic
- `GET /live` - Liveness probe

## Backup and Recovery

### Database Backups
- Automated daily backups of PostgreSQL database
- Point-in-time recovery capability
- Off-site backup storage

### Application Backups
- Version-controlled source code
- Infrastructure as code (IaC) configurations
- Environment variable backups

## Performance Tuning

### Database Optimization
- Connection pooling configuration
- Query optimization and indexing
- Regular maintenance tasks

### Application Scaling
- Horizontal pod/container scaling
- Load balancing configuration
- CDN for static assets

## Deployment Steps

1. **Prepare Environment**
   - Set up production environment variables
   - Configure domain and SSL certificates

2. **Database Setup**
   - Create production database
   - Run initial schema migrations

3. **Deploy Application**
   - Build production Docker image
   - Deploy to production environment
   - Verify health checks pass

4. **Post-Deployment**
   - Monitor application performance
   - Verify all endpoints are functioning
   - Set up monitoring and alerting

## Rollback Plan

In case of deployment issues:
1. Monitor health checks and error rates
2. Roll back to previous stable version if needed
3. Restore from database backup if required
4. Communicate with stakeholders

## Maintenance Schedule

- Weekly security updates
- Monthly performance reviews
- Quarterly disaster recovery tests
- Regular dependency updates