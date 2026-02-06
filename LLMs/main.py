import sys
import asyncio
import os
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import specific backend components
from backend.app.models import db, Email, Round, API

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

from agents.generator_agent import GeneratorAgent
from agents.detector_agent import DetectorAgent
from agents.judge_agent import JudgeAgent
from agents.orchestration_agent import OrchestrationAgent

load_dotenv()

OPENAI_MODEL = "gpt-5-mini-2025-08-07"
DEFAULT_MAX_ROUNDS = 10

def create_minimal_app():
    """Create a minimal Flask app context for DB access."""
    app = Flask(__name__)
    # Ensure this matches your backend config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def initialize_kernel():
    """Initialize the Semantic Kernel with OpenAI service."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Please set OPENAI_API_KEY in your .env file")
        print("Example .env file:")
        print("OPENAI_API_KEY=sk-...")
        exit(1)

    print("Initializing Semantic Kernel...")
    kernel = sk.Kernel()

    kernel.add_service(
        OpenAIChatCompletion(
            service_id="openai",
            ai_model_id=OPENAI_MODEL,
            api_key=api_key
        )
    )

    print(f"Kernel initialized with OpenAI service ({OPENAI_MODEL})\n")
    return kernel

def register_agents(kernel):
    # ... (Same as your existing code) ...
    kernel.add_plugin(GeneratorAgent(), "generator")
    kernel.add_plugin(DetectorAgent(), "detector")
    kernel.add_plugin(JudgeAgent(), "judge")

async def save_results_to_db(result: dict):
    """Map the JSON result from the Agent to the Database Models."""
    
    # 1. Create a Round record (optional, depending on your logic)
    new_round = Round(
        status="completed",
        total_emails=1,
        processed_emails=1
    )
    db.session.add(new_round)
    db.session.flush() # Flush to get the round ID
    
    # 2. Map JSON keys to Email Model columns
    # Note: Ensure the JSON keys returned by the prompt match these exactly
    email_entry = Email(
        round_id=new_round.id,
        
        # Generator Outputs
        generated_content=result.get("generated_content"),
        generated_subject=result.get("generated_subject"),
        generated_body=result.get("generated_body"),
        is_phishing=result.get("is_phishing", True),
        
        # REQUIRED: Metadata (Must be a dict/JSON)
        generated_email_metadata=result.get("generated_email_metadata", {}), 
        
        # REQUIRED: Ground Truth (Used by judge)
        judge_ground_truth=result.get("judge_ground_truth", "phishing"),

        # Latency (Ensure this matches the spelling in email.py)
        # If you didn't fix email.py, change this to generator_latenc_ms
        generator_latency_ms=result.get("generator_latency_ms"), 

        # Detector Outputs
        # Note: Parameter is 'detector_verdict', JSON might be 'detection_verdict'
        detector_verdict=result.get("detector_verdict"), 
        detector_reasoning=result.get("detector_reasoning"),
        detector_risk_score=result.get("detector_risk_score"),
        detector_latency_ms=result.get("detector_latency_ms"),

        # Judge Outputs
        judge_verdict=result.get("judge_verdict"),
        judge_reasoning=result.get("judge_reasoning"),
        judge_quality_score=result.get("judge_quality_score", 0),
        judge_latency_ms=result.get("judge_latency_ms"),
        
        # Boolean Logic
        is_judge_correct=(str(result.get("judge_verdict")).lower() == "correct")
    )

    db.session.add(email_entry)
    db.session.commit()

async def main():
    # 1. Initialize the App Context
    app = create_minimal_app()
    
    # 2. Run the logic inside the app context
    with app.app_context():
        kernel = initialize_kernel()
        register_agents(kernel)

        # ... (Your input logic for max_rounds) ...
        max_rounds = DEFAULT_MAX_ROUNDS

        orchestration_agent = OrchestrationAgent()
        
        # 3. Get result from AI
        result = await orchestration_agent.ai_orchestrate(kernel, max_rounds)

        if result:
            print("\n" + "="*60)
            print("💾 SAVING TO DATABASE")
            print("="*60)
            try:
                await save_results_to_db(result)
            except Exception as e:
                print(f"❌ Database Error: {e}")
        else:
            print("\n❌ No result returned, skipping database save.")

if __name__ == "__main__":
    asyncio.run(main())