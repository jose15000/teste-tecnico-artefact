from src.agent import Agent
from src.tools import AVAILABLE_TOOLS
from src.tools_schema import TOOLS_SCHEMA


def main() -> None:
    agent = Agent(tools=AVAILABLE_TOOLS, tools_schema=TOOLS_SCHEMA)
    print("Empório da Música - atendimento (digite 'sair' para encerrar, 'limpar' para reiniciar)\n")

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in {"sair", "exit", "quit"}:
            break
        if user_input.lower() == "limpar":
            agent.reset()
            print("Conversa reiniciada.\n")
            continue
        print(f"\nAtendente: {agent.chat(user_input)}\n")


if __name__ == "__main__":
    main()
