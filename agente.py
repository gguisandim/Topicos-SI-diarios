"""Agente mínimo para experimentar descrições de tools com Ollama."""

import json
import os
from urllib.request import Request, urlopen

MAX_PASSOS = 5
MODEL = os.getenv("OLLAMA_MODEL", "qwen3")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
PERGUNTA = "Use uma ferramenta para responder: quantos caracteres existem na palavra 'agente'?"


def nome_disciplina():
    """Retorna o nome da disciplina usada neste experimento."""
    return "Desenvolvimento de Aplicações utilizando Inteligência Artificial"


def consultar_texto(texto: str):
    """Conta quantos caracteres existem no texto informado."""
    return len(texto)


def ferramentas(descricao_vaga=False):
    descricao = "faz uma consulta" if descricao_vaga else consultar_texto.__doc__
    return [
        {
            "type": "function",
            "function": {
                "name": "nome_disciplina",
                "description": nome_disciplina.__doc__,
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "consultar_texto",
                "description": descricao,
                "parameters": {
                    "type": "object",
                    "properties": {"texto": {"type": "string"}},
                    "required": ["texto"],
                },
            },
        },
    ]


def chat(messages, tools):
    payload = json.dumps({
        "model": MODEL, "messages": messages, "tools": tools, "stream": False
    }).encode()
    req = Request(f"{HOST}/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urlopen(req) as response:
        return json.load(response)["message"]


def executar(descricao_vaga=False):
    messages = [{"role": "user", "content": PERGUNTA}]
    tools = ferramentas(descricao_vaga)
    chamadas = []

    for passo in range(1, MAX_PASSOS + 1):
        message = chat(messages, tools)
        messages.append(message)
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return {
                "passos": passo,
                "chamadas": chamadas,
                "primeira_tool_correta": chamadas[:1] == ["consultar_texto"],
                "resposta": message.get("content", ""),
            }

        for call in tool_calls:
            fn = call["function"]
            nome, args = fn["name"], fn.get("arguments", {})
            chamadas.append(nome)
            if nome == "nome_disciplina":
                resultado = nome_disciplina()
            elif nome == "consultar_texto":
                resultado = consultar_texto(**args)
            else:
                resultado = "tool desconhecida"
            messages.append({"role": "tool", "tool_name": nome, "content": str(resultado)})

    return {"passos": MAX_PASSOS, "chamadas": chamadas, "primeira_tool_correta": False,
            "resposta": "MAX_PASSOS atingido"}


if __name__ == "__main__":
    for rotulo, vaga in [("descrição clara", False), ("descrição vaga", True)]:
        print(f"\n--- {rotulo} ---")
        print(json.dumps(executar(vaga), ensure_ascii=False, indent=2))
