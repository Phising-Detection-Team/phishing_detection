import os
from pathlib import Path
from semantic_kernel.functions import kernel_function
from anthropic import AsyncAnthropic


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

        # Parse detector prompts
        if '## Detector Agent Prompts' in content:
            det_section = content[content.find('## Detector Agent Prompts'):]

            if '### System Prompt' in det_section:
                start = det_section.find('### System Prompt')
                end = det_section.find('```', start + 20)
                next_section = det_section.find('###', end)
                system_content = det_section[start:next_section].split('```')[1].strip()
                cls._prompts['detector_system'] = system_content

            if '### Detection Analysis Prompt' in det_section:
                start = det_section.find('### Detection Analysis Prompt')
                end = det_section.find('```', start + 30)
                next_section = det_section.find('---', end)
                detection_content = det_section[start:next_section].split('```')[1].strip()
                cls._prompts['detector_analysis'] = detection_content

        return cls._prompts

    @classmethod
    def get_prompt(cls, prompt_name: str) -> str:
        """Get a specific prompt by name."""
        prompts = cls.load_prompts()
        return prompts.get(prompt_name, '')


class DetectorAgent:
    """
    Detector Agent: Analyzes emails to identify scam indicators.
    This agent uses Claude (Anthropic) to detect various scam patterns and characteristics.
    """

    def __init__(self):
        """Initialize the Detector Agent with Claude client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-haiku-20240307"
        self.prompts = PromptLoader.load_prompts()

    @kernel_function(
        description="Analyzes an email to detect if it's a scam with detailed indicator scoring and reasoning",
        name="detect_scam"
    )
    async def detect_scam(self, email_content: str) -> str:
        """
        Analyze an email to determine if it's a scam with comprehensive indicator analysis.

        Args:
            email_content: The email content to analyze

        Returns:
            Detailed analysis with verdict, confidence, indicator scores, and reasoning
        """
        # Load prompt template and format with email content
        prompt_template = PromptLoader.get_prompt('detector_analysis')
        prompt = prompt_template.format(email_content=email_content)

        # Load system prompt
        system_prompt = PromptLoader.get_prompt('detector_system')

        # Call Claude API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.6,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text
