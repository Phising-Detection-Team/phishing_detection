# Phishing Detection System - Phase 1 Development & Planning Guide

**Phase 1: Foundation (Weeks 1-4)**  
**Start Date**: February 9, 2026  
**Target Completion**: March 9, 2026  
**Current Status**: Database schema complete, implementation ready

---

## Executive Summary

Phase 1 delivery includes:
- ✅ Database schema (done)
- 🔲 Flask API with all endpoints (est. 3-4 days)
- 🔲 Three-agent integration (Python functions with OpenAI/Anthropic)
- 🔲 Semantic Kernel & OpenAI Agentic SDK orchestration with parallel workflows
- 🔲 Cost tracking implementation
- 🔲 Error handling & pause-on-fail logic
- 🔲 Unit & integration tests (80%+ coverage)
- 🔲 Database schema learning (constraints, migrations, rollback)
- 🔲 Redis caching (LLM responses & DB queries)
- 🔲 Docker containerization
- 🔲 Security hardening
- 🔲 Load testing baseline

**Total Estimated Effort**: 130-160 engineering hours across 6 buckets
**Team Capacity**: 4 developers × 4 weeks × 25-30 hours/week = 400-480 available hours  
**Slack Buffer**: Comfortable (2.5-3.5x buffer for unknowns)

---

## Team Structure (4 Developers)

### Team Members
- **Hoang Nhat Duy** - Project Supervisor, Tech Lead & Semantic Kernel Architect
- **Bao Duy** - Developer/Engineer, Semantic Kernel Lead
- **Thanh Dang** - Developer/Engineer, Infrastructure & API Lead
- **Thien Quy** - Cybersecurity Analyst/Developer, Security & Testing Lead

### Role Distribution

| Role | Owner | Focus Area | Learning Goals |
|------|-------|-----------|----------------|
| **Tech Lead** | Hoang | SK architecture, mentorship, code reviews, unblocking | Semantic Kernel mastery + system design |
| **SK Deep Dive** | Bao Duy | SK plugins, parallel workflows, agent orchestration | SK + OpenAI Agentic SDK expertise |
| **Infrastructure** | Thanh Dang | Flask APIs, database integration, Docker | REST API design + DevOps |
| **Security & QA** | Thien Quy | Testing, security hardening, performance testing | Security engineering + reliability |

### Weekly Commitment
- **Hoang**: 15-20 hrs implementation + 10 hrs mentorship/review = ~25-30 hrs/week
- **Bao Duy**: 25-30 hrs on SK orchestration
- **Thanh Dang**: 25-30 hrs on APIs and Docker
- **Thien Quy**: 25-30 hrs on testing and security

---

**Board Name**: Phishing Detection - Phase 1  
**Board Type**: Kanban (Backlog → TODO → In Progress → In Review → Done)  
**Team Size**: 4 developers  
**Sprint Length**: 4 weeks (Feb 9 - Mar 9, 2026)

### Bucket Structure (5 Buckets)

Create these 5 buckets in Microsoft Planner:

1. **BUCKET 1: INFRASTRUCTURE & API SETUP** (20 hrs)
2. **BUCKET 2: THREE-AGENT INTEGRATION** (30 hrs)
3. **BUCKET 3: TESTING & QA** (25 hrs)
4. **BUCKET 4: DATABASE SCHEMA & MIGRATION LEARNING** (11 hrs)
5. **BUCKET 5: PERFORMANCE & DEPLOYMENT** (20 hrs)
6. **BUCKET 6: FRONTEND SCAFFOLDING** (planning only)

### Kanban Workflow

Cards move through these columns:

```
BACKLOG → TODO → IN PROGRESS → IN REVIEW → DONE
```

**Guidelines**:
- Only 1-2 cards per developer in "IN PROGRESS" at a time
- Use "IN REVIEW" for code review / PR feedback
- "DONE" = merged to main branch + tested + documented

### Priority Levels

- 🔴 **P0 - Critical**: Blocker for other tasks or Phase 1 completion
- 🟡 **P1 - High**: Important, some flexibility on timing
- 🟢 **P2 - Medium**: Nice-to-have, or Phase 2 work
- ⚪ **P3 - Low**: Future phases, exploratory

### Weekly Sprint Reviews

**Every Friday 3:00 PM** (15 mins):
- [ ] Review completed cards (actual vs. planned)
- [ ] Discuss blockers
- [ ] Adjust priorities for next week
- [ ] Update timeline/effort if needed

### Key Metrics to Track

Each week, monitor:
- Completed cards vs. planned
- Code coverage (target: 80%+)
- Outstanding bugs
- Blocker issues
- Team velocity (hours/developer/week)

---

## Detailed Task Breakdown by Category

### BUCKET 1: INFRASTRUCTURE & API SETUP

#### 1.1 Flask App Initialization
- **Priority**: 🔴 P0 (Blocker)
- **Assigned To**: Thanh Dang (Developer/Engineer)
- **Effort**: 2-3 hours
- **Timeline**: Week 1 (Monday-Tuesday)
- **Depends On**: None
- **Blocking**: 1.2, 1.3, 1.4, 1.5

**Description**:
Initialize Flask application with configuration, blueprints, and error handlers.

**Acceptance Criteria**:
- [ ] Flask app runs: `python run.py` without errors
- [ ] All blueprints registered (rounds, emails, logs, health)
- [ ] Config loads from environment variables
- [ ] CORS headers configured
- [ ] Error handlers working (400, 404, 500)

**Checklist**:
- [ ] Create `backend/app/__init__.py` with Flask() initialization
- [ ] Create `backend/app/config.py` with Dev/Test/Prod configs
  - Database URL from env variables
  - OpenAI API key and settings
  - Semantic Kernel configuration
  - Redis connection settings for caching
  - API keys for Gemini/OpenAI (from env)
- [ ] Update `backend/run.py` as Flask app entry point
  - Initialize app with config
  - Initialize SQLAlchemy `db`
  - Initialize Redis connection for caching
  - Initialize Semantic Kernel kernel
  - Register error handlers
