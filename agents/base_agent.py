# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")

class Agent(ABC, Generic[InputType, OutputType]):
    """Abstract base class for all agents."""
    
    @abstractmethod
    def execute(self, input_data: InputType) -> OutputType:
        """Executes the agent's task."""
        pass