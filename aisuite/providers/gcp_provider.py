from aisuite.provider import Provider
from typing import override


class GcpProvider(Provider):
    def __init__(self) -> None:
        pass

    @override
    def chat_completions_create(self, model, messages):
        raise ValueError("GCP Provider not yet implemented.")
