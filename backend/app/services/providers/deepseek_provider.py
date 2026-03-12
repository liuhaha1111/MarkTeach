from app.services.providers.base import ProviderClient


class DeepSeekProvider(ProviderClient):
    def generate_section(self, chunk: str, *, model: str, prompt: str) -> str:
        del model
        del prompt
        text = ' '.join(line.strip() for line in chunk.splitlines() if line.strip())
        return text[:360] if text else 'No content provided.'
