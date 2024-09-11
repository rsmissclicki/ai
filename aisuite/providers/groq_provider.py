from aisuite.provider import Provider


class GroqProvider(Provider):
    def __init__(self) -> None:
        pass

    def chat_completions_create(self, model, messages):
        raise ValueError("Groq provider not yet implemented.")
