import sys
from pathlib import Path

# Add project root to Python path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

import semantic_kernel as sk
import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from backend.app.models import db

# Import our agents
from agents.generator_agent import GeneratorAgent
from agents.detector_agent import DetectorAgent
from agents.judge_agent import JudgeAgent
from agents.orchestration_agent import OrchestrationAgent

# Load environment variables
load_dotenv()

# Constants
OPENAI_MODEL = "gpt-5-mini-2025-08-07"
DEFAULT_MAX_ROUNDS = 10

# Initialize Semantic Kernel with OpenAI
def initialize_kernel() -> sk.Kernel:
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

# Register agents with the kernel
def register_agents(kernel: sk.Kernel) -> None:
    """Register agent plugins with the kernel."""
    generator = GeneratorAgent()
    detector = DetectorAgent()
    judge = JudgeAgent()

    kernel.add_plugin(generator, "generator")
    kernel.add_plugin(detector, "detector")
    kernel.add_plugin(judge, "judge")

    print("✅ All agents initialized successfully!")
    print("   - Generator Agent: Ready to create scam emails")
    print("   - Detector Agent: Ready to detect scams")
    print("   - Judge Agent: Ready to evaluate matches\n")

async def main():
    """Main orchestration function using AI-powered function calling."""
    # Initialize kernel and register agents
    kernel = initialize_kernel()
    register_agents(kernel)

    # Get max rounds from user input (with default)
    try:
        user_input = input("\nEnter maximum rounds for orchestration (default 10): ").strip()
        max_rounds = int(user_input) if user_input else DEFAULT_MAX_ROUNDS
        if max_rounds <= 0:
            print("Invalid input. Using default value.")
            max_rounds = DEFAULT_MAX_ROUNDS
    except ValueError:
        print("Invalid input. Using default value.")
        max_rounds = DEFAULT_MAX_ROUNDS

    # Run AI orchestration and get result as dict
    orchestration_agent = OrchestrationAgent()
    result = await orchestration_agent.ai_orchestrate(kernel, max_rounds)

    print("\n" + "="*60)
    print("🏁 COMPETITION COMPLETE")
    print("="*60)

    # Result is now a dict that can be merged with other JSON
    if result:
        print(f"\n✅ Result stored as dictionary with {len(result)} keys")
        print(f"Keys: {list(result.keys())}")

        other_json_data = {
            'generated_prompt': 'Example prompt used to generate scam email',
            'generator_latenc_ms': 1234,
            'detector_latency_ms': 2345,
            'judge_latency_ms': 3456,
            'is_judge_correct': True,
            'manual_override': False,
            'override_verdict': None,
            'override_reason': None,
            'overridden_by': None,
            'overridden_at': None,
            'created_at': '2024-08-15T12:34:56Z',
            'processing_time': 7.035,
            'cost': 0.45
        }
        # Example: You can now merge with other JSON
        # merged_result = {**result, **other_json_data}
    else:
        print("\n❌ No result returned")

if __name__ == "__main__":
    asyncio.run(main())
