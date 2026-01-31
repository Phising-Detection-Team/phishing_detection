# Email Scam Detection - Multi-Agent System

A multi-agent AI system using Semantic Kernel orchestration where three agents compete and learn:

## 🎭 Agents

### 1. Generator Agent
- **Goal**: Create convincing scam emails
- **Capabilities**: Generates various types of scam emails (phishing, lottery, Nigerian prince, etc.)
- **Strategy**: Uses social engineering tactics to create realistic scams

### 2. Detector Agent
- **Goal**: Detect and analyze scam emails
- **Capabilities**: Identifies scam indicators, provides confidence scores and reasoning
- **Strategy**: Analyzes urgency tactics, information requests, credibility issues, etc.

### 3. Judge Agent
- **Goal**: Evaluate both agents and determine the winner
- **Capabilities**: Scores performance, provides improvement suggestions, tracks progress
- **Strategy**: Assesses realism vs. detection accuracy

## 🚀 Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

3. **Run the system**:
   ```bash
   python main.py
   ```

## 🎮 How It Works

The system runs in rounds:

1. **Generator** creates a scam email
2. **Detector** analyzes and determines if it's a scam
3. **Judge** evaluates both agents and declares a winner

After multiple rounds, the Judge provides insights on how both agents are evolving and improving.

## 📊 Scoring

- **Generator Score**: Based on realism, subtlety, and social engineering quality
- **Detector Score**: Based on accuracy, reasoning quality, and confidence calibration

## 🔧 Configuration

Edit [main.py](main.py) to:
- Change the number of rounds: `run_multiple_rounds(kernel, num_rounds=5)`
- Switch AI models: Change `"gpt-4"` to `"gpt-3.5-turbo"` for faster results
- Customize agent behaviors in the respective agent files

## 📝 Example Output

```
🎮 MULTI-AGENT SCAM DETECTION COMPETITION
============================================================

ROUND 1: GENERATOR vs DETECTOR
============================================================

🎭 Generator Agent: Creating scam email...
📧 Generated Scam Email:
[Scam email content]

🔍 Detector Agent: Analyzing email...
🎯 Detection Result:
[Analysis results]

⚖️ Judge Agent: Evaluating performance...
⚖️ Judge's Decision:
[Scores and winner]
```

## 🎯 Use Cases

- **Security Training**: Help teams recognize scam patterns
- **AI Research**: Study adversarial AI systems
- **Educational**: Demonstrate multi-agent orchestration
- **Testing**: Evaluate email security systems

## ⚠️ Disclaimer

This system is for educational and research purposes only. Do not use generated scam emails for malicious purposes.
