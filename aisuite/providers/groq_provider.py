from aisuite.provider import Provider
from typing import override


class GroqProvider(Provider):
    def __init__(self) -> None:
        pass

    @override
    def chat_completions_create(self, model, messages):
        raise ValueError("Groq provider not yet implemented.")
