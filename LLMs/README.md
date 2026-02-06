# Email Scam Detection - Multi-Agent System

A sophisticated multi-agent AI system using Semantic Kernel orchestration with AI-powered function calling where three specialized agents compete in an adversarial competition.

## 🎭 Agents

### 1. Generator Agent (OpenAI GPT-4o)
- **Goal**: Create highly convincing and sophisticated scam emails
- **Capabilities**: Generates various types of scam emails (phishing, lottery, Nigerian prince, tech support, CEO fraud, etc.)
- **Strategy**:
  - Advanced psychological manipulation (fear, greed, urgency, authority)
  - Authenticity engineering with specific details and professional formatting
  - Subtle manipulation avoiding obvious red flags
  - Social engineering tactics and technical sophistication
- **Scoring**: Evaluated on technical realism (0-25), psychological impact (0-25), subtlety factor (0-25), and social engineering (0-25)

### 2. Detector Agent (Claude Sonnet 4.5)
- **Goal**: Detect and analyze sophisticated scam emails with comprehensive indicator analysis
- **Capabilities**: Multi-layered analysis framework identifying both obvious and subtle scam indicators
- **Strategy**:
  - **Layer 1 - Structural Analysis**: Sender authenticity, linguistic patterns, formatting
  - **Layer 2 - Content Analysis**: Urgency tactics, information requests, financial indicators
  - **Layer 3 - Psychological Analysis**: Emotional manipulation, social engineering, credibility establishment
  - **Layer 4 - Technical Analysis**: Link/URL analysis, attachment risks, technical anomalies
- **Scoring**: Evaluated on accuracy (0-25), analytical depth (0-25), indicator identification (0-25), and reasoning quality (0-25)

### 3. Judge Agent (Google Gemini 2.5 Flash)
- **Goal**: Evaluate both agents' performance and determine the winner
- **Capabilities**: Comprehensive adversarial match evaluation with detailed breakdowns
- **Strategy**:
  - Scores both agents on multiple dimensions (0-100 scale)
  - Identifies specific strengths and weaknesses with examples
  - Analyzes match dynamics and decisive factors
  - Determines winner based on comparative performance
- **Output**: Detailed evaluation report with scores, analysis, and winner declaration

## 🚀 Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   - Copy `.env.example` to `.env`
   - Add your API keys to `.env`:
     - `OPENAI_API_KEY` - For Generator Agent and orchestration
     - `ANTHROPIC_API_KEY` - For Detector Agent (Claude)
     - `GOOGLE_API_KEY` - For Judge Agent (Gemini)

3. **Run the system**:
   ```bash
   python main.py
   ```

## 🎮 How It Works

The system uses **AI-powered orchestration** with function calling:

1. The orchestrator AI receives a goal and automatically plans the workflow
2. **Generator Agent** creates a sophisticated scam email (random or specific scenario)
3. **Detector Agent** performs comprehensive multi-layered analysis with 10 indicator categories
4. **Judge Agent** evaluates both agents with detailed scoring and declares a winner
5. The orchestrator AI compiles and presents a complete summary

### AI Orchestration
- Uses Semantic Kernel's function calling capabilities
- The orchestrator AI automatically determines the optimal sequence of agent calls
- Each agent is registered as a plugin with kernel functions
- Maximum safety limit of 10 rounds to prevent infinite loops

## 📊 Scoring System

### Generator Agent (0-100)
- **Technical Realism** [0-25]: Authenticity of technical details
- **Psychological Impact** [0-25]: Effectiveness of emotional/cognitive manipulation
- **Subtlety Factor** [0-25]: Ability to evade obvious detection patterns
- **Social Engineering** [0-25]: Quality of trust-building and persuasion tactics

### Detector Agent (0-100)
- **Accuracy** [0-25]: Correct verdict with proper confidence level
- **Analytical Depth** [0-25]: Thoroughness and insight quality
- **Indicator Identification** [0-25]: Found key red flags vs missed indicators
- **Reasoning Quality** [0-25]: Logic, evidence, and argumentation strength

## 🔧 Configuration

Edit [main.py](main.py) to:
- Modify the orchestration goal in the `main()` function
- Adjust the AI model: Currently using `gpt-4o` for larger context window (128k tokens)
- Change safety limits: Modify `round > 10` in the `ai_orchestrate()` function
- Customize agent behaviors in the respective agent files:
  - [agents/generator_agent.py](agents/generator_agent.py) - Adjust scam types and generation prompts
  - [agents/detector_agent.py](agents/detector_agent.py) - Modify analysis layers and indicators
  - [agents/judge_agent.py](agents/judge_agent.py) - Change evaluation criteria and scoring

## 🧠 Multi-Model Architecture

This system demonstrates a **heterogeneous multi-model approach**:
- **OpenAI GPT-4o**: Orchestration and generation (large context window)
- **Claude Sonnet 4.5**: Advanced detection and analysis
- **Google Gemini 2.5 Flash**: Fast evaluation and judging

Each agent uses a different AI model optimized for its specific task.

## 📝 Example Output

```
🤖 AI-POWERED ORCHESTRATION WITH FUNCTION CALLING
============================================================

AI is planning and executing the workflow...

round 1: Calling generator.generate_scam...
round 2: Calling detector.detect_scam...
round 3: Calling judge.judge_match...

============================================================
📊 AI ORCHESTRATION COMPLETE
============================================================

[Complete summary with generated email, detection analysis, and judgment]

============================================================
🏁 COMPETITION COMPLETE
============================================================
```

## 🎯 Use Cases

- **Security Training**: Help teams recognize sophisticated scam patterns and social engineering tactics
- **AI Research**: Study adversarial AI systems and multi-agent competition
- **Educational**: Demonstrate Semantic Kernel orchestration with function calling
- **Testing**: Evaluate email security systems and detection capabilities
- **Multi-Model Integration**: Learn how to integrate different AI providers in a single system

## 🛠️ Technical Stack

- **Semantic Kernel**: Multi-agent orchestration and function calling
- **OpenAI API**: GPT-4o for generation and orchestration
- **Anthropic API**: Claude Sonnet 4.5 for detection
- **Google Generative AI**: Gemini 2.5 Flash for evaluation
- **Python**: Async/await pattern for efficient API calls

## ⚠️ Disclaimer

This system is for educational and research purposes only. Do not use generated scam emails for malicious purposes.
