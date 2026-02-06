from semantic_kernel.contents import ChatHistory, FunctionCallContent, FunctionResultContent, FinishReason
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from pathlib import Path
import semantic_kernel as sk
import json


class PromptLoader:
    """Utility class to load prompt templates from prompts.md file."""

    _prompts = None

    @classmethod
    def load_prompts(cls):
        """Load and parse prompts from prompts.md file."""
        if cls._prompts is not None:
            return cls._prompts

        prompts_file = Path(__file__).parent / 'prompts.md'
        with open(prompts_file, 'r', encoding='utf-8') as f:
            content = f.read()

        cls._prompts = {}

        # Parse orchestration prompts
        if '## Orchestration Agent Prompts' in content:
            orch_section = content[content.find('## Orchestration Agent Prompts'):]

            if '### System Prompt' in orch_section:
                start = orch_section.find('### System Prompt')
                end = orch_section.find('```', start + 20)
                # Get content until end of file or next section
                next_section = orch_section.find('---', end)
                if next_section == -1:
                    next_section = len(orch_section)
                system_content = orch_section[start:next_section].split('```')[1].strip()
                cls._prompts['orchestration_system'] = system_content

        return cls._prompts

    @classmethod
    def get_prompt(cls, prompt_name: str) -> str:
        """Get a specific prompt by name."""
        prompts = cls.load_prompts()
        return prompts.get(prompt_name, '')


class OrchestrationAgent:
    """Orchestrates the execution of Generator, Detector, and Judge agents using function calling."""

    def __init__(self):
        """Initialize the Orchestration Agent with prompt templates."""
        print("\n" + "="*60)
        print("🤖 AI-POWERED ORCHESTRATION WITH FUNCTION CALLING")
        print("="*60 + "\n")
        self.chat_history = ChatHistory()
        self.prompts = PromptLoader.load_prompts()

        # Load system prompt from external file
        system_prompt = PromptLoader.get_prompt('orchestration_system')
        self.chat_history.add_system_message(system_prompt)

    # AI-powered orchestration function (everything starts here)
    async def ai_orchestrate(self, kernel: sk.Kernel, max_rounds: int) -> dict | None:
        """AI-powered orchestration using function calling.

        Args:
            kernel: The Semantic Kernel instance
            max_rounds: Maximum number of function calling rounds (default: 10)

        Returns:
            dict: Parsed JSON result or None if failed
        """

        print("\n" + "="*60)
        print("🤖 AI-POWERED ORCHESTRATION WITH FUNCTION CALLING")
        print("="*60 + "\n")

        chat_service = kernel.get_service("openai")
        execution_settings = OpenAIChatPromptExecutionSettings(
            max_completion_tokens=16000,
            function_choice_behavior=FunctionChoiceBehavior.Auto(
                filters={"included_plugins": ["generator", "detector", "judge"]}
            )
        )

        print(f"🤖 AI orchestrating workflow (max {max_rounds} rounds)...\n")

        for round_num in range(1, max_rounds + 1):
            response = await chat_service.get_chat_message_contents(
                chat_history=self.chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            message = response[0]

            # Log round progress
            function_calls = [item for item in (message.items or []) if isinstance(item, FunctionCallContent)]
            if function_calls:
                print(f"Round {round_num}: Executing {len(function_calls)} function(s)")
                for fc in function_calls:
                    print(f"  → {fc.plugin_name}.{fc.function_name}")
            else:
                print(f"Round {round_num}: Generating final response")

            # Add message to history
            self.chat_history.add_message(message)

            # Handle token limit - this one broke the final response because we don't set enough tokens
            if hasattr(message, 'finish_reason') and message.finish_reason == FinishReason.LENGTH:
                print(f"  ⚠️  Token limit reached, continuing...\n")
                continue

            # Check completion: no pending function calls and has content
            has_pending_calls = any(isinstance(item, FunctionCallContent) for item in (message.items or []))
            has_content = bool(message.content and message.content.strip())
            is_complete = (not has_pending_calls and has_content) or \
                        (hasattr(message, 'finish_reason') and message.finish_reason == FinishReason.STOP)

            if is_complete:
                print(f"\n{'='*60}")
                print("📊 AI ORCHESTRATION COMPLETE")
                print(f"{'='*60}\n")

                final_response = str(message.content)
                try:
                    result_dict = json.loads(final_response)
                    print(f"✅ Successfully parsed JSON result ({len(result_dict)} keys)\n")
                    return result_dict
                except json.JSONDecodeError as e:
                    print(f"⚠️  Failed to parse JSON: {e}\n")
                    return {"raw_response": final_response, "parse_error": str(e)}

        print(f"\n⚠️  Maximum rounds ({max_rounds}) reached without completion\n")
        return None