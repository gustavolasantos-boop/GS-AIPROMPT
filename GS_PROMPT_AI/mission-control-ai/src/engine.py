"""Motor de análise da Mission Control AI."""

import os
from pathlib import Path

from ollama import Client
from dotenv import load_dotenv

load_dotenv()

# Identificação da trilha — ALTEREM conforme a escolha do grupo
TRILHA = "agrosat"  # "agrosat" | "envirosat" | "connectsat" | "mobilitysat"

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")
    }
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""

    messages = []

    if system:
        messages.append(
            {
                "role": "system",
                "content": system
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:
        response = client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={
                "num_predict": max_tokens,
                "temperature": temperature
            },
            stream=False
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md."""

    path = Path("prompts/system_prompt.md")

    if path.exists():
        return path.read_text(encoding="utf-8")

    return "Você é um assistente."


class MissionEngine:
    """Motor de análise da missão."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):
        return True

    def status_snapshot(self):
        """Retorna um resumo atual da telemetria e dos alertas."""

        from src.telemetria import coletar, formatar_resumo
        from src.alertas import avaliar

        dados = coletar()
        relatorio = avaliar(dados)

        return (
            formatar_resumo(dados)
            + "\n\n"
            + relatorio["resumo_texto"]
        )

    def analyze(self, pergunta_usuario):
        """Analisa a missão usando telemetria + regras Python + IA."""

        from src.telemetria import coletar, formatar_resumo
        from src.alertas import avaliar

        dados = coletar()
        relatorio = avaliar(dados)

        prompt = f"""
PERGUNTA DO OPERADOR:
{pergunta_usuario}

DADOS DE TELEMETRIA:
{formatar_resumo(dados)}

ANÁLISE AUTOMÁTICA:
{relatorio["resumo_texto"]}

NÍVEL GERAL DA MISSÃO:
{relatorio["nivel_geral"]}

ALERTAS CRÍTICOS:
{relatorio["criticos"]}

ALERTAS MODERADOS:
{relatorio["em_alerta"]}

AÇÕES AUTOMÁTICAS EXECUTADAS:
{relatorio["acoes_auto"]}

Explique:

1. O estado técnico do satélite AgroSat.
2. Os riscos operacionais identificados.
3. O impacto para produtores rurais e seguradoras agrícolas.
4. Quais ações devem ser tomadas pela equipe de missão.
5. Use linguagem profissional e objetiva.
"""

        return llm(
            prompt=prompt,
            system=self.system_prompt,
            temperature=0.3
        )
   
