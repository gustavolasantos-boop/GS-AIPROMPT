"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()

session = PromptSession(
    style=Style.from_dict(
        {
            "prompt": "#06B6D4 bold"
        }
    )
)


def show_banner():
    """Banner personalizado da Global Solution 2026.1."""

    titulo1 = pyfiglet.figlet_format(
        "Global Solution",
        font="ansi_shadow"
    )

    titulo2 = pyfiglet.figlet_format(
        "Mission Control AI",
        font="ansi_shadow"
    )

    console.print(
        Text(
            titulo1,
            style="bold #A855F7"
        )
    )

    console.print(
        Text(
            titulo2,
            style="bold #06B6D4"
        )
    )

    console.print(
        Text(
            "🌾 TRILHA 1 — AGROSAT (Sensoriamento Agrícola)",
            style="bold green"
        )
    )

    console.print(
        Panel.fit(
            "[bold]Monitoramento inteligente de satélite multiespectral[/bold]\n\n"
            "🚜 Produtores Rurais\n"
            "📈 Seguro Agrícola\n"
            "🌱 Monitoramento de Safras\n"
            "🛰️ Dados Orbitais + IA Generativa\n\n"
            "Comandos: /help  /status  /clear  /exit",
            title="◆ GLOBAL SOLUTION 2026.1",
            border_style="#06B6D4"
        )
    )


def show_response(text):
    """Renderiza resposta da IA em painel com timestamp."""

    now = datetime.now().strftime("%H:%M")

    console.print(
        Panel(
            text,
            title="◆ Mission Control",
            subtitle=now,
            border_style="#06B6D4"
        )
    )


def run_cli(engine):
    """Loop principal da CLI."""

    show_banner()

    if not engine.is_ready():
        console.print(
            "⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="yellow"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()

        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break

        if user_input == "/help":
            console.print(
                "Comandos: /help /status /about /clear /exit"
            )
            continue

        if user_input == "/status":
            show_response(
                engine.status_snapshot()
            )
            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        # Qualquer outra entrada vai para o motor de análise
        resposta = engine.analyze(user_input)

        show_response(resposta)