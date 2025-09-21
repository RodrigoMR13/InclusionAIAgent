from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def generate_response(self, text: str) -> str:
        pass
