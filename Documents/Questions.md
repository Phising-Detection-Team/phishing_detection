# Email Security Detection System - Project Scoping Questionnaire

## Purpose
This questionnaire will help you define clear objectives, scope, and requirements for your real-time email threat detection system. Complete this document collaboratively with your team to ensure alignment before development begins.

---

## Section 1: Project Vision & Goals

### 1.1 Problem Statement
- **What specific problem are you trying to solve?**
  - [x] Answer: To automatically detect and verify whether an incoming email is legitimate or a phishing attempt, reducing the reliance on human judgment.

- **Who is experiencing this problem?**
  - [x] Answer: Individuals and small business employees who frequently use email but lack advanced cybersecurity awareness to identify sophisticated threats.

- **What are the consequences if this problem isn't solved?**
  - [x] Answer: Users risk compromising their private information (credentials, financial data) and assets, leading to potential identity theft or financial loss.

- **Why are existing solutions (Gmail spam filters, Microsoft Defender, commercial tools) insufficient?**
  - [x] Answer: Attackers continuously evolve their techniques (e.g., social engineering, zero-day exploits) to bypass the static rule-based filters and authentication layers of existing tools.

### 1.2 Project Objectives
- **What is the primary goal of this project?** (Choose one)
  - [ ] Proof of concept / Technical demonstration
  - [x] Portfolio project to showcase skills
  - [x] Production-ready tool for real users -> This is the main goal
  - [ ] Research project / Academic work
  - [ ] Foundation for a startup/commercial product
  - [ ] Other: _______________

- **What does success look like?** (Be specific)
  - [x] Answer: The AI models successfully verifies emails in real-time with historical sets of training datas (described in The Two-Model Approach with a judgement Model/Human Override sections), detecting potential threats with high accuracy and sending immediate, clear flags to the user.

- **What are your top 3 must-have features?**
  1. AI-based Phishing Detection Model (Final Training Dataset after all the rounds for a Frontier/Open-Source model)
  2. Real-time Content Scripts for continuous monitoring (browser extension stage?!)
  3. Instant Alert and Notification System (Mobile/Web)

- **What are nice-to-have features that could be added later?**
  - Recommendation system - Educational tips to help users recognize future threats based on the specific type of attack detected.

### 1.3 Success Metrics
How will you measure if the project is successful?

- **Technical metrics:**
  - **Notes**: 
        - Precision: “Of all the scam emails items the model predicted as scam, how many were actually scam?”
        - Recall: “Of all the actual scam emails, how many did the model correctly detect?”

  - [x] Detection accuracy (target: > 85% precision, > 80% recall)
  - [x] False positive rate (target: less than 5%)
  - [x] Detection speed (target: within 5 seconds)
  - [x] System uptime (target: 99%)
  - [ ] Other: _______________

- **User metrics:**
  - [x] User satisfaction score (Survey based)
  - [x] Number of threats successfully blocked
  - [x] Reduction in successful attacks (simulated or real)
  - [x] User engagement with alerts (Click-through rate on warnings - Future Enhancements on On-click behavior)
  - [ ] Other: _______________

---

## Section 2: Target Users & Stakeholders

### 2.1 Primary Users
- **Who will use this system?** (Choose all that apply)
  - [x] Individual users (personal email protection) -> Chose
  - [x] Small business owners -> Chose
  - [ ] IT administrators
  - [x] Security operations teams -> Chose
  - [ ] Enterprise organizations
  - [ ] Other: _______________

- **Create a user persona** (describe your ideal user in 3-5 sentences):
  - **Name/Role:** Sarah, Retail Store Manager
  - **Background:** Manages daily operations and communicates with suppliers via email on both mobile and desktop.
  - **Pain points:** Receives high volumes of invoices and orders; worries about accidentally clicking a fake invoice that could compromise the store's network.
  - **Technical proficiency:** Basic digital literacy; knows how to use email and browsers but lacks technical security knowledge.
  - **Goals:** Wants a "set it and forget it" tool that warns her clearly before she makes a mistake.

### 2.2 Stakeholders
- **Who needs to understand/approve this project?**
  - [x] Technical stakeholders: Project Supervisor / Mentor (Le Hoang Nhat Duy)
  - [ ] Business stakeholders: N/A (Self-funded/Student Project)
  - [x] End users: Beta testers (Classmates, Friends)
  - [ ] Investors/Advisors: _______________