- [ ] Create `.env.example` with required variables
  - `DATABASE_URL`
  - `REDIS_URL` (for caching LLM responses and query results)
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`
  - `SEMANTIC_KERNEL_LOG_LEVEL`
  - `FLASK_ENV`
- [ ] Test: `python run.py` starts without errors
- [ ] Test: Health check endpoint returns 200

**Notes**: Do NOT integrate agents yet, just structure

---

#### 1.2 API Endpoints - Rounds
- **Priority**: 🔴 P0
- **Assigned To**: Thanh Dang (Infrastructure Lead)
- **Effort**: 3-4 hours
- **Timeline**: Week 1 (Wednesday-Thursday)
- **Depends On**: 1.1 (Flask init)
- **Blocking**: 2.2, 3.3

**Description**:
Implement three endpoints for round management: start new round, list rounds with pagination/filtering, get round details.

**Acceptance Criteria**:
- [ ] `POST /api/rounds` returns 201 with round object
- [ ] `GET /api/rounds` returns paginated list with filters
- [ ] `GET /api/rounds/{id}` returns round details
- [ ] All filters work (status, created_by, sort_by)
- [ ] Database transactions complete
- [ ] Input validation returns proper error codes

**Checklist**:
- [ ] Create `backend/app/routes/rounds.py`
- [ ] Implement `POST /api/rounds` endpoint
  - Input: total_emails, notes, created_by
  - Validation: Check no round is running
  - Output: Round object with status=running
  - Action: Trigger Semantic Kernel workflow for round execution
- [ ] Implement `GET /api/rounds` endpoint
  - Query params: status, created_by, sort_by, page, per_page
  - Output: Paginated list + metadata
  - Test all sorting/filtering options
- [ ] Implement `GET /api/rounds/{id}` endpoint
  - Output: Full round with metrics
  - Return 404 if not found
- [ ] Verify HTTP status codes match OpenAPI spec
- [ ] Test pagination with edge cases (page=0, per_page=1000)

---

#### 1.3 API Endpoints - Emails
- **Priority**: 🔴 P0
- **Assigned To**: Thanh Dang (Infrastructure Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 1 (Thursday-Friday)
- **Depends On**: 1.1, 1.2
- **Blocking**: 3.3

**Description**:
Implement endpoints for email retrieval and verdict override.

**Acceptance Criteria**:
- [ ] `GET /api/rounds/{id}/emails` supports 5 filter types
- [ ] `GET /api/emails/{id}` returns all agent outputs
- [ ] `POST /api/emails/{id}/override` updates database
- [ ] Override recalculates round accuracy automatically
- [ ] Response times < 200ms

**Checklist**:
- [ ] Create `backend/app/routes/emails.py`
- [ ] Implement `GET /api/rounds/{id}/emails`
  - Query params: filter (all/correct/incorrect/false_positives/false_negatives), page, per_page
  - Output: Paginated email list
  - Test all filter combinations
- [ ] Implement `GET /api/emails/{id}`
  - Output: Full email with all agent outputs (generator, detector, judge)
  - Return 404 if not found
- [ ] Implement `POST /api/emails/{id}/override`
  - Input: verdict (phishing|legitimate), reason, overridden_by
  - Action: Update override fields, recalculate round accuracy
  - Output: Updated email
  - Validation: verdict must be valid enum
- [ ] Implement accuracy recalculation logic in database query
- [ ] Test pagination with multiple pages

---

#### 1.4 API Endpoints - Logs & System Health
- **Priority**: 🟡 P1
- **Assigned To**: Thanh Dang (Infrastructure Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 1 (Wednesday-Friday)
- **Depends On**: 1.1
- **Blocking**: 3.3

**Description**:
Implement endpoints for system logs, cost tracking, and health status.

**Acceptance Criteria**:
- [ ] `GET /api/logs` returns logs with all filters
- [ ] `GET /api/costs` returns cost breakdown correctly
- [ ] `GET /api/health` returns component status
- [ ] Log filtering by level, round, timestamp works
- [ ] Cost aggregation is fast (<500ms for 10k logs)

**Checklist**:
- [ ] Create `backend/app/routes/logs.py`
- [ ] Implement `GET /api/logs` endpoint
  - Query params: level (all/info/warning/error), round_id, start_time, end_time, page, per_page
  - Output: Paginated logs with context
  - Test time range filtering
- [ ] Create `backend/app/routes/health.py`
- [ ] Implement `GET /api/health` endpoint
  - Check database connectivity
  - Check Redis cache connectivity
  - Check OpenAI API connectivity
  - Check Semantic Kernel initialization
  - Output: Status (healthy|degraded|unhealthy) + components
- [ ] Create `backend/app/routes/costs.py`
- [ ] Implement `GET /api/costs` endpoint
  - Query params: round_id (optional), agent_type (optional)
  - Output: Total cost, cost breakdown by agent, cost by round, estimated monthly
  - Implement SUM aggregations efficiently
- [ ] Test pagination on all endpoints

---

#### 1.5 Error Handling & Validation Middleware
- **Priority**: 🔴 P0
- **Assigned To**: Hoang Nhat Duy (Tech Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 1 (Wednesday-Thursday)
- **Depends On**: 1.1
- **Blocking**: None (improves all endpoints)

**Description**:
Create consistent error handling, validation, and exception management across all endpoints.

**Acceptance Criteria**:
- [ ] All API errors return consistent JSON format
- [ ] HTTP status codes match error type (400, 404, 500, etc.)
- [ ] No unhandled exceptions reach client
- [ ] Errors contain error_code + message + details
- [ ] All errors logged to database

**Checklist**:
- [ ] Create `backend/app/utils/errors.py`
  - Define custom exceptions: `RoundInProgress`, `EmailNotFound`, `RoundNotFound`, `ValidationError`
- [ ] Create error handler decorators for Flask
- [ ] Implement global Flask error handlers
  - `@app.errorhandler(400)` - Bad Request
  - `@app.errorhandler(404)` - Not Found
  - `@app.errorhandler(500)` - Internal Server Error
- [ ] Create request validation decorator
  - Validates request body against schema
  - Returns 400 with detailed field errors
- [ ] Ensure consistent error response format:
  ```json
  {
    "error": "ERROR_CODE",
    "message": "Human readable message",
    "details": {...}
  }
  ```
- [ ] Test: Invalid input returns 400
- [ ] Test: Missing resource returns 404
- [ ] Test: Server error returns 500 with context

---

### BUCKET 2: THREE-AGENT INTEGRATION

#### 2.1 Service Layer - Agent Wrappers
- **Priority**: 🔴 P0
- **Assigned To**: Bao Duy (Developer/Engineer) with Hoang (Tech Lead)
- **Effort**: 4-5 hours
- **Timeline**: Week 1 (Thursday-Friday) + Week 2 (Monday)
- **Depends On**: Hoang's agent implementations (Agent APIs ready)
- **Blocking**: 2.2, 2.3

**Description**:
Create service layer wrapping calls to three-agent implementations (Generator, Detector, Judge). Extract costs, metrics, and handle errors.

**Acceptance Criteria**:
- [ ] Generator service callable with Python function
- [ ] Detector service callable with Python function
- [ ] Judge service callable with Python function
- [ ] All services return cost metrics (cost, tokens_used, latency_ms)
- [ ] Error handling captures and logs failures
- [ ] Service latency tracked in milliseconds

**Checklist**:
- [ ] Create `backend/app/services/__init__.py` (export all services)
- [ ] Create `backend/app/services/generator_service.py`
  - Function: `generate_email(phishing_type: str, **kwargs) -> dict`
  - Input: phishing_type (e.g., "credential_theft", "ceo_fraud")
  - Call: Hoang's Generator API/function
  - Output: Extract from response:
    - `subject` (str)
    - `body` (str)
    - `metadata` (dict) - headers, links, attachments
    - `latency_ms` (int)
    - `cost` (float) - USD
    - `model` (str) - model name
    - `tokens_used` (int)
  - Error handling: Capture failures, log, raise custom exception
- [ ] Create `backend/app/services/detector_service.py`
  - Function: `detect_phishing(email_content: str) -> dict`
  - Input: Full email (subject + body + metadata)
  - Call: Hoang's Detector API/function
  - Output: Extract from response:
    - `verdict` (str) - "phishing" or "legitimate"
    - `confidence` (float) - 0.0 to 1.0
    - `reasoning` (str)
    - `latency_ms` (int)
    - `cost` (float)
    - `model` (str)
    - `tokens_used` (int)
  - Error handling: Pause & Alert (see 2.4)
- [ ] Create `backend/app/services/judge_service.py`
  - Function: `evaluate(generated_email, detector_verdict, generator_verdict) -> dict`
  - Call: Hoang's Judge API/function
  - Output: Extract from response:
    - `ground_truth` (str) - "phishing" or "legitimate"
    - `is_correct` (bool)
    - `quality_score` (int) - 1-10
    - `feedback` (str)
    - `latency_ms` (int)
    - `cost` (float)
    - `model` (str)
- [ ] Create `backend/app/services/cost_service.py`
  - Function: `aggregate_email_cost(email_id) -> float`
  - Function: `aggregate_round_cost(round_id) -> float`
  - Function: `get_cost_summary() -> dict`
- [ ] Test: All services callable without errors
- [ ] Test: Cost extraction works correctly
- [ ] Test: Error handling captures failures

**Notes**: Blocker: Waiting for Hoang's agent implementations. API interface must be clarified first.

---

#### 2.2 Round Orchestration with Semantic Kernel
- **Priority**: 🔴 P0
- **Assigned To**: Bao Duy (SK Lead) with Hoang (Tech Lead mentoring)
- **Effort**: 5-6 hours
- **Timeline**: Week 2 (Monday-Wednesday)
- **Depends On**: 2.1 (service layer), 1.1 (Flask init)
- **Blocking**: 2.3, 2.4

**Description**:
Implement round execution orchestration using Semantic Kernel & OpenAI Agentic SDK with parallel workflow execution for Generator → Detector → Judge pipeline.

**Acceptance Criteria**:
- [ ] Can start round execution from API endpoint
- [ ] Semantic Kernel orchestrates all three agents in sequence per email
- [ ] Round status updates as emails process
- [ ] All results saved to database
- [ ] Parallel workflows execute correctly (2 emails processed simultaneously)
- [ ] Round completes without hanging or timeouts

**Checklist**:
- [ ] Create `backend/app/orchestration/__init__.py`
- [ ] Create `backend/app/orchestration/round_orchestrator.py`
  - Initialize Semantic Kernel kernel with OpenAI plugin
  - Define `orchestrate_round(round_id, total_emails)` function
  - Main loop: Process emails with parallel workflows (2 at a time)
  - For each email:
    - Call generator_service → get subject, body, metadata
    - Call detector_service → get verdict, confidence
    - Call judge_service → get ground truth, quality score
    - Save email record to database with all outputs
    - Update round.processed_emails counter
    - On error: Trigger "Pause & Alert" (see 2.3)
- [ ] Create Semantic Kernel plugins for each agent
  - `GeneratorPlugin`: wraps generator_service
  - `DetectorPlugin`: wraps detector_service
  - `JudgePlugin`: wraps judge_service
  - Each plugin standardizes input/output contracts
- [ ] Implement parallel workflow execution
  - Use OpenAI Agentic SDK for task scheduling
  - Run 2 email processing workflows in parallel
  - Wait for both to complete before processing next batch
  - Monitor and log execution progress
- [ ] Add round status polling support
  - API endpoint: `GET /api/rounds/{id}/status` returns current progress
  - Returns: processed_emails count, percent complete, last email processed
- [ ] Test: Orchestrate full round (10 emails, 2 parallel)
- [ ] Test: Verify all emails processed correctly
- [ ] Test: Verify database integrity after round completes

---

#### 2.3 Cost Tracking Implementation
- **Priority**: 🔴 P0
- **Assigned To**: Thien Quy (with Bao Duy support on SK integration)
- **Effort**: 3-4 hours
- **Timeline**: Week 2 (Thursday-Friday)
- **Depends On**: 2.1, 2.2 (orchestration)
- **Blocking**: None

**Description**:
Extract costs from API responses and implement cost tracking, aggregation, and reporting.

**Acceptance Criteria**:
- [ ] Cost extracted from all three agents
- [ ] Email cost = sum of three agent costs
- [ ] Round cost = sum of all email costs
- [ ] Cost data visible in API responses
- [ ] Cost calculation accurate within 0.01 USD

**Checklist**:
- [ ] Modify 2.1 (service layer) to extract cost from responses
  - Generator returns: `{"cost": 0.001, "tokens_used": 50, ...}`
  - Detector returns: `{"cost": 0.002, "tokens_used": 100, ...}`
  - Judge returns: `{"cost": 0.001, "tokens_used": 30, ...}`
- [ ] Store costs in database
  - Email model: `cost` field (sum of three)
  - Round model: `total_cost` field
  - API calls model: track individual call costs
- [ ] Create `backend/app/services/cost_service.py`
  - Function: `aggregate_email_cost(email_id) -> float`
    - Sum: generator_cost + detector_cost + judge_cost
  - Function: `aggregate_round_cost(round_id) -> float`
    - Sum: all email costs in round
  - Function: `get_cost_summary() -> dict`
    - Total cost, cost by agent type, cost by round, estimated monthly
- [ ] Update `GET /api/costs` endpoint to use aggregation functions
- [ ] Test: Cost aggregations match expected values
- [ ] Test: Monthly estimate reasonable based on usage

---

#### 2.4 Pause & Alert Error Handling
- **Priority**: 🔴 P0
- **Assigned To**: Hoang Nhat Duy (Tech Lead)
- **Effort**: 3-4 hours
- **Timeline**: Week 2 (Friday) + Week 3 (Monday)
- **Depends On**: 2.2 (orchestration), 2.3 (cost tracking)
- **Blocking**: 2.5

**Description**:
Implement error handling that pauses round execution on agent failures and alerts the client.

**Implementation** (Option A - Decided):
When any agent API call fails:
1. Log error with full context (request, response, stack trace)
2. Set round status to `failed`
3. Create error log entry
4. Return error via API (client can see what failed)

**Acceptance Criteria**:
- [ ] When agent API fails: round status → `failed`
- [ ] Error logged with full context
- [ ] Client can see error via API: `GET /api/rounds/{id}`
- [ ] Round stops processing (no more emails after error)
- [ ] Error includes: agent type, request, response, stack trace

**Checklist**:
- [ ] Create `backend/app/utils/exceptions.py`
  - Define: `GeneratorException`, `DetectorException`, `JudgeException`
  - All inherit from custom `AgentException`
- [ ] In Semantic Kernel orchestration workflow:
  - Wrap agent service calls in try/except block within plugins
  - On exception in generator: Log, set round.status = 'failed', stop workflow
  - On exception in detector: Log, set round.status = 'failed', stop workflow
  - On exception in judge: Log, set round.status = 'failed', stop workflow
  - Semantic Kernel handles exception propagation to stop execution
  - No further emails processed after error
- [ ] Create error log context structure:
  - Agent type (generator/detector/judge)
  - Request payload (sanitized)
  - Error message
  - Stack trace
  - Timestamp
  - Email ID being processed
- [ ] Update `GET /api/rounds/{id}` response to include error info
  - New field: `error` (object or null)
    - `agent_type`, `message`, `context`, `timestamp`
- [ ] Test: Simulate generator failure
- [ ] Test: Simulate detector timeout
- [ ] Test: Verify round status set to failed
- [ ] Test: Verify error visible in API response

---

#### 2.5 Round Execution E2E Test
- **Priority**: 🔴 P0
- **Assigned To**: Thien Quy (Testing Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 2 (Friday)
- **Depends On**: 2.2, 2.3, 2.4 (all three-agent integration and orchestration)
- **Blocking**: None

**Description**:
End-to-end test verifying full round lifecycle: start → execute → complete with data integrity.

**Acceptance Criteria**:
- [ ] Can trigger round via `POST /api/rounds`
- [ ] Round executes with 5 test emails
- [ ] All emails complete successfully
- [ ] Round status transitions: running → completed
- [ ] All metrics calculated (accuracy, generator_rate, avg_confidence, cost)
- [ ] Can retrieve all results via API

**Checklist**:
- [ ] Create `tests/test_e2e_round_execution.py`
- [ ] Setup: Create isolated test database, initialize Semantic Kernel
- [ ] Test 1: Start round with 5 emails
  - POST /api/rounds with total_emails=5
  - Verify response includes round_id, status=running
- [ ] Test 2: Poll round status until completed
  - Loop: GET /api/rounds/{id} every 0.5 seconds, timeout 60 seconds
  - Verify status transitions: running → completed
- [ ] Test 3: Verify 5 emails processed
  - GET /api/rounds/{id}/emails
  - Count: should be 5
- [ ] Test 4: Check round accuracy calculated
  - round.detector_accuracy > 0
  - round.detector_accuracy <= 1.0
- [ ] Test 5: Check costs calculated
  - round.total_cost > 0
  - Sum of email costs ≈ round.total_cost
- [ ] Test 6: Retrieve emails via GET /api/rounds/{id}/emails
  - Verify pagination works
  - Verify filters work (all, correct, incorrect, etc.)
- [ ] Test 7: Retrieve email details via GET /api/emails/{id}
  - Verify all fields present (generator, detector, judge outputs)
- [ ] Test 8: Verify all verdicts saved
  - generator_verdict (phishing|legitimate)
  - detector_verdict (phishing|legitimate)
  - judge_ground_truth (phishing|legitimate)
- [ ] Test 9: Verify override works
  - POST /api/emails/{id}/override
  - Verify round accuracy recalculated
- [ ] Test 10: Full data integrity check
  - No null verdicts
  - No missing costs
  - All relationships consistent

---

### BUCKET 3: TESTING & QA

#### 3.1 Unit Tests - Database Models
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead)
- **Effort**: 3-4 hours
- **Timeline**: Week 2-3 (as code is written)
- **Depends On**: Database models (already done)
- **Blocking**: None

**Description**:
Unit tests for all database models ensuring correctness of calculations and relationships.

**Acceptance Criteria**:
- [ ] Round model tests: creation, updates, accuracy calculation
- [ ] Email model tests: verdicts, false positives/negatives
- [ ] Log model tests: creation, filtering
- [ ] Test coverage: 95%+ for models

**Checklist**:
- [ ] Create `tests/test_models_round.py`
  - Test `Round.create()`
  - Test `round.update_metrics()`
  - Test `round.to_dict()` returns correct structure
  - Test relationships: `round.emails` loading
  - Test accuracy calculation: (correct / total) * 100
  - Test edge cases: all correct, all incorrect, empty round
- [ ] Create `tests/test_models_email.py`
  - Test `Email.create()` with all fields
  - Test `email.is_false_positive()` logic
  - Test `email.is_false_negative()` logic
  - Test `email.get_final_verdict()` logic
  - Test override fields populated correctly
- [ ] Create `tests/test_models_log.py`
  - Test `Log.create_log()` with context
  - Test log filtering by level
  - Test log filtering by round_id
  - Test timestamp ordering
- [ ] Create `tests/test_models_api_call.py`
  - Test API call cost tracking
  - Test agent type classification
- [ ] Run coverage report: `pytest --cov`
- [ ] Verify coverage > 95% for all models

**Tools**: pytest, pytest-fixtures

---

#### 3.2 Unit Tests - Services
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead) with Bao Duy (SK knowledge)
- **Effort**: 4-5 hours
- **Timeline**: Week 2-3
- **Depends On**: 2.1 (services implemented)
- **Blocking**: None

**Description**:
Unit tests for service layer with mocked API responses. Verify cost extraction, error handling, and business logic.

**Acceptance Criteria**:
- [ ] All services tested independently
- [ ] Agent responses mocked (no real API calls)
- [ ] Error scenarios tested (timeout, rate limit, parsing error)
- [ ] Test coverage: 90%+ for services

**Checklist**:
- [ ] Create `tests/test_services_generator.py`
  - Mock OpenAI/Anthropic response with realistic data
  - Test `generate_email()` function signature
  - Test cost extraction from response
  - Test metadata extraction
  - Test error handling: timeout
  - Test error handling: rate limit (429)
  - Test error handling: invalid response format
- [ ] Create `tests/test_services_detector.py`
  - Mock detector response
  - Test `detect_phishing()` verdict parsing
  - Test confidence score validation (0-1)
  - Test reasoning extraction
  - Test error handling: timeout, invalid verdict
- [ ] Create `tests/test_services_judge.py`
  - Mock judge response
  - Test quality score validation (1-10)
  - Test ground_truth extraction
  - Test is_correct boolean logic
- [ ] Create `tests/test_services_cost.py`
  - Test cost aggregation logic
  - Test cost by agent breakdown
  - Test estimated monthly projection
  - Test edge cases: zero cost, very high cost
- [ ] Run coverage: `pytest --cov`
- [ ] Verify coverage > 90%

**Tools**: pytest, unittest.mock, responses library for HTTP mocking

---

#### 3.3 Integration Tests - API Endpoints
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead) with Thanh Dang (API knowledge)
- **Effort**: 5-6 hours
- **Timeline**: Week 2-3
- **Depends On**: 1.2-1.4 (all endpoints), 2.2 (Semantic Kernel orchestration)
- **Blocking**: Phase 1 completion

**Description**:
Integration tests for all API endpoints using real database and mocked agents. Verify request/response contracts, pagination, filtering.

**Acceptance Criteria**:
- [ ] All API endpoints tested with real database
- [ ] Requests/responses match OpenAPI spec
- [ ] Pagination works correctly
- [ ] Filters return expected data
- [ ] Overrides update database correctly
- [ ] Test coverage: 85%+ for API routes

**Checklist**:
- [ ] Create `tests/test_api_rounds.py`
  - Test `POST /api/rounds` (201, request validation)
  - Test `GET /api/rounds` (pagination, sorting, filtering by status/created_by)
  - Test `GET /api/rounds/{id}` (200, 404 on missing)
  - Verify database records created
- [ ] Create `tests/test_api_emails.py`
  - Test `GET /api/rounds/{id}/emails` (all 5 filters)
  - Test `GET /api/emails/{id}` (all fields present, 404)
  - Test `POST /api/emails/{id}/override` (verdict update, validation)
  - Verify accuracy recalculation after override
- [ ] Create `tests/test_api_logs.py`
  - Test `GET /api/logs` (level, round_id, time range filters)
  - Test pagination
- [ ] Create `tests/test_api_costs.py`
  - Test `GET /api/costs` (totals, breakdowns by agent/round)
  - Test with zero costs (empty database)
- [ ] Create `tests/test_api_health.py`
  - Test `GET /api/health` (all components checked)
- [ ] Run coverage: `pytest --cov`
- [ ] Verify coverage > 85%

**Tools**: pytest, Flask test client, test fixtures

---

#### 3.4 E2E Tests - Error Scenarios
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 3
- **Depends On**: 2.4 (error handling implemented)
- **Blocking**: None

**Description**:
End-to-end tests for error handling ensuring graceful failure and recovery.

**Acceptance Criteria**:
- [ ] Round stops gracefully on agent failure
- [ ] Error is logged and visible in API
- [ ] Database remains consistent
- [ ] Partial round data saved correctly

**Checklist**:
- [ ] Create `tests/test_e2e_error_scenarios.py`
- [ ] Test: Generator API fails (mock exception)
  - Verify round status = failed
  - Verify error logged in logs table
  - Verify error visible in GET /api/rounds/{id}
  - Verify processed_emails = 0 (stopped immediately)
- [ ] Test: Detector API timeout
  - Verify round status = failed
  - Verify timeout error logged
- [ ] Test: Judge returns invalid response (malformed JSON)
  - Verify round status = failed
  - Verify parsing error logged
- [ ] Test: Database consistency
  - Verify no orphaned email records
  - Verify round status properly set
  - Verify logs created for all errors

---

#### 3.5 Code Coverage & Test Documentation
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead)
- **Effort**: 2-3 hours
- **Timeline**: Week 3 (Friday)
- **Depends On**: 3.1-3.4 (all tests)
- **Blocking**: Phase 1 completion

**Description**:
Finalize test coverage, generate reports, and document testing practices.

**Acceptance Criteria**:
- [ ] Overall code coverage ≥ 80%
- [ ] Critical paths (models, services) ≥ 95%
- [ ] Testing guide documented
- [ ] Coverage report generated

**Checklist**:
- [ ] Run coverage report: `pytest --cov=app --cov-report=html`
- [ ] Review htmlcov/index.html
- [ ] Identify untested code paths
- [ ] Add tests to reach 80% overall
  - Prioritize: Models (95%) > Services (90%) > Routes (80%)
- [ ] Create `TESTING.md` documentation
  - How to run all tests: `pytest`
  - How to run specific test file: `pytest tests/test_api_rounds.py`
  - How to check coverage: `pytest --cov=app --cov-report=html`
  - How to create mock fixtures
  - Coverage requirements by module
  - Common test patterns and examples
- [ ] Verify coverage ≥ 80% before Phase 1 close

---

### BUCKET 4: DATABASE SCHEMA & MIGRATION LEARNING

#### 4.1 Database Schema Review & Documentation
- **Priority**: 🔴 P0
- **Assigned To**: Bao Duy (Database foundation)
- **Effort**: 2-3 hours
- **Timeline**: Week 1 (Friday) + Week 2 (Monday)
- **Depends On**: None (models already exist)
- **Blocking**: None

**Description**:
Review and document the existing database schema to understand structure, relationships, and design decisions.

**Acceptance Criteria**:
- [ ] All 5 tables documented with purpose and fields
- [ ] Relationships between tables clearly explained
- [ ] Table diagrams created (ER diagram)
- [ ] Field types and constraints documented

**Checklist**:
- [ ] Review existing migration file: `backend/migrations/versions/f68964d2d980_initial_schema.py`
  - Understand what tables were created
  - Understand field types (String, Integer, DateTime, etc.)
  - Understand constraints (nullable, default values)
- [ ] Create `DATABASE_SCHEMA.md` documentation with sections:
  - [ ] **Round Table**
    - purpose: Tracks each adversarial training round
    - fields: id, baseline, email_count, status, metrics, created_at, updated_at
    - relationships: Has many Emails, Logs, APICall records
  - [ ] **Email Table**
    - purpose: Stores individual email data and verdicts
    - fields: id, round_id, generator_verdict, detector_verdict, judge_ground_truth, override fields
    - relationships: Belongs to Round, has Override, has multiple APICall entries
  - [ ] **Log Table**
    - purpose: System event logging with context
    - fields: id, round_id, level, message, context (JSONB), created_at
    - relationships: Belongs to Round (optional)
  - [ ] **APICall Table**
    - purpose: Track individual agent API calls and costs
    - fields: id, round_id, email_id, agent_type, cost, tokens_used, latency_ms
    - relationships: Belongs to Round and Email
  - [ ] **Override Table**
    - purpose: Manual verdict corrections by human reviewers
    - fields: id, email_id, verdicts, reason, overridden_by, created_at
    - relationships: Belongs to Email
- [ ] Create Entity Relationship (ER) diagram
  - Visualize table relationships (1-to-many, many-to-1)
  - Show foreign keys
  - Use text format or tool like: `backend/DATABASE_ER_DIAGRAM.md` (ASCII art or reference to Excalidraw)
- [ ] Verify schema matches model definitions
  - Check: `backend/app/models/*.py` match migration
  - Document any discrepancies found

---

#### 4.2 Writing Custom Migrations
- **Priority**: 🔴 P0
- **Assigned To**: Bao Duy (Hands-on learning)
- **Effort**: 3-4 hours
- **Timeline**: Week 2 (Wednesday-Thursday)
- **Depends On**: 1.1, 1.2, 1.3, 1.4 (API endpoints working)
- **Blocking**: None

**Description**:
Learn how to write and apply custom migrations for schema changes using Alembic.

**Acceptance Criteria**:
- [ ] Understand Alembic migration structure
- [ ] Can generate and test migrations
- [ ] Migrations apply cleanly without errors
- [ ] Can roll back migrations if needed

**Checklist**:
- [ ] Review existing migration: `backend/migrations/versions/f68964d2d980_initial_schema.py`
  - Understand structure: `upgrade()` and `downgrade()` functions
  - Understand table creation syntax
  - Understand constraint definitions
- [ ] Create a sample migration (for learning):
  - Command: `cd backend && alembic revision -m "add_sample_column"`
  - Creates new file in `backend/migrations/versions/`
  - File contains empty `upgrade()` and `downgrade()` functions
  - **Task**: Add a new column to Round table (e.g., `notes` TEXT field)
    - In `upgrade()`: use `op.add_column('round', sa.Column('notes', sa.String(), nullable=True))`
    - In `downgrade()`: use `op.drop_column('round', 'notes')`
  - Test: Run `alembic upgrade head` - should apply successfully
  - Test: Run `alembic downgrade -1` - should remove the column
  - Test: Run `alembic upgrade head` again - should re-add the column
  - Delete this sample migration (revert git changes)
- [ ] Understand common migration operations:
  - `op.add_column()` - add new field to table
  - `op.drop_column()` - remove field
  - `op.alter_column()` - modify field properties (type, nullable)
  - `op.create_index()` / `op.drop_index()` - add/remove indexes
  - `op.execute()` - run raw SQL for custom operations
- [ ] Document sample migration patterns in `MIGRATION_GUIDE.md`
- [ ] Learn rollback mechanics
  - Understand downgrade() functions are critical for reverting changes
  - Test rolling back the sample migration

---

#### 4.3 Database Constraints & Data Validation
- **Priority**: 🟡 P1
- **Assigned To**: Bao Duy (Database learning)
- **Effort**: 2-3 hours
- **Timeline**: Week 2 (Friday) + Week 3 (Tuesday)
- **Depends On**: 4.1 (schema understood)
- **Blocking**: None

**Description**:
Review database constraints, understand how they enforce data integrity, and identify potential validation gaps.

**Acceptance Criteria**:
- [ ] All foreign key relationships understood
- [ ] Constraint types identified (PK, FK, NOT NULL, defaults)
- [ ] Validation logic in models aligned with database constraints

**Checklist**:
- [ ] Query database to see actual constraints:
  - Command in psql: `\d round` (shows column definitions and constraints)
  - Command: `SELECT * FROM information_schema.key_column_usage WHERE table_name='round';`
  - Command: `SELECT * FROM information_schema.table_constraints WHERE table_name='round';`
- [ ] Document constraints found:
  - [ ] Primary keys (all have id INT PRIMARY KEY)
  - [ ] Foreign keys defined
    - Email.round_id → Round.id
    - Log.round_id → Round.id (nullable)
    - APICall.round_id → Round.id (nullable)
    - Override.email_id → Email.id
  - [ ] NOT NULL constraints on required fields
  - [ ] Default values (e.g., created_at defaults to NOW())
- [ ] Review SQLAlchemy model definitions
  - Verify model fields match database columns
  - Check `nullable=False` in models match NOT NULL in database
  - Review relationships defined in models
- [ ] Create `DATABASE_VALIDATION.md` doc:
  - List all constraints and what they protect against
  - Examples: Why delete a Round should delete related Emails
  - Explain cascade delete strategy
- [ ] Test constraint enforcement:
  - Try to insert Round with NULL status → should fail
  - Try to insert Email with invalid round_id → should fail
  - Try to delete Round with related Emails → should cascade delete
  - Document results

---

#### 4.4 Database Querying & Testing
- **Priority**: 🟡 P1
- **Assigned To**: Bao Duy (with Thien Quy on testing)
- **Effort**: 2-3 hours
- **Timeline**: Week 3 (Wednesday-Thursday)
- **Depends On**: 1.2, 1.3, 1.4 (API endpoints written), 4.1 (schema known)
- **Blocking**: None

**Description**:
Learn how to query the database directly to inspect data, verify migrations, and test data integrity.

**Acceptance Criteria**:
- [ ] Can query database with SQL and SQLAlchemy ORM
- [ ] Understand difference between SQL queries and ORM queries
- [ ] Can inspect data to verify API operations work correctly

**Checklist**:
- [ ] Learn basic PostgreSQL queries (in psql):
  - `SELECT * FROM round;` - view all rounds
  - `SELECT * FROM email WHERE round_id = 1;` - filter emails by round
  - `SELECT COUNT(*) FROM email;` - count total emails
  - `SELECT DISTINCT status FROM round;` - see unique statuses
  - `SELECT * FROM email WHERE detector_verdict IS NULL;` - find nulls
- [ ] Learn SQLAlchemy ORM queries:
  - `Round.query.all()` - get all rounds
  - `Round.query.filter_by(status='completed').all()` - filter
  - `db.session.execute(db.select(Round).where(Round.status == 'running'))` - modern syntax
  - `round.emails` - navigate relationships (get emails for a round)
  - `db.session.query(Email).count()` - count with ORM
- [ ] Create test queries script: `backend/test_queries.py`
  - Script that demonstrates various query patterns
  - Comments explaining what each query does
  - Run after API operations to verify data was saved
  - Examples:
    - Query: Get all emails from last round
    - Query: Count emails by verdict
    - Query: Find emails missing judge verdict
    - Query: Total cost across all rounds
- [ ] Manual testing workflow:
  - Start Flask app
  - Call API: `POST /api/rounds` (create round)
  - Call API: `GET /api/rounds` (list rounds)
  - Run test_queries.py to inspect database directly
  - Verify data matches API responses
  - Document findings
- [ ] Create `DATABASE_QUERY_GUIDE.md` with:
  - Common SQL queries and their ORM equivalents
  - How to connect to database directly (psql connection string)
  - When to use SQL vs ORM
  - Debugging tips (checking what queries ORM generates)

---

#### 4.5 Migration Testing & Rollback Practice
- **Priority**: 🟡 P1
- **Assigned To**: Hoang Nhat Duy (with Bao Duy)
- **Effort**: 2 hours
- **Timeline**: Week 3 (Friday)
- **Depends On**: 4.2 (migrations understood), 4.4 (can query database)
- **Blocking**: None

**Description**:
Practice applying, testing, and rolling back migrations to ensure migration safety and understand version control.

**Acceptance Criteria**:
- [ ] Can apply migrations with confidence
- [ ] Understand migration history
- [ ] Can rollback if migration fails
- [ ] Migration workflow documented

**Checklist**:
- [ ] Review migration history:
  - Command: `cd backend && alembic current` - shows current migration
  - Command: `alembic history` - shows all migrations applied
  - Command: `alembic branches` - shows any migration branches (should be none)
- [ ] Learn migration commands:
  - `alembic upgrade head` - apply all pending migrations
  - `alembic upgrade +1` - apply next one migration
  - `alembic downgrade -1` - rollback last migration
  - `alembic downgrade base` - rollback all back to schema creation
  - `alembic revision --autogenerate -m "message"` - generate migration from model changes
- [ ] Practice rollback scenario:
  - Query database current state: `SELECT COUNT(*) FROM round;`
  - Rollback: `alembic downgrade -1`
  - Verify: `alembic current` shows older version
  - Query database: schema should be older
  - Re-apply: `alembic upgrade head`
  - Verify back to current state
  - Document what changed at each step
- [ ] Create migration safety checklist: `MIGRATION_SAFETY.md`
  - Always backup database before running migrations on production
  - Test migrations on development/test database first
  - Reversibility: ensure downgrade() function exists and tested
  - Data safety: be careful with drop_column (data is lost), use nullable first
  - Review all migrations before applying
- [ ] Document common migration patterns:
  - Adding optional field (new column, nullable=True)
  - Removing field (drop_column)
  - Renaming field (requires downgrade to handle)
  - Changing field type (risky, test carefully)
  - Adding constraint (safe if data already valid)

---

### BUCKET 5: PERFORMANCE & DEPLOYMENT

**Focus**: Production-readiness features - caching optimization, containerization, security hardening, and load testing

#### 5.1 Redis Caching Strategy Implementation
- **Priority**: 🟡 P1
- **Assigned To**: Bao Duy (Secondary) with Hoang review
- **Effort**: 2-3 hours
- **Description**: Implement TTL-based caching for LLM API responses and repeated database queries. Set cache invalidation strategies, handle cache miss scenarios.

#### 5.2 Docker & Docker Compose Containerization
- **Priority**: 🟡 P1
- **Assigned To**: Thanh Dang (Infrastructure Lead)
- **Effort**: 4-5 hours
- **Description**: Create Dockerfile for Flask app, docker-compose.yml for full stack (Flask + PostgreSQL + Redis). Build, test, document run commands. Test with multiple containers.

#### 5.3 Security Hardening & Input Validation
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Security Lead)
- **Effort**: 3-4 hours
- **Description**: Implement CSRF protection, SQL injection prevention, XSS protection. Validate all user inputs. Test security vulnerabilities. Document security approach.

#### 5.4 Load Testing & Performance Baseline
- **Priority**: 🟡 P1
- **Assigned To**: Thien Quy (Testing Lead)
- **Effort**: 2-3 hours
- **Description**: Use locust/Apache JMeter to simulate concurrent requests. Measure response times, throughput, error rates. Document baseline metrics (target: handle 10+ concurrent rounds).

---

### BUCKET 6: FRONTEND SCAFFOLDING & PLANNING

**Note**: This bucket is for **scoping only**. Frontend development starts AFTER Phase 1 backend completes.

**Note**: API documentation (Swagger UI, development guides, architecture docs) will be handled in Phase 1.5 or Phase 2 once the core backend is stable and the API contract is finalized. This allows for more accurate examples and documentation.

**Cards to create in Planner** (as placeholders for visibility):
- [ ] React + Vite Setup
- [ ] Home Dashboard Component (static mockup)
- [ ] Rounds List View Component
- [ ] Round Detail View Component
- [ ] Email Detail View Component
- [ ] Logs View Component
- [ ] Cost Dashboard Component
- [ ] Navigation & Routing (React Router)
- [ ] Charts & Data Visualization (Chart.js)
- [ ] Error Handling & User Feedback
- [ ] WebSocket Integration (Nice-to-have, Phase 1.5)
- [ ] Styling & UI Polish

---

## Task Dependencies & Critical Path

```
CRITICAL PATH (must complete in order):
1. Flask App Init (1.1) - Week 1 Mon-Tue
   ↓
2. API Endpoints - Rounds (1.2), Logs (1.4), Health (1.4) - Week 1 Wed-Fri
   ↓
3. Service Layer (2.1) - Week 1-2
   ↓
4. Semantic Kernel Orchestration (2.2) - Week 2 Mon-Wed
   ↓
5. Cost Tracking (2.3) & Error Handling (2.4) - Week 2 Thu-Fri
   ↓
6. Round Execution E2E Test (2.5) - Week 2 Fri
   ↓
7. API Integration Tests (3.3) - Week 2-3
   ↓
8. Database Schema & Migrations Learning (4.1, 4.2, 4.3) - Week 1-3

PARALLEL TRACKS (can run simultaneously):
- Error Handling (1.5) after Flask init
- API Endpoints - Emails (1.3) after Rounds
- Database Constraints (4.3) during Week 2
- Database Querying & Testing (4.4) during Week 3
- Unit Tests (3.1, 3.2) start mid-week as code is written
```

---

## Risk Assessment & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Three-agent APIs not ready** | Blocks 2.2-2.5 | Mock agents first, swap when ready. Weekly checkin with Hoang. |
| **Semantic Kernel setup fails** | Blocks round execution | Use mock orchestration for testing. Document fallback approach. |
| **Redis cache fails** | Performance impact only | Gracefully degrade to direct database queries. Log cache misses. |
| **Cost extraction from APIs complex** | Budget tracking broken | Start with manual cost entry, iterate. Document API response format clearly. |
| **API failures are frequent** | Round hangs | Implement retry logic + timeouts. Test failure scenarios. |
| **Team communication gaps** | Duplicate work, integration issues | Daily 15-min standups. Shared task board. Weekly syncs. |
| **Test data generation** | Tests flaky | Use fixtures. Mock external APIs. Use factories for test data. |
| **Time estimates off** | Slipped deadline | Buffer in Week 4. Prioritize critical path. Re-estimate mid-week. |

---

## Notes & Assumptions

- **Python Version**: 3.9+ (as per requirements.txt)
- **Database**: PostgreSQL (migrations already run via `alembic upgrade head`)
- **Task Orchestration**: Semantic Kernel + OpenAI Agentic SDK (parallel workflows)
- **Caching**: Redis for LLM response caching and database query result caching
- **Agent APIs**: Callable as Python functions via Hoang's implementations
  - Must return cost, latency, model, tokens_used in response
  - Error handling via exceptions
- **No authentication**: Internal tool for team only
- **No email persistence**: Generated emails not archived, only metadata stored
- **Polling, not WebSocket**: Real-time updates via polling initially (WebSocket = Phase 1.5)
- **Caching Strategy**: Redis for expensive LLM API call responses + repeated database queries (TTL-based expiration)

---

## Appendix: Technology Stack

**Backend Framework**: Flask 3.1.2  
**ORM**: SQLAlchemy 2.0.46  
**Task Orchestration**: Semantic Kernel 1.0+ with OpenAI Agentic SDK  
**Database**: PostgreSQL with Alembic migrations  
**Cache**: Redis 7+ (LLM response caching + query result caching)  
**API Specs**: OpenAPI 3.0 (YAML)  
**Testing**: pytest 9.0.2, coverage 7.13.2  
**Code Quality**: black, flake8, pylint, mypy (optional)  
**API Documentation**: Swagger UI (flasgger or flask-swagger-ui)

---

## Sample Planner Card Template

Use this template when creating cards in Microsoft Planner:

```
Title: [BUCKET #] Task Name

Priority: 🔴 P0 / 🟡 P1 / 🟢 P2

Assigned To: Developer Name

Effort: 2-3 hours

Timeline: Week X (specific days)

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Checklist:
- [ ] Subtask 1
- [ ] Subtask 2
- [ ] Subtask 3

Dependencies:
Depends On: [Other card titles]
Blocking: [Other card titles]
```

---

**Document Version**: 2.0 (Consolidated)  
**Last Updated**: Feb 9, 2026  
**Next Review**: End of Week 1  
**Maintained By**: Hoang Nhat Duy (Project Lead)
