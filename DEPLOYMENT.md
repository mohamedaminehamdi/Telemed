# Docker & Deployment Guide

## Overview

This guide covers containerization and deployment of the Telemed telemedicine platform using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4GB RAM minimum
- 2GB free disk space

## Local Development with Docker

### 1. Build and Start Containers

```bash
# Clone the repository
git clone https://github.com/yourusername/telemed.git
cd telemed

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Access Services

- **Backend API**: http://localhost:8000/api/v1/
- **Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/api/v1/docs/
- **Swagger UI**: http://localhost:8000/api/swagger/
- **Database**: localhost:5432 (PostgreSQL)
- **Cache**: localhost:6379 (Redis)

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser (admin account)
docker-compose exec backend python manage.py createsuperuser

# Load sample data (optional)
docker-compose exec backend python manage.py loaddata fixtures/sample_data.json
```

### 4. Common Commands

```bash
# View running containers
docker-compose ps

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Execute command in container
docker-compose exec backend python manage.py shell
docker-compose exec frontend npm run test

# Rebuild images
docker-compose build

# Remove all containers and volumes
docker-compose down -v

# Restart services
docker-compose restart
```

## Services

### Backend (Django)

**Container**: `telemed-backend`
**Port**: 8000
**Image**: Built from `backend/Dockerfile`

Features:
- Django REST Framework API
- PostgreSQL database
- Redis caching
- JWT authentication
- Gunicorn WSGI server

Environment Variables:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,backend
DATABASE_URL=postgresql://postgres:postgres@db:5432/telemed
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
JWT_SECRET_KEY=jwt-secret-key
```

### Frontend (Vue 3)

**Container**: `telemed-frontend`
**Port**: 5173
**Image**: Built from `frontend/Dockerfile`

Features:
- Vue 3 with Vite
- Pinia state management
- Axios HTTP client
- Responsive design system

Environment Variables:
```
VITE_APP_API_URL=http://backend:8000/api/v1
VITE_APP_JITSI_URL=https://meet.jitsi
```

### Database (PostgreSQL)

**Container**: `telemed-db`
**Port**: 5432
**Image**: postgres:15-alpine
**Volume**: postgres_data

Configuration:
```
POSTGRES_DB=telemed
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Cache (Redis)

**Container**: `telemed-redis`
**Port**: 6379
**Image**: redis:7-alpine
**Volume**: redis_data

## Production Deployment

### 1. Environment Configuration

Create `.env.production`:
```bash
DEBUG=False
SECRET_KEY=your-very-secure-random-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db-server:5432/telemed_prod
POSTGRES_PASSWORD=very-secure-password
REDIS_URL=redis://redis-server:6379/0
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Build Production Images

```bash
# Backend
docker build -t telemed-backend:latest ./backend
docker build -t telemed-frontend:latest ./frontend

# Tag for registry
docker tag telemed-backend:latest your-registry/telemed-backend:latest
docker tag telemed-frontend:latest your-registry/telemed-frontend:latest

# Push to registry
docker push your-registry/telemed-backend:latest
docker push your-registry/telemed-frontend:latest
```

### 3. Deploy to Production

#### Option A: Docker Compose on VPS

```bash
# SSH into server
ssh user@your-server

# Clone repo
git clone https://github.com/yourusername/telemed.git
cd telemed

# Create .env.production
nano .env.production  # Add environment variables

# Start services with production compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify health
curl http://localhost:8000/api/v1/health/
```

#### Option B: Kubernetes Deployment

Use the provided Kubernetes manifests:
```bash
# Create namespace
kubectl create namespace telemed

# Create secrets
kubectl create secret generic telemed-secrets \
  --from-file=.env.production \
  -n telemed

# Deploy
kubectl apply -f k8s/backend-deployment.yaml -n telemed
kubectl apply -f k8s/frontend-deployment.yaml -n telemed
kubectl apply -f k8s/postgres-statefulset.yaml -n telemed
kubectl apply -f k8s/redis-deployment.yaml -n telemed
kubectl apply -f k8s/ingress.yaml -n telemed

# Check status
kubectl get pods -n telemed
kubectl get services -n telemed
```

### 4. Database Backup & Restore

```bash
# Backup database
docker-compose exec -T db pg_dump -U postgres telemed > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres telemed < backup.sql

# Backup volumes
docker run --rm -v telemed_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data

# List backups
aws s3 ls s3://your-backup-bucket/telemed/
```

## Health Checks

Each service includes health checks:

```bash
# Check backend health
curl http://localhost:8000/api/v1/health/

# Check frontend
curl http://localhost:5173

# Check database
docker-compose exec db pg_isready -U postgres

# Check Redis
docker-compose exec redis redis-cli ping

# View health status
docker-compose ps
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend service to 3 instances
docker-compose up -d --scale backend=3

# Use load balancer (nginx, HAProxy) to distribute traffic
```

### Resource Limits

Add to `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Monitoring & Logging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Since last 1 hour
docker-compose logs --since=1h backend
```

### Monitoring Tools

Install monitoring stack:
```bash
# Prometheus for metrics
docker pull prom/prometheus

# Grafana for dashboards
docker pull grafana/grafana

# ELK Stack for logs
# - Elasticsearch
# - Logstash
# - Kibana
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check resource constraints
docker stats

# Rebuild image
docker-compose build --no-cache backend

# Check environment variables
docker-compose exec backend printenv
```

### Database Connection Issues

```bash
# Test connection
docker-compose exec backend python manage.py dbshell

# Check database status
docker-compose exec db pg_isready

# Reset database
docker-compose exec backend python manage.py migrate --reset
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Verify API connectivity
docker-compose exec frontend curl http://backend:8000/api/v1/

# Rebuild frontend
docker-compose build --no-cache frontend
```

## Security Best Practices

1. **Change Default Passwords**
   - PostgreSQL default password
   - Django secret key
   - JWT secret key

2. **Use Environment Variables**
   - Never commit secrets to git
   - Use `.env` files locally
   - Use Docker secrets in production

3. **Enable HTTPS**
   - Use Let's Encrypt with Certbot
   - Configure nginx reverse proxy
   - Update CORS_ALLOWED_ORIGINS

4. **Database Security**
   - Use strong passwords
   - Limit database access
   - Regular backups
   - Enable audit logging

5. **API Security**
   - Enable CSRF protection
   - Use rate limiting
   - Implement API key authentication
   - Monitor for suspicious activity

## Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Complete cleanup (careful!)
docker-compose down -v

# Remove all Telemed images
docker rmi telemed-backend telemed-frontend
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Vue.js Production Deployment](https://vitejs.dev/guide/ssr.html)

---

**Last Updated**: March 19, 2026
**Version**: 1.0
