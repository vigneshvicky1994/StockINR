"""LLM-backed decision making using OpenAI or Gemini."""

from typing import List, Tuple

try:  # pragma: no cover - optional dependency
    import openai
except ImportError:  # pragma: no cover
    openai = None

try:  # pragma: no cover - optional dependency
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class LLMDecisionMaker:
    """Query an LLM provider to obtain trading actions."""

    def __init__(self, provider: str, api_key: str):
        provider = provider.lower()
        self.provider = provider
        if provider == "openai":
            if openai is None:
                raise ImportError("openai package not installed")
            openai.api_key = api_key
        elif provider == "gemini":
            if genai is None:
                raise ImportError("google-generativeai package not installed")
            genai.configure(api_key=api_key)
            self._gemini_model = genai.GenerativeModel("gemini-pro")
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    def _parse_lines(self, text: str) -> List[Tuple[str, str]]:
        decisions: List[Tuple[str, str]] = []
        for line in text.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                action = parts[0].upper()
                symbol = parts[1].upper()
                decisions.append((action, symbol))
        return decisions

    def decide(self, context: str, budget: float) -> List[Tuple[str, str]]:
        """Ask the configured LLM for decisions."""

        prompt = (
            "You are a trading assistant for the Indian stock market. "
            "Based on the following context decide whether to BUY, SELL or HOLD "
            "stocks within a budget of INR %.2f. Respond with one action per line "
            "in the format 'ACTION SYMBOL'.\n%s" % (budget, context)
        )

        if self.provider == "openai":
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.choices[0].message.content
        elif self.provider == "gemini":
            resp = self._gemini_model.generate_content(prompt)
            text = resp.text or ""
        else:  # pragma: no cover - should not occur
            raise RuntimeError("Invalid provider")

        return self._parse_lines(text)

