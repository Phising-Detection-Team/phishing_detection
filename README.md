# Phishing Detection System

> **AI-Powered Email Security through Adversarial Training**

An intelligent email security system that uses frontier AI models in a three-agent architecture to detect phishing emails. The system employs competitive learning where a Generator creates realistic phishing emails, a Detector identifies them, and a Judge evaluates both, continuously improving detection accuracy through offline training rounds.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Status](#project-status)
- [Team](#team)
- [Documentation](#documentation)

---

## 🎯 Project Overview

### Purpose

This system addresses the growing sophistication of phishing attacks by using AI models that compete against each other to generate training data and improve detection accuracy. Unlike traditional rule-based filters, this approach continuously evolves to counter new attack techniques.

### Target Users

- **Individual email users** seeking personal email protection
- **Small business employees** lacking advanced cybersecurity awareness
- **Security operations teams** needing automated threat detection

### Success Metrics

- **Detection accuracy**: >85% precision, >80% recall
- **False positive rate**: <5%
- **Detection speed**: <5 seconds per email
- **System uptime**: 99%

---

## ✨ Key Features

### Three-Agent Competition System (Phase 1 - In Progress)

- **Generator Agent**: Creates synthetic phishing emails for training
- **Detector Agent**: Analyzes emails and identifies threats
- **Judge Agent**: Evaluates detector accuracy and generator quality

### Real-Time Monitoring Dashboard (Phase 2 - Planned)

- Live competition round progress tracking
- WebSocket-powered instant updates
- Historical accuracy trend visualization
- Drill-down into individual email analysis
- Manual verdict override capability

### Browser Extension (Phase 3 - Future)

- Real-time email scanning for Gmail, Outlook, etc.
- Risk score overlay on emails
- Privacy-first local pre-filtering
- User consent and data protection

---

## 🏗️ System Architecture

### Three-Agent Architecture

```
┌──────────────┐
│   Generator  │ → Creates phishing emails with metadata
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Detector   │ → Analyzes email, provides verdict + reasoning
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Judge     │ → Evaluates correctness, assigns quality score
└──────────────┘
```

### Competition Round Lifecycle

1. **Initialize**: Configure round (100 emails default)
2. **Generate**: Create synthetic phishing/legitimate emails
3. **Detect**: Analyze each email for threat indicators
4. **Judge**: Evaluate detector performance
5. **Store**: Persist results in PostgreSQL
6. **Analyze**: Display metrics and insights

### Technology Layers

- **Frontend**: React dashboard (real-time updates via WebSocket)
- **Backend**: Flask API with Celery for async processing
- **Database**: PostgreSQL for persistence, Redis for caching
- **AI Integration**: Google Gemini API (frontier models)
- **Deployment**: Docker containers (planned)

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Task Queue**: Celery 5.6.2 with Redis
- **Database**: PostgreSQL with SQLAlchemy 2.0.46
- **Real-time**: Flask-SocketIO 5.6.0
- **Migrations**: Alembic 1.18.3

### Frontend (Planned)
- **Framework**: React with Next.js or Vite
- **Charts**: Chart.js for analytics
- **WebSocket**: Socket.IO client

### AI/ML
- **Primary Model**: Google Gemini (via google-generativeai 0.8.6)
- **Future**: PyTorch/TensorFlow for fine-tuned models

### DevOps
- **Containerization**: Docker & Docker Compose (planned)
- **Version Control**: Git/GitHub
- **Testing**: pytest 9.0.2, coverage 7.13.2
- **Code Quality**: black, flake8, pylint, mypy

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Google Gemini API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd phishing_detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r app/requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start Redis server
redis-server

# Run Celery worker
celery -A app.celery worker --loglevel=info

# Run Flask application
python app/run.py
```

### Configuration

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/phishing_detection

# Redis
REDIS_URL=redis://localhost:6379/0

# Google Gemini API
GEMINI_API_KEY=your_api_key_here

# Flask
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

---

## 📊 Project Status

### Current Phase: **Phase 1 - Foundation** (Weeks 1-4)

#### ✅ Completed
- Database schema design (Email model)
- SQLAlchemy models with proper relationships
- Requirements.txt with comprehensive dependencies
- Project architecture documentation
- Detailed project scoping questionnaire

#### 🔄 In Progress
- Flask API setup and configuration
- Three-agent integration (Generator, Detector, Judge)
- Database models for Round and Log entities
- Celery task orchestration
- Docker containerization

#### ⏳ Upcoming (Phase 1)
- Basic React dashboard setup
- Manual round triggering via API
- End-to-end testing
- Documentation and code comments

### Roadmap

| Phase | Timeline | Status | Key Deliverables |
|-------|----------|--------|------------------|
| **Phase 1**: Foundation | Weeks 1-4 | 🔄 In Progress | Offline competition system, database setup |
| **Phase 2**: Dashboard | Weeks 5-8 | ⏳ Planned | Real-time monitoring, WebSocket integration |
| **Phase 3**: User API | Weeks 9-12 | ⏳ Planned | Email scanning endpoint, caching, rate limiting |
| **Phase 4**: Extension | Weeks 13-16 | ⏳ Planned | Chrome extension, Gmail integration |
| **Phase 5+**: Enhancements | Future | 💡 Ideas | Federated learning, custom model fine-tuning |

---

## 👥 Team

- **Le Hoang Nhat Duy** - Project Supervisor / Expert
- **Pham Thanh Hoan** - Developer / Engineer
- **Pham Thien Quy** - Cybersecurity Analyst / Developer

**Team Structure**: First-time multi-person project with flexible timeline and collaborative learning focus.

---

## 📚 Documentation

- [Project Scope](Documents/Project_Scope.md) - Comprehensive specification and requirements
- [Questions & Decisions](Documents/Questions.md) - Detailed scoping questionnaire with answers
- [Architecture Diagram](Documents/Project_Architecture.excalidraw) - System architecture visualization

### Key Documentation Highlights

#### Threat Detection Scope (Priority Ordered)
1. **Priority 1**: Phishing, malware attachments, social engineering
2. **Priority 2**: Spear phishing, BEC, account takeover
3. **Priority 3**: Spam

#### Data Privacy Approach
- GDPR-compliant principles (student project)
- Encryption at rest (AES-256) and in transit (TLS 1.2+)
- User consent flow for browser extension
- 30-day data retention policy
- Clear privacy policy and ToS

#### Ethical Safeguards
- Generator is internal-only (no public access)
- Watermarking of all synthetic emails
- Admin authentication required
- Rate limiting (10 generations/hour)
- Audit logging for accountability

---

## 🔒 Security & Privacy

### Data Protection
- All sensitive data encrypted at rest and in transit
- API keys stored in environment variables (never committed)
- Database credentials secured via environment configuration
- Session management with secure cookies

### Responsible AI Usage
- Generator model isolated (no external network access)
- Research-only purpose documentation
- Team accountability agreement
- Regular ethical reviews

---

## 📈 Success Metrics & KPIs

### Technical Metrics
- Detection accuracy: Target >85% precision, >80% recall
- False positive rate: <5%
- Processing latency: <5 seconds per email
- System uptime: 99%

### User Metrics (Future)
- User satisfaction score (survey-based)
- Threats successfully blocked
- Alert click-through rate
- Reduction in successful attacks

---

## 🤝 Contributing

This is a student project with a closed team during active development. Post-completion, the repository will be open-sourced on GitHub with contribution guidelines.

---

## 📄 License

To be determined upon project completion.

---

## 🙏 Acknowledgments

- **OpenPhish & PhishTank**: Public phishing datasets
- **Google Gemini**: Frontier AI model access
- **Flask Community**: Excellent web framework documentation
- **Academic Supervisor**: Le Hoang Nhat Duy

---

## 📞 Contact

For questions or collaboration inquiries:
- **Email**: [Contact through repository issues]
- **Project Start Date**: January 29, 2025
- **Expected Completion**: April 2025 (MVP)

---

**Status**: 🔄 Active Development | **Last Updated**: February 1, 2026
