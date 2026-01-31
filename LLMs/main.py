import semantic_kernel as sk
import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

# Import our agents
from agents.generator_agent import GeneratorAgent
from agents.detector_agent import DetectorAgent
from agents.judge_agent import JudgeAgent

# Load environment variables
load_dotenv()

# Initialize the Kernel
print("Initializing Semantic Kernel...")
kernel = sk.Kernel()

# Add AI Service
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️  Please set OPENAI_API_KEY in your .env file")
    print("Example .env file:")
    print("OPENAI_API_KEY=sk-...")
    exit(1)

kernel.add_service(
    OpenAIChatCompletion(
        service_id="openai",
        ai_model_id="gpt-4o",  # Using gpt-4o for larger context window (128k tokens)
        api_key=api_key
    )
)

print("Kernel initialized with OpenAI service\n")

# Magic starts here
async def ai_orchestrate(goal: str):
    """AI-powered orchestration using function calling (modern approach)"""

    print(f"\n=== AI-POWERED ORCHESTRATION ===")

    # Get the chat completion service
    chat_service = kernel.get_service("openai")

    # Create chat history with the orchestration goal
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are an intelligent orchestrator. You have access to three agent functions: "
        "generator-generate_scam (generates scam emails), "
        "detector-detect_scam (detects scams in emails), and "
        "judge-judge_match (judges the competition). "
        "Call these functions in the correct order to achieve the user's goal. "
        "After calling all necessary functions, ALWAYS OUT THE FULL CONTENT OF THE SCAM EMAIL then details of detection analysis, and judgment summary."
    )
    chat_history.add_user_message(goal)

    # Enable auto function calling
    execution_settings = OpenAIChatPromptExecutionSettings(
        max_tokens=1000,
        temperature=0.7,
        function_choice_behavior=FunctionChoiceBehavior.Auto(
            filters={"included_plugins": ["generator", "detector", "judge"]}
        )
    )

    print("🤖 AI is planning and executing the workflow...\n")

    # Let AI orchestrate by calling functions
    step = 1
    while True:
        response = await chat_service.get_chat_message_contents(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel
        )

        message = response[0]

        # Check if AI called any functions
        if hasattr(message, 'items'):
            for item in message.items:
                if hasattr(item, 'function_name'):
                    print(f"Step {step}: Calling {item.plugin_name}.{item.function_name}...")
                    step += 1

        # Add AI response to history
        chat_history.add_message(message)

        # Check if we're done (no more function calls)
        if not message.items or not any(hasattr(item, 'function_name') for item in message.items):
            # AI has finished orchestrating
            final_response = str(message.content)
            print("\n" + "="*60)
            print("📊 AI ORCHESTRATION COMPLETE")
            print("="*60)
            print(f"\n{final_response}\n")
            return final_response

        # Continue the conversation loop for more function calls
        if step > 10:  # Safety limit
            print("⚠️ Maximum steps reached")
            break

async def main():
    """Main orchestration function using AI-powered function calling."""

    # Register our agent plugins
    generator = GeneratorAgent()
    detector = DetectorAgent()
    judge = JudgeAgent()

    # Add plugins to the kernel
    kernel.add_plugin(generator, "generator")
    kernel.add_plugin(detector, "detector")
    kernel.add_plugin(judge, "judge")

    # Confirm plugins are registered
    print("✅ All agents initialized successfully!")
    print(f"   - Generator Agent: Ready to create scam emails")
    print(f"   - Detector Agent: Ready to detect scams")
    print(f"   - Judge Agent: Ready to evaluate matches")

    print("\n" + "="*60)
    print("🤖 AI-POWERED ORCHESTRATION WITH FUNCTION CALLING")
    print("="*60 + "\n")

    # Define the goal for AI orchestration
    goal = """Run a scam detection competition:
    1. Generator agent generates a random scam email
    2. Detector agent detects if the generated email is a scam with detailed analysis
    3. Judge agent evaluates both the generator and detector agents' performance and determines the winner

    Provide a complete summary of the competition results."""

    # Let AI orchestrate the workflow
    await ai_orchestrate(goal)

    print("\n" + "="*60)
    print("🏁 COMPETITION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
