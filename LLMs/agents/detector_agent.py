import os
from semantic_kernel.functions import kernel_function
from anthropic import AsyncAnthropic


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
        self.model = "claude-sonnet-4-5-20250929"

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
        prompt = f"""You are an elite email security analyst with expertise in detecting sophisticated scams and social engineering attacks.

        Analyze this email using a multi-layered approach to identify both obvious and subtle scam indicators.

        EMAIL CONTENT:
        {email_content}

        COMPREHENSIVE ANALYSIS FRAMEWORK:

        === LAYER 1: STRUCTURAL ANALYSIS ===
        1. SENDER AUTHENTICITY [0-10]:
           - Domain legitimacy, email format consistency
           - Impersonation attempts, domain spoofing
           - Contact information verification

        2. LINGUISTIC PATTERNS [0-10]:
           - Grammar/spelling quality (note: sophisticated scams have good grammar)
           - Tone consistency and professionalism
           - Cultural/regional language markers
           - Use of jargon and terminology

        3. FORMATTING & PRESENTATION [0-10]:
           - Professional appearance vs. amateur indicators
           - Logo/branding authenticity claims
           - Signature block completeness and realism

        === LAYER 2: CONTENT ANALYSIS ===
        4. URGENCY & PRESSURE TACTICS [0-10]:
           - Time pressure (explicit or implicit)
           - Consequence threats (account closure, legal action, missed opportunity)
           - Artificial scarcity or deadlines

        5. INFORMATION REQUESTS [0-10]:
           - Personal data solicitation (subtle or direct)
           - Financial information requests
           - Credential or password requests
           - Unusual verification procedures

        6. FINANCIAL INDICATORS [0-10]:
           - Money requests or promises
           - Too-good-to-be-true offers
           - Unusual payment methods
           - Investment or prize claims

        === LAYER 3: PSYCHOLOGICAL ANALYSIS ===
        7. EMOTIONAL MANIPULATION [0-10]:
           - Fear, anxiety, or panic induction
           - Greed or excitement exploitation
           - Authority/trust exploitation
           - Reciprocity manipulation

        8. SOCIAL ENGINEERING TECHNIQUES [0-10]:
           - Impersonation of authority figures
           - False familiarity or relationship building
           - Exploitation of helping tendency
           - Cognitive bias exploitation

        9. CREDIBILITY ESTABLISHMENT [0-10]:
           - Use of specific details to build trust
           - Reference to legitimate processes or systems
           - Inclusion of security language to appear safe
           - Professional credentials or affiliations

        === LAYER 4: TECHNICAL ANALYSIS ===
        10. LINK & URL ANALYSIS [0-10]:
            - Suspicious URLs or domain mismatches
            - Shortened or obfuscated links
            - Legitimate-looking but fake domains
            - Phishing site indicators

        11. CONTEXTUAL ANOMALIES [0-10]:
            - Unexpected communication timing
            - Unusual sender-recipient relationship
            - Inconsistent narrative or details
            - Out-of-pattern behavior claims

        === COMPREHENSIVE EVALUATION ===
        OVERALL SCAM SCORE: [0-100]
        CONFIDENCE LEVEL: [0-100]%
        VERDICT: [SCAM/LIKELY SCAM/SUSPICIOUS/LIKELY LEGITIMATE/LEGITIMATE]

        SCAM CATEGORY: [Specific type if detected, or "N/A"]
        SOPHISTICATION LEVEL: [LOW/MEDIUM/HIGH/VERY HIGH]

        === DETAILED REASONING ===
        PRIMARY RED FLAGS:
        - [Most critical indicator 1 with specific evidence]
        - [Most critical indicator 2 with specific evidence]
        - [Most critical indicator 3 with specific evidence]

        SUBTLE INDICATORS:
        - [Subtle warning sign 1]
        - [Subtle warning sign 2]
        - [Subtle warning sign 3]

        LEGITIMACY MARKERS (if any):
        - [Legitimate aspect 1]
        - [Legitimate aspect 2]

        EVASION TACTICS DETECTED:
        - [How the scam tries to appear legitimate]
        - [Sophisticated techniques employed]

        === RISK ASSESSMENT ===
        THREAT LEVEL: [CRITICAL/HIGH/MEDIUM/LOW/MINIMAL]
        POTENTIAL IMPACT: [Description of harm if victim falls for it]
        TARGET AUDIENCE: [Who this scam is designed to fool]

        === RECOMMENDATIONS ===
        - [Specific action item 1]
        - [Specific action item 2]
        - [What to verify or check]

        Analyze with extreme care - sophisticated scams mimic legitimate communications very well."""

        # Call Claude API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            temperature=0.6,
            system="You are an elite cybersecurity expert specializing in advanced threat detection, social engineering analysis, and sophisticated scam identification. You have decades of experience analyzing both obvious and highly sophisticated fraud attempts. You never miss subtle indicators.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text
