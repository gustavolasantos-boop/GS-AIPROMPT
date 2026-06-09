"""
banner_ascii.py — Gerador de banner ASCII para Mission Control AI · AgroSat

Uso:
    python banner_ascii.py              # Exibe o banner padrão
    python banner_ascii.py -fonts       # Lista fontes disponíveis
    python banner_ascii.py -font slant -text "AgroSat"
    python banner_ascii.py -demo        # Demonstra 8 fontes diferentes
"""

import sys
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()


def show_banner():
    """Exibe o banner principal da Mission Control AI · AgroSat."""
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")
    linha3 = pyfiglet.figlet_format("AgroSat", font="small")

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(Text(linha3, style="bold #22C55E")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))
    console.print(Align.center(
        Text("🌾  Trilha 1 — Sensoriamento Agrícola · Satélite Multiespectral",
             style="#22C55E")
    ))
    console.print()


def list_fonts():
    """Lista todas as fontes disponíveis no PyFiglet."""
    fonts = pyfiglet.FigletFont.getFonts()
    console.print(Panel(
        "\n".join(sorted(fonts)),
        title=f"[bold cyan]{len(fonts)} fontes disponíveis[/bold cyan]",
        border_style="cyan"
    ))


def demo_fonts():
    """Demonstra 8 fontes diferentes com o texto AgroSat."""
    fontes = ["ansi_shadow", "slant", "small", "banner", "block", "bubble", "digital", "lean"]
    texto = "AgroSat"
    for fonte in fontes:
        try:
            resultado = pyfiglet.figlet_format(texto, font=fonte)
            console.print(Panel(
                Text(resultado, style="bold #06B6D4"),
                title=f"[bold]Fonte: {fonte}[/bold]",
                border_style="#8484A0"
            ))
        except Exception:
            console.print(f"[red]Fonte '{fonte}' não disponível[/red]")


def custom_banner(font: str, text: str):
    """Exibe banner customizado com fonte e texto especificados."""
    try:
        resultado = pyfiglet.figlet_format(text, font=font)
        console.print(Text(resultado, style="bold #06B6D4"))
    except pyfiglet.FontNotFound:
        console.print(f"[red]Fonte '{font}' não encontrada. Use -fonts para listar as disponíveis.[/red]")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        show_banner()
    elif "-fonts" in args:
        list_fonts()
    elif "-demo" in args:
        demo_fonts()
    elif "-font" in args and "-text" in args:
        try:
            font_idx = args.index("-font") + 1
            text_idx = args.index("-text") + 1
            custom_banner(args[font_idx], args[text_idx])
        except IndexError:
            console.print("[red]Uso: python banner_ascii.py -font <nome> -text <texto>[/red]")
    else:
        show_banner()