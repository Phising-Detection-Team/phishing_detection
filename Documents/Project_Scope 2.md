
# Phishing Detection System - Project Specification
**Date**: January 29, 2026  
**Team Size**: 3 members  
**Project Lead**: First-time multi-person project leadership  
**Timeline**: Flexible, no rush (estimated 12-16 weeks for MVP)

---

## Executive Summary

An AI-powered email security system that uses competing machine learning models to detect phishing emails. The system employs a three-agent architecture where a Generator creates realistic phishing emails, a Detector identifies them, and a Judge evaluates both. This adversarial training approach continuously improves detection accuracy through offline competition rounds, while a browser extension provides real-time protection for end users.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Team Composition](#team-composition)
3. [Target Users](#target-users)
4. [System Architecture](#system-architecture)
5. [Technical Stack](#technical-stack)
6. [Core Features](#core-features)
7. [Database Design](#database-design)
8. [API Specification](#api-specification)
9. [User Interface](#user-interface)
10. [Real-Time Communication](#real-time-communication)
11. [Competition System](#competition-system)
12. [Ethical Considerations](#ethical-considerations)
13. [Privacy & Compliance](#privacy-compliance)
14. [Budget & Cost Management](#budget-cost-management)
15. [Development Phases](#development-phases)
16. [Success Metrics](#success-metrics)

---

## Project Overview

### Purpose
Develop a system that detects phishing and scam emails using frontier AI models in an adversarial training setup. The system will:
- Generate synthetic phishing emails for training data
- Detect phishing attempts with high accuracy
- Continuously improve through competitive rounds
- Provide real-time protection via browser extension

### Non-Technical Explanation
*For stakeholders:* "We're building an AI-powered email security system that learns by competing against itself. Think of it like a sparring partner for cybersecurity - one AI learns to create realistic phishing emails (like a security tester), while another AI learns to detect them (like a security guard). Each time they compete, both get smarter. This helps protect people from increasingly sophisticated email scams without requiring massive amounts of training data upfront."

### Key Differentiators
- **Self-improving**: Models compete to generate better training data
- **No manual labeling**: Automated judge evaluates performance
- **Browser-native**: Seamless integration with Gmail, Outlook, etc.
- **Cost-effective**: Uses frontier models initially, collects data for future fine-tuning

---

## Target Users

### Primary Audience
- **Individual email users**: People wanting personal email protection
- **Small businesses**: Teams needing affordable phishing detection

### User Interaction
- **Browser extension** for Gmail, Outlook, and other webmail clients
- Opens when user navigates to email website
- Real-time scanning when emails are opened
- Displays risk score and rationale directly in the interface

### Expected Volume
- **Initial**: < 100 emails per day
- **Scaling consideration**: Architecture supports growth to thousands/day

---

## Core Features

### Feature Priority Matrix

| Priority | Feature | Status | Phase |
|----------|---------|--------|-------|
| **P0** | Three-agent competition system | To Build | Phase 1 |
| **P0** | Real-time dashboard with live updates | To Build | Phase 1 |
| **P0** | Database persistence | To Build | Phase 1 |
| **P1** | Manual verdict override | To Build | Phase 1 |
| **P1** | Historical accuracy charts | To Build | Phase 1 |
| **P1** | Round triggering via UI | To Build | Phase 1 |
| **P2** | CLI script for rounds | To Build | Phase 1 |
| **P2** | Optional email upload for rounds | To Build | Phase 2 |
| **P2** | Cost tracking dashboard | To Build | Phase 2 |
| **P3** | Browser extension (detection only) | To Build | Phase 3 |
| **P3** | Caching layer for scans | To Build | Phase 3 |
| **Future** | Email forwarding integration | Backlog | Phase 4+ |
| **Future** | Custom model fine-tuning | Backlog | Phase 4+ |

### Feature Requirements

#### 1. Monitor Competition Progress in Real-Time (Priority: 1)
- **Description**: Live dashboard showing email processing progress
- **Requirements**:
  - WebSocket connection for instant updates
  - Progress bar (X/100 emails processed)
  - Live accuracy graph updating as emails complete
  - Current detector accuracy percentage
  - Generator success rate percentage
  - Processing speed (emails/minute)

#### 2. Trigger New Competition Rounds (Priority: 2)
- **Description**: Start competitions via UI or CLI
- **Requirements**:
  - "Start Round" button in dashboard
  - Configuration options: number of emails (default 100)
  - Optional: upload batch of test emails
  - CLI command: `python cli.py run-round --emails 100`
  - Validation: prevent concurrent rounds
  - Runs to completion (no pause/stop)

#### 3. Compare Performance Across Model Versions (Priority: 3)
- **Description**: Historical comparison of detector improvement
- **Requirements**:
  - Time-series line chart (rounds on X-axis, accuracy on Y-axis)
  - Display last 10-20 rounds
  - Hover tooltips with detailed metrics
  - Date-based filtering
  - Export chart as PNG for presentations

#### 4. Debug Failed Detections (Priority: 4)
- **Description**: Drill down into specific email failures
- **Requirements**:
  - Click round → view all emails
  - Filter by: All, Correct, Incorrect, False Positives, False Negatives
  - Click email → full detail view
  - Display: generated content, detector analysis, judge verdict
  - Search functionality

#### 5. Manual Override of Judgments (Priority: 4)
- **Description**: Team can correct judge verdicts
- **Requirements**:
  - "Override Verdict" button on email detail page
  - Dropdown: Correct Detection / Incorrect Detection
  - Text field: reason for override
  - Tracks who made override and when
  - Updates round accuracy metrics automatically

#### 6. Generate Reports for Presentations (Priority: 2)
- **Description**: Export data for stakeholders
- **Requirements**:
  - Screenshot-friendly dashboard design
  - Clean, professional charts
  - Summary stats prominently displayed
  - Future: PDF export, CSV download

---

### Key Design Decisions

**1. Round Status Values**
- `running`: Competition in progress
- `completed`: Successfully finished
- `failed`: Error occurred during execution

**2. Verdict Values**
- `phishing`: Email is malicious
- `legitimate`: Email is safe

**3. Log Levels**
- `info`: Normal operations (round started, completed)
- `warning`: Non-critical issues (high latency, retries)
- `error`: Failures requiring attention (API timeouts, exceptions)

**4. JSONB Fields**
- `generated_email_metadata`: Flexible storage for headers, links, attachments
- `context` in logs: Stack traces, API responses, error details

**5. Log Retention Strategy**
- Keep logs for last 5 completed rounds
- Automated cleanup via scheduled Celery task
- Archive old logs to file storage before deletion

---

## User Interface

### Page Layouts

#### 1. Home Dashboard
**Purpose**: High-level overview and quick actions

**Components**:
- Active round status widget (if running)
- Quick stats cards: Total rounds, Current accuracy, Total cost
- "Start New Round" button
- Recent rounds table (last 5)
- Accuracy trend chart (last 10 rounds)
- System health indicators

**Key Metrics Displayed**:
- Detector accuracy (%) - Priority 1
- Generator success rate (%) - Priority 1
- Average confidence score - Priority 2
- Processing time - Priority 2
- Cost - Priority 3

#### 2. Rounds List View
**Purpose**: Historical overview of all competition rounds

**Components**:
- Data table with columns: Round #, Date, Status, Emails, Accuracy, Duration, Cost
- Search and filter controls
- Pagination
- Time-series chart showing accuracy over all rounds
- Generator success rate trend line

**Interactions**:
- Click row → Navigate to Round Detail
- Sort by any column
- Filter by status (running, completed, failed)
- Date range picker

#### 3. Round Detail View
**Purpose**: Deep dive into single round performance

**Components**:
- Round summary header (ID, date, duration, final metrics)
- Breakdown stats: Correct identifications, false negatives, false positives
- Email list table with filters (All, Correct, Incorrect, False Positives, False Negatives)
- Search box for email content
- Live progress section (if round is running)
  - Real-time progress bar
  - Live accuracy graph
  - Current processing rate (emails/min)

**Interactions**:
- Click email row → Navigate to Email Detail
- Apply filters to narrow email list
- Export round data as CSV

#### 4. Email Detail View
**Purpose**: Full conversation between all three agents

**Components**:
- Three-column layout:
  - **Generator Section**: Prompt, generated email content, metadata, latency
  - **Detector Section**: Risk score, reasoning, verdict, latency
  - **Judge Section**: Ground truth, correctness evaluation, quality score, feedback, latency
- Manual override panel:
  - Override verdict dropdown
  - Reason text field
  - Submit button
  - Override history (who, when, why)
- Navigation: Previous/Next email buttons

**Visual Design**:
- Color coding: Green (correct), Red (incorrect), Yellow (overridden)
- Expandable sections for verbose content
- Syntax highlighting for email headers/metadata

#### 5. System Logs View
**Purpose**: Debug and monitor system operations

**Components**:
- Log level filter (All, Info, Warning, Error)
- Round filter dropdown
- Time range selector
- Log entries table: Timestamp, Level, Message, Context (expandable)
- Real-time log streaming (auto-updates)

**Retention**:
- Display logs from last 5 rounds only
- Older logs archived automatically

#### 6. Cost Dashboard
**Purpose**: Budget tracking and API usage monitoring

**Components**:
- Budget progress bar ($X / $100 used)
- Pie chart: Cost breakdown by agent (Generator, Detector, Judge)
- Line chart: Daily spending over time
- Cost per round table
- Projected monthly spend based on current usage
- Cost efficiency metrics (cost per email, cost per correct detection)

---

## Competition System

### Competition Round Lifecycle

### Round Configuration

**Default Settings**:
- Emails per round: 100
- Processing mode: Sequential (one at a time for MVP)
- Retry policy: 3 attempts for API failures
- Timeout: 30 seconds per agent call

**Optional Settings**:
- Upload custom test emails (JSON format)
- Round notes/description
- Creator name for tracking

### Email Generation Strategy

**Generator Prompts** (examples to be refined):
- "Create a phishing email impersonating a bank"
- "Generate a job scam email"
- "Create a fake package delivery notification"
- "Generate a CEO fraud email"
- "Create a prize/lottery scam"

**Prompt Rotation**: Cycle through different phishing types for variety

### Detector Analysis

**Input**: Full email content (subject, body, headers, metadata)

**Output**:
- Risk score (0.0 - 1.0)
- Verdict (phishing | legitimate)
- Detailed reasoning (multi-point analysis)
- Confidence level

**Reasoning Format** (structured):
- Domain analysis
- Language patterns (urgency, threats, rewards)
- Link analysis
- Sender reputation indicators
- Header authenticity checks

### Judge Evaluation

**Responsibilities**:
1. Assign ground truth label (phishing | legitimate)
2. Evaluate detector correctness (correct | incorrect)
3. Rate generator quality (1-10 score)
4. Provide feedback for improvement

**Evaluation Criteria**:
- **Generator Quality**: Realism, sophistication, variety
- **Detector Accuracy**: Correctly identified phishing, reasoning quality
- **False Positive Analysis**: Legitimate emails incorrectly flagged

**Output Format**:
- Ground truth verdict
- Is detector correct (boolean)
- Quality score (1-10)
- Detailed feedback (text)

### Manual Override Process

**Who Can Override**: Any team member

**Override Workflow**:
1. Navigate to email detail page
2. Review all three agent outputs
3. Click "Override Verdict"
4. Select corrected verdict
5. Enter reason (required)
6. Submit

**Effects**:
- Updates email record with override
- Recalculates round accuracy metrics
- Logs override action
- Does NOT retrain models (manual collection for future fine-tuning)

### Performance Optimization

**Future Enhancements** (Post-MVP):
- Parallel processing (5-10 emails simultaneously)
- Batch API calls where supported
- Result caching for identical emails
- GPU acceleration for custom models

---

## Ethical Considerations

### Responsible AI Usage

**Core Principles**:
1. **Generator is internal-only**: Never user-facing, never publicly accessible
2. **Research purposes only**: Improve detection, not create real threats
3. **Team accountability**: All usage logged and auditable
4. **Transparent labeling**: Generated emails watermarked/tracked
5. **Controlled access**: Admin authentication required

### Security Safeguards

**Technical Controls**:
- Generator endpoint requires admin authentication token (no public access)
- Rate limiting: Maximum 10 generations per hour per user
- Watermarking: All generated emails tagged with hidden identifier
- Audit logging: Every generation logged with purpose and user ID
- No email sending: System cannot send generated emails externally
- Isolated environment: Generator runs in secure container

**Access Control**:
- Role-based permissions (admin vs. viewer)
- API keys rotated regularly
- Session timeouts enforced
- IP whitelist for production environment

### Ethical Guidelines Document

**Team Agreement** (to be signed by all members):
1. Generator only for improving detector
2. Never test on real users without explicit consent
3. Generated emails stored securely on internal servers only
4. No sharing of generated content outside team
5. Regular review of generated content quality and appropriateness
6. Immediate incident reporting for misuse concerns

### Legal Considerations

**Terms of Service Compliance**:
- Review OpenAI, Anthropic, etc. TOS regarding malicious content generation
- Some providers prohibit generating phishing content
- May require research exemption or academic partnership
- Consider using models with explicit security research allowances

**Institutional Requirements**:
- Research ethics approval (if academic institution)
- Legal review for liability concerns
- Data protection officer consultation
- Insurance considerations

**Liability Protection**:
- Clear documentation that generator is for security research
- Watermarking proves synthetic origin
- User agreements for browser extension
- Incident response plan

### Content Moderation

**Generator Output Review**:
- Random sampling of generated emails for quality control
- Flag excessively harmful content (e.g., explicit threats)
- Adjust prompts to avoid offensive content
- Maintain diversity without crossing ethical lines

**Feedback Mechanism**:
- Team can flag problematic generated emails
- Regular retrospectives on ethical concerns
- Continuous refinement of generation guidelines

---

## Privacy & Compliance

### GDPR Fundamentals

**What is GDPR**:
- EU General Data Protection Regulation
- Protects personal data of EU residents
- Applies if: EU users use your browser extension

**Key Requirements**:
1. **Consent**: Users must agree before email processing
2. **Data Minimization**: Only collect necessary information
3. **Right to Access**: Users can request their data
4. **Right to Deletion**: Users can request data removal
5. **Data Security**: Encrypt and protect sensitive information
6. **Breach Notification**: Report data breaches within 72 hours

### Privacy-First Architecture

**Data Collection Strategy**:
- **Minimize**: Only send emails flagged as potentially suspicious to server
- **Anonymize**: Strip personally identifiable information where possible
- **Encrypt**: TLS for all data in transit
- **Retention**: Delete scan results after 30 days (configurable)

**Browser Extension Privacy**:
- Local pre-filtering: Basic checks done in browser (no server call)
- User consent: Clear opt-in flow on first launch
- Privacy policy: Accessible from extension popup
- Data disclosure: Explain what data is sent to server

### User Consent Flow

**First-Time Installation**:
1. User installs extension
2. Extension shows welcome screen
3. Display privacy policy summary
4. User clicks "I Agree" or "Learn More"
5. Extension activates only after consent

**Privacy Policy Content** (simplified):
- What data is collected (email content for suspicious emails only)
- Why it's collected (phishing detection)
- Where it's stored (server location)
- How long it's kept (30 days)
- Who has access (internal team only)
- User rights (request data, request deletion)

### Data Handling Best Practices

**Email Scanning**:
- Do NOT store full email content permanently
- Store only: risk score, verdict, timestamp, anonymized metadata
- Option: Store flagged emails temporarily for manual review (with consent)

**Competition System**:
- Generated emails are synthetic (no real user data)
- Safe to store and analyze

**User Accounts** (if implemented):
- Secure password hashing (bcrypt)
- Optional two-factor authentication
- Session management with secure cookies

### Compliance Checklist

- [ ] Privacy policy drafted and reviewed
- [ ] User consent mechanism implemented
- [ ] Data encryption at rest and in transit
- [ ] Data retention policy defined and automated
- [ ] User data export functionality
- [ ] User data deletion functionality
- [ ] Security audit conducted
- [ ] Incident response plan documented
- [ ] GDPR compliance review (if EU users)
- [ ] Terms of service finalized

---

## Development Phases

### Phase 1: Foundation (Weeks 1-4)
**Goal**: Offline competition system functional

**Deliverables**:
- ✅ Flask API with Docker setup
- ✅ PostgreSQL database with schema
- ✅ Three-agent system (Generator, Detector, Judge)
- ✅ Celery background tasks
- ✅ Basic React dashboard (static)
- ✅ Manual round triggering via API
- ✅ Database persistence of results
- ✅ Basic logging

**Success Criteria**:
- Can start a competition round manually
- All 100 emails processed successfully
- Results stored in database
- Can view results in simple UI

**Team Split**:
- **Developer**: Backend API, database setup, Docker configuration
- **Engineer/PM**: React app scaffolding, component structure, architecture docs
- **Security Student**: Prompt engineering, evaluation criteria design, testing

**Milestones**:
- Week 1: Project setup, Docker environment, database schema
- Week 2: Three-agent integration, basic API endpoints
- Week 3: Celery tasks, competition orchestration logic
- Week 4: Basic UI, end-to-end testing

---

### Phase 2: Real-Time Dashboard (Weeks 5-8)
**Goal**: Live monitoring and interactivity

**Deliverables**:
- ✅ WebSocket integration (Flask-SocketIO)
- ✅ Real-time progress updates
- ✅ Live accuracy chart
- ✅ Round detail page with drill-down
- ✅ Email detail view (three-column layout)
- ✅ Manual override functionality
- ✅ System logs viewer
- ✅ Historical comparison charts

**Success Criteria**:
- Watch competition progress live in browser
- Click through to individual email analysis
- Override judge verdicts
- View accuracy improvement over time

**Team Split**:
- **Developer**: WebSocket server, event emission, API refinements
- **Engineer/PM**: React components, Chart.js integration, UI/UX polish
- **Security Student**: Analyze first round results, refine prompts, document findings

**Milestones**:
- Week 5: WebSocket setup, basic event streaming
- Week 6: Live dashboard components, progress indicators
- Week 7: Detail pages, override functionality
- Week 8: Charts, logs viewer, polish

---

### Phase 3: User Scanning API (Weeks 9-12)
**Goal**: API ready for browser extension

**Deliverables**:
- ✅ `/api/scan` endpoint optimized for speed
- ✅ Redis caching layer
- ✅ Response time < 2 seconds
- ✅ Rate limiting
- ✅ API documentation
- ✅ Cost tracking dashboard
- ✅ Privacy policy draft

**Success Criteria**:
- Can POST an email to `/api/scan` and get risk score back
- Cache hit rate > 30%
- API handles 100+ requests/day
- Cost per scan tracked accurately

**Team Split**:
- **Developer**: Scanning endpoint, caching, optimization, rate limiting
- **Engineer/PM**: Cost dashboard, API docs, deployment prep
- **Security Student**: Test with real phishing datasets, validate accuracy

**Milestones**:
- Week 9: Scan endpoint implementation, caching setup
- Week 10: Performance optimization, rate limiting
- Week 11: Cost tracking, monitoring dashboard
- Week 12: Documentation, privacy policy, testing

---

### Phase 4: Browser Extension (Weeks 13-16)
**Goal**: End-user phishing detection

**Deliverables**:
- ✅ Chrome extension (manifest v3)
- ✅ Gmail integration (content script)
- ✅ Email content extraction
- ✅ Risk score badge overlay
- ✅ Detail popup with full analysis
- ✅ User settings panel
- ✅ Privacy consent flow
- ✅ Local pre-filtering

**Success Criteria**:
- Extension installs and works in Chrome
- Displays risk score on Gmail emails
- Respects user privacy preferences
- Handles errors gracefully

**Team Split**:
- **Developer**: Backend API refinements, extension backend services
- **Engineer/PM**: Extension development, Gmail integration, UI components
- **Security Student**: Local filtering logic, indicator detection, user testing

**Milestones**:
- Week 13: Extension scaffolding, Gmail content extraction
- Week 14: API integration, risk score display
- Week 15: Privacy flow, settings, local filtering
- Week 16: Testing, bug fixes, Chrome Web Store preparation

---

### Phase 5+: Enhancements (Future)
**Potential Features**:
- Outlook, Yahoo Mail support
- Custom model fine-tuning with collected data
- Email forwarding integration (forward@phishguard.com)
- Mobile app
- Enterprise dashboard (multi-user teams)
- Export training datasets
- A/B testing different models
- Scheduled competition rounds
- Slack/email notifications

---

## Next Steps

### Immediate Actions
1. **Review this specification** with full team
2. **Get team agreement** on ethical guidelines
3. **Set up project repository** (Git)
4. **Choose initial AI models** (recommend GPT-4o-mini to start)
5. **Create project workspace** in VS Code
6. **Scaffold project structure** (backend + frontend)

### First Week Tasks
- [ ] Initialize Git repository
- [ ] Set up Docker Compose environment
- [ ] Create PostgreSQL schema
- [ ] Set up OpenAI/Anthropic API accounts
- [ ] Implement basic Flask app structure
- [ ] Create React app with Vite
- [ ] Weekly team sync established

---

## Document Version Control
- **Version**: 1.0
- **Last Updated**: January 29, 2026
- **Next Review**: After Phase 1 completion
- **Maintained By**: Project Lead

---

**End of Specification Document**
