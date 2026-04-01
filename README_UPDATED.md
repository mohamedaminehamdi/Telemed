# Telemed - Comprehensive Telemedicine Platform

A full-stack telemedicine application built with Django REST Framework, Vue 3, and modern DevOps practices. Enables patients to book appointments, have video consultations, and manage prescriptions with licensed healthcare providers.

## 🎯 Features

### Core Features
- **Patient Portal**
  - Browse and search doctors by specialization
  - Book, reschedule, and cancel appointments
  - Video consultations with integrated chat
  - View consultation history and notes
  - Manage prescriptions and refill requests
  - Personal health records

- **Doctor Dashboard**
  - Manage appointment schedule
  - Conduct secure video consultations
  - Create and manage patient prescriptions
  - Track patient interactions and history
  - Generate prescription exports (PDF, HL7)
  - Respond to prescription refill requests

- **Video Consultations**
  - Real-time video communication (Jitsi integration)
  - Built-in chat during consultations
  - Screen sharing capabilities
  - Session recording with consent
  - Automatic session cleanup
  - Pre-call device checks

- **Prescription Management**
  - Digital prescription creation
  - Dosage and frequency tracking
  - Refill request handling
  - Drug interaction checking
  - PDF and HL7 format export
  - Prescription history

- **Authentication & Security**
  - JWT-based authentication
  - Role-based access control (RBAC)
  - Patient and Doctor role separation
  - Password hashing and validation
  - Secure API endpoints

## 🏗️ Architecture

### Frontend Stack
```
Vue 3 (Composition API)
├── Vite Build Tool
├── Pinia State Management
├── Vue Router Navigation
├── Axios HTTP Client
├── TailwindCSS Styling
└── Vitest Testing Framework
```

### Backend Stack
```
Django 3.x
├── Django REST Framework
├── PostgreSQL Database
├── Redis Caching
├── JWT Authentication
├── Celery Task Queue (optional)
└── Gunicorn WSGI Server
```

### DevOps & Deployment
```
Docker & Docker Compose
├── Multi-stage builds
├── Health checks
├── Volume management
└── Production-ready configuration

Kubernetes (Optional)
├── Deployment manifests
├── Service definitions
├── Ingress configuration
└── StatefulSets for databases
```

## 📊 Project Structure

```
telemed/
├── backend/
│   ├── apps/
│   │   ├── api/              # API endpoints & serializers
│   │   ├── users/            # User models & management
│   │   ├── appointments/     # Appointment logic
│   │   ├── consultations/    # Video consultation views
│   │   └── prescriptions/    # Prescription management
│   ├── config/               # Django settings
│   ├── utils/                # Shared utilities
│   ├── tests/                # Test suite (pytest)
│   ├── Dockerfile            # Docker image definition
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   │   └── shared/       # Reusable components
│   │   ├── stores/           # Pinia state stores
│   │   ├── composables/      # Vue composition hooks
│   │   ├── services/         # API service layer
│   │   ├── utils/            # Helper utilities
│   │   ├── assets/           # Images, fonts
│   │   ├── styles/           # CSS/SCSS
│   │   ├── router/           # Vue Router config
│   │   ├── views/            # Page components
│   │   └── App.vue           # Root component
│   ├── tests/                # Test suite (Vitest)
│   ├── public/               # Static assets
│   ├── package.json          # NPM dependencies
│   ├── vitest.config.js      # Test configuration
│   ├── Dockerfile            # Docker image definition
│   └── TEST_README.md        # Testing guide
│
├── docker-compose.yml        # Multi-service orchestration
├── DEPLOYMENT.md             # Deployment guide
├── .env.example              # Environment variables template
├── .dockerignore              # Docker build exclusions
└── README.md                 # This file
```

## 🚀 Quick Start

### Local Development with Docker

```bash
# Clone repository
git clone https://github.com/yourusername/telemed.git
cd telemed

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Access applications
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api/v1
# Admin: http://localhost:8000/admin
```

