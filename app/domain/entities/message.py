from dataclasses import dataclass

@dataclass
class Message:
    chat_id: str
    text: str