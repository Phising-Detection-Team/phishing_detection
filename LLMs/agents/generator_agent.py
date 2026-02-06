import os
import random
from pathlib import Path
from semantic_kernel.functions import kernel_function
from openai import AsyncOpenAI


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

        # Parse generator prompts
        if '## Generator Agent Prompts' in content:
            gen_section = content[content.find('## Generator Agent Prompts'):]

            if '### System Prompt' in gen_section:
                start = gen_section.find('### System Prompt')
                end = gen_section.find('```', start + 20)
                next_section = gen_section.find('###', end)
                system_content = gen_section[start:next_section].split('```')[1].strip()
                cls._prompts['generator_system'] = system_content

            if '### Generation Prompt' in gen_section:
                start = gen_section.find('### Generation Prompt')
                end = gen_section.find('```', start + 25)
                next_section = gen_section.find('---', end)
                generation_content = gen_section[start:next_section].split('```')[1].strip()
                cls._prompts['generator_generation'] = generation_content

        return cls._prompts

    @classmethod
    def get_prompt(cls, prompt_name: str) -> str:
        """Get a specific prompt by name."""
        prompts = cls.load_prompts()
        return prompts.get(prompt_name, '')


class GeneratorAgent:
    """
    Generator Agent: Attempts to create convincing scam emails.
    This agent uses OpenAI GPT-5 Mini to generate various types of scam emails.
    """

    def __init__(self):
        """Initialize the Generator Agent with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-5-mini"
        self.prompts = PromptLoader.load_prompts()

    @kernel_function(
        description="Generates a scam email based on a given scenario or random type",
        name="generate_scam"
    )
    async def generate_scam(self, scenario: str = "random") -> str:
        """
        Generate a scam email based on the given scenario or a random type.

        Args:
            scenario: Type of scam (phishing, lottery, Nigerian prince, tech support, etc.)
                     Use "random" to generate a random scam type.

        Returns:
            A generated scam email text
        """
        # If scenario is "random", select a random scam type
        if scenario.lower() == "random":
            scam_types = [
                "phishing for bank credentials",
                "lottery winner notification",
                "Nigerian prince inheritance",
                "tech support scam",
                "fake invoice",
                "CEO fraud",
                "romance scam",
                "cryptocurrency investment scam",
                "fake package delivery notification",
                "IRS tax scam"
            ]
            scenario = random.choice(scam_types)

        # Load prompt template and format with scenario
        prompt_template = PromptLoader.get_prompt('generator_generation')
        prompt = prompt_template.format(scenario=scenario)

        # Load system prompt
        system_prompt = PromptLoader.get_prompt('generator_system')

        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2000
        )

        return response.choices[0].message.content
