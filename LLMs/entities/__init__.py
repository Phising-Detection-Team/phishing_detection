"""Entity classes for agent configuration and state management."""

from .base_entity import BaseEntity
from .generator_agent_entity import GeneratorAgentEntity
from .detector_agent_entity import DetectorAgentEntity
# from .judge_agent_entity import JudgeAgentEntity  # Commented out - not needed
from .orchestration_agent_entity import OrchestrationAgentEntity

__all__ = [
    'BaseEntity',
    'GeneratorAgentEntity',
    'DetectorAgentEntity',
    # 'JudgeAgentEntity',  # Commented out
    'OrchestrationAgentEntity',
]
