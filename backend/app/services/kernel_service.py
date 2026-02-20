"""
Semantic Kernel integration for the Flask application.

Initializes the SK kernel with OpenAI service and registers
agent plugins (Generator, Detector, Orchestration) so that
Flask routes can trigger competition rounds via the kernel.

Usage in routes:
    from flask import current_app
    kernel = current_app.config['SK_KERNEL']
"""

import sys
import os


class KernelService:
    """Manages the Semantic Kernel lifecycle within the Flask app."""

    def __init__(self):
        self.kernel = None
        self._initialized = False

    def init_app(self, app):
        """
        Initialize Semantic Kernel and store it on the Flask app.

        Adds the LLMs/ directory to sys.path so we can import
        the agent services that the team built.
        """
        api_key = app.config.get('OPENAI_API_KEY', '')
        model_id = app.config.get('OPENAI_MODEL', 'gpt-4o-mini')

        if not api_key:
            app.logger.warning(
                'OPENAI_API_KEY not set -- Semantic Kernel will not be initialized. '
                'Set it in .env to enable AI orchestration.'
            )
            app.config['SK_KERNEL'] = None
            return

        try:
            import semantic_kernel as sk
            from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

            # Add LLMs/ to path so agent services can be imported
            llms_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', '..', 'LLMs'
            ))
            if llms_path not in sys.path:
                sys.path.insert(0, llms_path)

            from services.generator_agent_service import GeneratorAgentService
            from services.detector_agent_service import DetectorAgentService
            from services.orchestration_agent_service import OrchestrationAgentService

            # Create kernel
            self.kernel = sk.Kernel()

            # Add OpenAI chat service
            self.kernel.add_service(
                OpenAIChatCompletion(
                    service_id='openai',
                    ai_model_id=model_id,
                    api_key=api_key
                )
            )

            # Register agent plugins
            self.kernel.add_plugin(GeneratorAgentService(), 'generator')
            self.kernel.add_plugin(DetectorAgentService(), 'detector')
            self.kernel.add_plugin(OrchestrationAgentService(), 'orchestration')

            self._initialized = True
            app.config['SK_KERNEL'] = self.kernel
            app.logger.info(f'Semantic Kernel initialized with model: {model_id}')

        except ImportError as e:
            app.logger.warning(
                f'Semantic Kernel dependencies not installed: {e}. '
                'Run: pip install -r requirements.txt from the project root.'
            )
            app.config['SK_KERNEL'] = None

        except Exception as e:
            app.logger.error(f'Failed to initialize Semantic Kernel: {e}')
            app.config['SK_KERNEL'] = None

    @property
    def is_initialized(self):
        return self._initialized
