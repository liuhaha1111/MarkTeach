from typing import Protocol


class ProviderClient(Protocol):
    def generate_section(self, chunk: str, *, model: str, prompt: str) -> str:
        ...
