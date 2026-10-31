import json
import os
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv
from groq import BadRequestError, Groq

from src.prompts import SYSTEM_PROMPT

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

DEFAULT_MODEL = "openai/gpt-oss-120b"
FALLBACK_REPLY = "Desculpe, não consegui concluir sua solicitação. Pode reformular?"


class Agent:
    def __init__(
        self,
        tools: dict[str, Callable] | None = None,
        tools_schema: list[dict] | None = None,
        model: str | None = None,
    ):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY não encontrada. Configure o arquivo .env.")

        self.client = Groq(api_key=api_key)
        self.model = model or os.getenv("GROQ_MODEL", DEFAULT_MODEL)

        self.available_tools = tools or {}
        self.tools_schema = tools_schema or []

        self.messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_input: str, max_steps: int = 5) -> str:
        """Envia a mensagem do usuário e executa o loop de tool calling até a resposta final."""
        self.messages.append({"role": "user", "content": user_input})

        for _ in range(max_steps):
            kwargs = {"model": self.model, "messages": self.messages}
            if self.tools_schema:
                kwargs.update(tools=self.tools_schema, tool_choice="auto")

            response = self._create_with_retry(kwargs)
            if response is None:
                return FALLBACK_REPLY
            message = response.choices[0].message
            self.messages.append(message)

            if not message.tool_calls:
                return message.content or FALLBACK_REPLY

            for call in message.tool_calls:
                result = self._run_tool(call.function.name, call.function.arguments)
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False, default=str),
                    }
                )

        return FALLBACK_REPLY

    def _create_with_retry(self, kwargs: dict, retries: int = 3):
        """Chama a API; se o modelo gerar um tool call malformado (output_parse_failed), tenta de novo."""
        for _ in range(retries):
            try:
                return self.client.chat.completions.create(**kwargs)
            except BadRequestError as e:
                if getattr(e, "code", None) != "output_parse_failed":
                    raise
        return None

    def _run_tool(self, name: str, raw_arguments: str | None):
        """Executa uma tool e devolve o erro como dado, para o modelo poder se corrigir."""
        func = self.available_tools.get(name)
        if func is None:
            return {"error": f"Ferramenta '{name}' não existe."}
        try:
            return func(**json.loads(raw_arguments or "{}"))
        except Exception as e:
            return {"error": str(e)}

    def reset(self) -> None:
        """Limpa o histórico, mantendo apenas o system prompt."""
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