- **What does each stakeholder group care most about?**
  - **Technical:** Code quality, Testing cases coverage, architecture scalability, and model accuracy.
  - **Business:** (N/A)
  - **Users:** Ease of use, low false positives (don't block real emails), and speed.

---

## Section 3: Technical Architecture & Infrastructure

### 3.1 Deployment Model
- **Where will this system run?**
  - [ ] Cloud (AWS, Azure, GCP) - Which provider? _______________
  - [ ] On-premise servers
  - [ ] Hybrid (cloud + on-premise)
  - [ ] User's local machine
  - [x] Not yet decided -> Let's discuss about this. End goal is for Browser Extension and we are not familiar how to proceed with this.

- **What is your expected scale?**
  - [x] Number of users: 50+
  - [x] Number of email accounts monitored: 50+
  - [x] Emails processed per day: 50+
  - [x] Expected growth over 6 months: 200+ users

### 3.2 Email Integration
- **Which email providers must you support?**
  - [ ] Gmail (consumer)
  - [ ] Google Workspace
  - [ ] Microsoft 365 / Outlook.com
  - [ ] Exchange Server
  - [ ] Yahoo Mail
  - [ ] Custom/Corporate IMAP servers
  - [x] Other: We plan to use Content Script to support Browser Extension. Out of the above options, which one can we support?

- **Authentication method:**
  - [x] OAuth2 (recommended for Gmail/Microsoft)
  - [ ] IMAP username/password
  - [x] API-based (Gmail API, Microsoft Graph API)

- **What email data will you access?**
  - [ ] Headers only
  - [ ] Headers + body text
  - [x] Headers + body + attachments 
  - [ ] Metadata only (sender, timestamp, subject)

- **Real-time monitoring requirements:**
  - [ ] Check frequency: Every 15 minutes
  - [x] Processing latency target: Detect threats within 10 seconds
  - [ ] Historical scan needed? (analyze past emails): No

### 3.3 Technology Stack
- **What technologies are you committed to using?**
  - **Programming language:** Python
  - **ML/AI framework:** PyTorch or TensorFlow (for model training), Scikit-learn. Not for now, might be used for model training later.
  - **Backend framework:** FastAPI (for high performance) or Flask
  - **Database:** PostgreSQL (Metadata), Redis (caching/queue)
  - **Frontend:** React - Next.js or Vite
  - **Deployment/Orchestration:** Docker, Docker Compose - as mentioned above, let's discuss more on this

- **Are there any technology constraints?** (e.g., must use specific cloud provider, must be open-source, etc.)
  - [x] Answer: Must use GitHub for version control

### 3.4 System Architecture Questions
- **Will this be:**
  - [ ] Real-time streaming system (continuous monitoring)
  - [ ] Batch processing system (periodic scans)
  - [x] Hybrid (real-time + scheduled deep scans) - Let's see how possible it is after first iteration.

- **How will you handle high email volumes?**
  - [ ] Queue-based processing
  - [ ] Parallel processing
  - [x] Prioritization (check high-risk emails first)
  - [ ] Not yet decided

- **Do you need a web interface/dashboard?**
  - [ ] Yes, for end users
  - [x] Yes, for administrators only
  - [ ] No, command-line/API only
  - [ ] Not yet decided -> Chose (Likely yes, for users to view logs)

---

## Section 4: Threat Model & Detection Scope

### 4.1 Threat Categories
**What specific threats will you detect?** (Rank by priority: 1=highest)

- [x] Priority _1_: **Phishing** (credential theft, fake login pages)
- [x] Priority _2_: **Spear phishing** (targeted attacks, CEO fraud)
- [x] Priority _2_: **Business Email Compromise (BEC)**
- [x] Priority _1_: **Malware/ransomware attachments**
- [x] Priority _1_: **Social engineering** (urgency tactics, authority impersonation)
- [x] Priority _2_: **Account takeover** (suspicious sending behavior)
- [x] Priority _2_: **Data exfiltration** (unusual outgoing emails)
- [x] Priority _3_: **Spam** (general unwanted emails)

### 4.2 Detection Direction
- **What email traffic will you analyze?**
  - [x] Incoming emails only -> Chose
  - [ ] Outgoing emails only
  - [ ] Both incoming and outgoing
  - [ ] Internal emails (within organization)

### 4.3 "Unusual Patterns" Definition
**What constitutes an "unusual pattern"?** (Be specific - this is critical for building the detection model): 

- **Sender-based signals:**
  - [x] Unknown/new sender (first time contact)
  - [x] Spoofed sender address (mismatch between display name and actual email)
  - [x] Sender domain reputation (domain age < 30 days)
  - [x] Geolocation anomalies (login/send from unusual country)

- **Content-based signals:**
  - [x] Urgency/pressure language ("act now", "verify immediately", "overdue payment")
  - [x] Requests for sensitive information (passwords, bank details)
  - [x] Grammar/spelling errors inconsistent with corporate templates
  - [x] Brand impersonation (using logos of banks/tech companies)

- **Technical signals:**
  - [x] Suspicious URLs/domains (typosquatting, e.g., "g0ogle.com")
  - [x] Malicious attachment types (.exe, .scr, macro-enabled .doc)
  - [x] SPF/DKIM/DMARC failures
  - [x] Everything before the final "@" in a URL is treated as userinfo (credentials) and is not used to determine the destination host.

- **Behavioral signals (requires baseline):**
  - [x] User never emails this sender
  - [x] Unusual sending time (e.g., 3 AM local time)
  - [x] Atypical email volume (bulk sending)

### 4.4 Baseline & Personalization
- **Will the system learn individual user behavior?**
  - [ ] No, general detection model for all users
  - [x] Yes, personalized baselines (e.g., who the user usually communicates with)

- **If personalized, what is the training period?**
  - [x] 14 days of normal email history needed (or analyze last 500 emails).

---

## Section 5: The Two-Model Approach

### 5.1 Model 1: Phishing Email Generator
- **Why are you building a generative model?** (Choose all that apply)
  - [x] Generate synthetic training data (to augment limited real phishing samples)
  - [x] Red team simulations (help users train to recognize phishing)

- **What data will you use to train the generative model?**
  - [x] Public phishing datasets (e.g., PhishTank, OpenPhish)
  - [ ] Historical phishing emails from organization

- **Ethical and security safeguards:**
  - [x] How will you prevent misuse? The generator will be containerized with no external network access to send emails.
  - [x] Will generated emails be watermarked? Yes, all generated content will have a specific metadata tag.
  - [x] Who will have access? Only the development team.
  - [x] Let's discuss more on how we can guardrail this model to ensure moral considerations.

### 5.2 Model 2: Detection/Classification Model
- **What type of model are you building?**
  - [x] Multi-class classifier (phishing, spam, malware, legitimate)
  - [ ] Anomaly detection model

- **What features will the model analyze?**
  - [x] Email text (NLP-based features via BERT/RoBERTa)
  - [x] Email headers
  - [x] URLs and links
  - [x] Sender metadata

- **What ML techniques are you considering?**
  - [ ] Deep learning (Transformers - BERT/DistilBERT)
  - [ ] Traditional ML (Random Forest for metadata analysis)
  - [x] Not yet decided -> For now we need synthetic dataset first for final training

### 5.3 Model Integration
- **Will both models work together in production?**
  - [x] No - Model 1 is only for training/testing. Model 2 should be production-ready after the training.
  - [] Yes - Model 1 generates edge cases to continuously retrain Model 2 (Adversarial Training)

- **How often will models be retrained/updated?**
  - [ ] Real-time learning (continuous updates) -> Chose
  - [ ] Daily
  - [x] Weekly -> Chose (Scheduled batch retraining) - redeployment for detection model if needed

---

## Section 6: Data & Privacy

### 6.1 Data Collection
- **What email data will you collect and store?**
  - [x] Full email content (headers + body + attachments) -> Chose
  - [ ] Metadata only (sender, timestamp, subject, labels)

- **How long will data be retained?**
  - [ ] Stored for training purposes (3 months) -> Chose
  - [x] for now if needed, we can generate more test emails from Model 1. Let's discuss on this if we need real emails from user.

### 6.2 Privacy & Compliance
- **What regulations apply to your project?**
  - [ ] GDPR (European Union)
  - [ ] HIPAA (healthcare data)
  - [ ] None / Not applicable (Student Project)
  - [x] Not sure - need to research -> Chose (Will follow GDPR principles as a best practice - this is still a student project just FYI)

- **How will you obtain user consent?**
  - [x] Answer: Implementing a clear Terms of Service and Privacy Policy agreement that users must digitally sign/accept upon account creation.

- **Will email data be encrypted?**
  - [x] At rest: Yes (AES-256)
  - [x] In transit: Yes (TLS 1.2+)

- **Where will data be stored geographically?**
  - [x] Answer: Local database initially, potentially AWS region (e.g., US-East) if cloud deployed.

- **Will you share data with third parties?**
  - [x] No

### 6.3 Training Data Sources
- **Where will you get training data for your models?**
  - [x] Public datasets (PhishTank, Enron Email Dataset)
  - [x] Synthetic data (generated by Model 1)

- **How will you ensure training data quality and balance?**
  - [x] Answer: We will perform data cleaning to remove duplicates and balance the classes (phishing vs. legit) using oversampling/undersampling techniques.

---

## Section 7: User Experience & Alerts

### 7.1 Alert Delivery
- **How will users receive threat notifications?**
  - [ ] Email notification
  - [ ] Push notification (mobile app) -> Chose
  - [ ] SMS
  - [ ] Web dashboard -> Chose
  - [x] Browser extension -> Chose

- **Alert urgency levels:**
  - [x] Will you have different severity levels? Yes (Critical, Warning, Info)
  - [x] What determines urgency? Probability score from the AI model (e.g., >90% = Critical).

### 7.2 User Actions
**What can users do when they receive an alert?**
  - [x] Mark as false positive (safe) - This retrains the model.
  - [x] Confirm threat and quarantine.
  - [x] Delete email permanently.
  - [x] Block sender.

### 7.3 User Onboarding
- **What does the user setup process look like?**
  1. Register account on the web dashboard.
  2. Input IMAP credentials (or App Password) for their email provider.
  3. System runs an initial "historical scan" to build a baseline.

- **Does the system need a training/calibration period?**
  - [ ] Yes - 24 hours for initial baseline.
  - [x] No - only check future emails incoming.

- **How will you minimize false positives during initial use?**
  - [x] Answer: Set the detection threshold higher (more conservative) for the first week so only obvious threats are flagged. Let's discuss more on this on how we can set this parameter.

### 7.4 Interface Requirements
- **Do you need a user interface?**
  - [x] Not yet decided -> Chose (Will likely build a Simple Web Dashboard using Streamlit or React).

---

## Section 8: Project Constraints & Resources

### 8.1 Timeline
- **What is your project timeline?**
  - [x] Start date: 01/29/2025
  - [x] Target completion date: 1 month
  - [x] Key milestones:
    - Milestone 1: Data collection & Model Training (Date: TBD + 2 weeks)
    - Milestone 2: Backend API & Database Setup for Data Collection
    - Milestone 3: UI Development & Integration Testing (Date: TBD + 6 weeks)

### 8.2 Team & Skills
- **Who is on your team?**
  - [x] Team member 1: Le Hoang Nhat Duy (Supervisor/Expert)
  - [x] Team member 2: Le Hoang Bao Duy (Supervisor/Expert)
  - [x] Team member 3: Pham Thien Quy (Cybersecurity Analyst/Developer)

- **What skills do you have?**
  - [x] Machine learning / AI (Python, Libraries)
  - [x] Full Stack development (API design)
  - [x] LLM and Agentic Workflow
  - [x] Cybersecurity (Threat analysis)

- **What skills are you missing?**
  - [x] Answer: Legal/Compliance expertise for Student Project Scope.

### 8.3 Budget
- **What is your budget?**
  - [x] No budget / Free tier only -> Chose (Will use open-source tools and free tiers of cloud services).

### 8.4 Non-Negotiable Constraints
  - 1. Must ensure user privacy (no leaking emails).
  - 3. Must be completed within the semester timeline.

---

## Section 9: Competitive Analysis & Differentiation

### Skip due to this is just a Student Project, not a commercial project.
---

## Section 10: Use Cases & Scenarios

### 10.1 Primary Use Case
**Scenario:** Small business owner receives targeted phishing email.

**Step-by-step flow:**
1. User receives suspicious email at 9:00 AM disguised as a vendor invoice.
2. System detects the email via IMAP within 30 seconds.
3. Model analyzes email; detects "Urgency" keyword and "Spoofed Domain".
4. User receives push notification: "Critical: Potential Phishing Detected".
5. User opens notification and sees threat details (e.g., "Sender domain does not match official vendor").
6. User clicks "Quarantine" button.
7. Email is moved to a local quarantine folder.
8. Sender is added to the personal blacklist.
9. Incident is logged for reporting.

### 10.2 Additional Scenarios
**Scenario 2: False Positive Handling**
- A legitimate urgent email from a new client is flagged as "Suspicious". The user reviews the alert, marks it as "Safe". The system updates the user's whitelist and retrains the model with this new example to prevent future errors.

**Scenario 3: Zero-Day Malware**
- An email contains a never-before-seen attachment type. The system's anomaly detector identifies the file structure as "Unusual" compared to the user's history and quarantines it pending manual review.

### 10.3 Edge Cases
- [x] Foreign language emails (requires multi-lingual NLP model).
- [x] Forwarded emails (headers might be messy).
- [x] Newsletters/marketing emails (often look like spam but are safe).

---

## Section 11: Testing & Validation

### 11.1 Testing Strategy
- **How will you test the detection model?**
  - [x] Hold-out test set from training data (80/20 split).
  - [x] Comparison against known phishing datasets.
  - [x] Red team exercises (Simulating attacks using the Generator model).

- **What is your acceptable false positive rate?**
  - [x] Less than 5% false positives.

- **What is your acceptable false negative rate?**
  - [x] Less than 2% false negatives (missed threats).

### 11.2 Validation With Users
- **How will you validate with actual users?**
  - [x] Pilot program with 5-10 users (classmates/friends).
  - [x] User surveys/feedback on ease of use.

### 11.3 Performance Benchmarks
- [x] Baseline (no detection system).
- [x] Existing email provider's spam filter (Benchmark: Can we catch what they miss?).

---

## Section 12: Risks & Mitigation

### 12.1 Technical Risks
| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation Strategy |
|------|-------------------|----------------|---------------------|
| High false positive rate | M | H | Implement "Sensitivity Settings" users can adjust; easy "Mark as Safe" feedback loop. |
| Model fails to detect new phishing tactics | M | H | Regular retraining (weekly) and use of Generator model to create new synthetic threats. |
| System can't scale to user load | L | M | Use asynchronous processing (Celery/Redis) to handle emails in queues. |
| Email provider blocks IMAP access | M | H | Implement rate limiting to respect provider API limits; use official APIs where possible. |

### 12.2 Ethical & Legal Risks
| Risk | Mitigation Strategy |
|------|---------------------|
| Generated phishing emails used maliciously | Strict containerization; no outbound email capability for the generator. |
| Privacy violation (reading user emails) | Data encryption (at rest/transit); transparent privacy policy; local processing preference. |

### 12.3 Project Risks
| Risk | Mitigation Strategy |
|------|---------------------|
| Insufficient training data | Use data augmentation and synthetic data generation. |

---

## Section 13: Post-Launch & Maintenance

### 13.1 Ongoing Operations
- **Who will maintain the system after launch?**
  - [x] Answer: The project team (until semester end); then open-sourced on GitHub.

- **What ongoing costs will exist?**
  - [x] Cloud infrastructure: $0/month (Free tier targets).
  - [x] Model retraining compute: Local machine usage.

- **How will you handle model drift and degradation?**
  - [x] Answer: Monitor performance metrics weekly; if accuracy drops below 80%, trigger a full retrain with new data.

### 13.2 Future Enhancements
  - 1. Browser Extension for webmail integration.
  - 2. Federated Learning (privacy-preserving model training).

### 13.3 Exit Strategy
  - [x] User data deletion process: "Delete Account" button wipes all database entries.
  - [x] User notification: Email blast 1 week before shutdown.
  - [x] Code/model archival: Public GitHub repository with documentation.

---

## Section 14: Documentation & Communication

### 14.1 Documentation Needs
  - [x] Technical architecture documentation (UML diagrams).
  - [x] API documentation (Swagger/OpenAPI).
  - [x] User guide (PDF/Wiki).
  - [x] Model training/evaluation reports (Jupyter Notebooks).

### 14.2 Portfolio Presentation
**If this is a portfolio project, what do you want to showcase?**
  - [x] ML/AI skills (model development)
  - [x] System design (architecture)
  - [x] Security expertise
  - [x] Product thinking

**What artifacts will you create for your portfolio?**
  - [x] GitHub repository (public).
  - [x] Demo video (Walkthrough of detecting a threat).
  - [x] Technical blog post (explaining the "Two-Model Approach").

---
