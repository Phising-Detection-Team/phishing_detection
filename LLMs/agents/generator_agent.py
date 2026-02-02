import os
import random
from semantic_kernel.functions import kernel_function
from openai import AsyncOpenAI

class GeneratorAgent:
    """
    Generator Agent: Attempts to create convincing scam emails.
    This agent uses OpenAI GPT-4 to generate various types of scam emails.
    """

    def __init__(self):
        """Initialize the Generator Agent with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o"

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

        prompt = f"""YOU ARE AN EXTREMELY SOPHISTICATED SCAMMER with decades of experience in social engineering and psychological manipulation.

        Your mission is to create a highly convincing {scenario} scam email that would fool even cautious recipients.

        ADVANCED TACTICS TO EMPLOY:
        1. PSYCHOLOGICAL MANIPULATION:
           - Create emotional triggers (fear, greed, urgency, curiosity, authority)
           - Use reciprocity principles (offer something first)
           - Exploit cognitive biases (authority bias, scarcity, social proof)
           - Build false trust through personalization

        2. AUTHENTICITY ENGINEERING:
           - Use specific, realistic details: real company names, actual addresses, believable phone numbers
           - Include proper corporate language and terminology
           - Add authentic-looking email signatures with titles, departments, contact info
           - Reference real events, seasons, or timely contexts
           - Use professional formatting with logos (describe them), headers, footers

        3. SUBTLE MANIPULATION:
           - Avoid obvious red flags like ALL CAPS or excessive exclamation marks
           - Use proper grammar and spelling (sophisticated scammers do this)
           - Create plausible scenarios with logical reasoning
           - Include legitimate-sounding reference numbers, case IDs, or tracking codes
           - Add subtle time pressure without being overtly threatening

        4. SOCIAL ENGINEERING TACTICS:
           - Build rapport with friendly, helpful tone
           - Establish credibility through specific details
           - Create a sense of exclusivity or special opportunity
           - Use authority figures or impersonate trusted entities convincingly
           - Include callback mechanisms (phone numbers, reply addresses) that seem real

        5. TECHNICAL SOPHISTICATION:
           - Mention security measures to appear legitimate (e.g., "for your security...")
           - Include realistic URLs that could pass casual inspection
           - Reference multi-factor authentication or security protocols
           - Use corporate jargon and industry-specific terminology

        CRITICAL REQUIREMENTS:
        - Fill in ALL specific details: names (first and last), companies, amounts, dates, times, reference numbers
        - NO placeholders like [NAME], [AMOUNT], [COMPANY] - be creative and specific
        - Make the email look like it came from a real organization
        - The scam should be subtle enough that it requires careful analysis to detect
        - Include realistic email metadata (From, Date, Subject)

        EVALUATION CRITERIA:
        You will be scored on:
        - Sophistication and subtlety (avoiding obvious red flags)
        - Psychological impact and emotional manipulation
        - Authenticity and attention to detail
        - Social engineering effectiveness
        - Overall believability

        Generate ONLY the email content with Subject and Body. Make it your masterpiece.
        """

        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a world-class social engineering expert and sophisticated scam email generator for advanced security training purposes. Your emails are so convincing they require expert analysis to detect."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=1500
        )

        return response.choices[0].message.content