### Local Development without Docker

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/telemed

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build
```

## 📖 Documentation

- **[API Documentation](./backend/API_DOCUMENTATION.md)** - REST API endpoints and examples
- **[Testing Guide](./frontend/TEST_README.md)** - Frontend testing with Vitest
- **[Deployment Guide](./DEPLOYMENT.md)** - Docker, Kubernetes, and production deployment
- **[Design System](./frontend/src/DESIGN_SYSTEM.md)** - Vue component library and design tokens
- **[Contributing Guide](./CONTRIBUTING.md)** - Development workflow and guidelines

## 🔐 Security Features

- ✅ **JWT Authentication** - Stateless token-based authentication
- ✅ **Role-Based Access Control** - Separate Patient and Doctor permissions
- ✅ **CORS Protection** - Cross-origin request whitelisting
- ✅ **CSRF Protection** - Cross-site request forgery prevention
- ✅ **Password Hashing** - Bcrypt password hashing
- ✅ **Secure Headers** - Security headers in HTTP responses
- ✅ **Rate Limiting** - API rate limiting per endpoint
- ✅ **Input Validation** - Server-side input validation
- ✅ **SQL Injection Protection** - Parameterized queries with ORM
- ✅ **XSS Protection** - Content Security Policy headers

## 📱 User Roles & Permissions

### Patient
- Browse doctors and specializations
- Book and manage appointments
- Join video consultations
- View and manage prescriptions
- Request prescription refills
- View medical history

### Doctor
- Manage appointment schedule
- Conduct video consultations
- Create prescriptions
- Manage patient records
- Accept/deny refill requests
- Export prescriptions

### Admin
- Full system access
- User management
- Content moderation
- System configuration
- Report generation

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest tests/test_api.py

# Run in watch mode
pytest-watch
```

### Frontend Tests
```bash
cd frontend

# Run all tests
npm run test

# Run in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage

# Run specific test
npm run test -- components.spec.js
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## 🔧 Configuration

### Environment Variables
See `.env.example` for all available configuration options.

Key variables:
- `DEBUG` - Django debug mode (False in production)
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis cache connection
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ALLOWED_ORIGINS` - Allowed CORS origins
- `JITSI_SERVER_URL` - Jitsi Meet server URL

## 📊 System Requirements

### Minimum
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM
- 1GB disk space

### Recommended for Production
- 4+ GB RAM
- 20GB disk space
- PostgreSQL 12+ (managed separately)
- Redis 6+ (managed separately)
- SSL/TLS certificates

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Create feature branch from `main`
2. Make changes and write tests
3. Ensure all tests pass
4. Submit pull request with description
5. Code review and approval
6. Merge to `main`

## 📈 Performance Optimization

- **Caching**: Redis caching for frequently accessed data
- **Database**: Indexed queries and connection pooling
- **Frontend**: Code splitting, lazy loading, image optimization
- **API**: Pagination, filtering, select_related for queries
- **CDN**: Static files served from CDN in production

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**
```bash
# Check logs
docker-compose logs backend

# Verify database is running
docker-compose exec db pg_isready

# Reset database
docker-compose exec backend python manage.py migrate --reset
```

**Frontend won't load**
```bash
# Check logs
docker-compose logs frontend

# Verify API connectivity
docker-compose exec frontend curl http://backend:8000/api/v1/

# Clear node_modules and reinstall
rm -rf frontend/node_modules
docker-compose exec frontend npm install
```

**Video consultation not working**
- Verify Jitsi server URL in environment variables
- Check browser console for errors
- Ensure cameras/microphones have permissions

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@telemed.com
- **Documentation**: Full docs at `/docs`

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- **Lead Developer**: Mohamed Amine Hamdi
- **Architecture**: Full-stack telemedicine platform
- **Last Updated**: March 2026

## 🚧 Roadmap

### Q2 2026
- [ ] Blockchain-based medical records
- [ ] AI-powered symptom checker
- [ ] Insurance integration
- [ ] Mobile app (React Native)

### Q3 2026
- [ ] Pharmacy integration
- [ ] Patient wearables integration
- [ ] Advanced analytics dashboard
- [ ] Multilingual support

### Q4 2026
- [ ] Prescription fulfillment
- [ ] Lab integration
- [ ] Billing and payments
- [ ] HIPAA compliance audit

## 🎓 Learning Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue 3 Documentation](https://vuejs.org/guide/introduction.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [PostgreSQL Tutorials](https://www.postgresql.org/docs/)
- [Pinia State Management](https://pinia.vuejs.org/)
- [Vite Guide](https://vitejs.dev/)

---

**🎉 Ready to get started? Follow the [Quick Start](#-quick-start) section above or check out [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment.**

**Happy coding! 💻**
