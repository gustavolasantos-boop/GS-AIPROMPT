"""
src/alertas.py — Thresholds, regras de decisão e respostas automatizadas
Trilha: AgroSat · Satélite Multiespectral

A lógica de decisão é implementada em Python puro (não no prompt da IA).
A IA recebe os alertas já processados para contextualizar o impacto terrestre.
"""

from src.telemetria import LIMITES

# ─────────────────────────────────────────────
#  Níveis de severidade
# ─────────────────────────────────────────────
NORMAL   = "NORMAL"
ALERTA   = "ALERTA"
CRITICO  = "CRÍTICO"


# ─────────────────────────────────────────────
#  Avaliação individual de cada parâmetro
# ─────────────────────────────────────────────

def _avaliar_saude_ndvi(valor: float) -> tuple[str, str]:
    """Avalia o sensor multiespectral (NDVI)."""
    if valor < LIMITES["saude_ndvi"]["critico"]:
        return CRITICO, (
            f"Sensor NDVI em estado CRÍTICO ({valor:.3f}). "
            "Degradação severa compromete geração de imagens multiespectrais. "
            "Produtores rurais perdem acesso a dados de NDVI para monitoramento de safra."
        )
    elif valor < LIMITES["saude_ndvi"]["min"]:
        return ALERTA, (
            f"Sensor NDVI com desempenho reduzido ({valor:.3f}). "
            "Imagens podem apresentar ruído — precisão dos índices vegetativos afetada."
        )
    return NORMAL, f"Sensor NDVI operacional ({valor:.3f})."


def _avaliar_temperatura_payload(valor: float) -> tuple[str, str]:
    """Avalia a temperatura do payload óptico."""
    if valor > LIMITES["temperatura_payload"]["critico"]:
        return CRITICO, (
            f"Temperatura do payload CRÍTICA ({valor:.1f}°C). "
            "Risco de dano permanente ao sensor óptico. "
            "Modo de proteção térmica ativado automaticamente — câmeras desligadas."
        )
    elif valor > LIMITES["temperatura_payload"]["max"]:
        return ALERTA, (
            f"Temperatura do payload elevada ({valor:.1f}°C). "
            "Qualidade de imagem pode ser afetada por expansão térmica dos espelhos."
        )
    return NORMAL, f"Temperatura do payload dentro do nominal ({valor:.1f}°C)."


def _avaliar_armazenamento(valor: float) -> tuple[str, str]:
    """Avalia a capacidade de armazenamento."""
    if valor > LIMITES["armazenamento"]["critico"]:
        return CRITICO, (
            f"Armazenamento CRÍTICO ({valor:.1f}%). "
            "Buffer de imagens quase cheio — capturas novas serão descartadas. "
            "Downlink prioritário deve ser iniciado imediatamente."
        )
    elif valor > LIMITES["armazenamento"]["max"]:
        return ALERTA, (
            f"Armazenamento alto ({valor:.1f}%). "
            "Recomenda-se priorizar downlink na próxima janela disponível."
        )
    return NORMAL, f"Armazenamento dentro do normal ({valor:.1f}%)."


def _avaliar_janela_downlink(valor: float) -> tuple[str, str]:
    """Avalia o tempo restante para a janela de downlink."""
    if valor < LIMITES["janela_downlink"]["critico"]:
        return CRITICO, (
            f"Janela de downlink IMINENTE ({valor:.1f} min). "
            "Iniciar protocolo de transmissão imediatamente para não perder a janela."
        )
    elif valor < LIMITES["janela_downlink"]["min"]:
        return ALERTA, (
            f"Janela de downlink se aproximando ({valor:.1f} min). "
            "Preparar fila de transmissão prioritária."
        )
    return NORMAL, f"Próxima janela de downlink em {valor:.1f} min."


def _avaliar_estabilidade_atitude(valor: float) -> tuple[str, str]:
    """Avalia a estabilidade de atitude do satélite."""
    if valor > LIMITES["estabilidade_atitude"]["critico"]:
        return CRITICO, (
            f"Instabilidade de atitude CRÍTICA ({valor:.2f} arco-s). "
            "Imagens produzidas são inutilizáveis — desfoque severo. "
            "Sistema de controle de atitude (ADCS) necessita de recalibração urgente."
        )
    elif valor > LIMITES["estabilidade_atitude"]["max"]:
        return ALERTA, (
            f"Instabilidade de atitude detectada ({valor:.2f} arco-s). "
            "Resolução espacial das imagens degradada — imagens agrícolas de menor precisão."
        )
    return NORMAL, f"Atitude estável ({valor:.2f} arco-s)."


def _avaliar_energia(valor: float) -> tuple[str, str]:
    """Avalia o nível de energia disponível."""
    if valor < LIMITES["energia_disponivel"]["critico"]:
        return CRITICO, (
            f"Energia CRÍTICA ({valor:.1f}%). "
            "Modo de economia de energia ativado automaticamente. "
            "Sensores e transmissores não essenciais desligados para preservar sistemas vitais."
        )
    elif valor < LIMITES["energia_disponivel"]["min"]:
        return ALERTA, (
            f"Energia abaixo do ideal ({valor:.1f}%). "
            "Reduzir operações de alta demanda energética. Verificar painéis solares."
        )
    return NORMAL, f"Energia disponível adequada ({valor:.1f}%)."


# ─────────────────────────────────────────────
#  Respostas automatizadas para situações críticas
# ─────────────────────────────────────────────

def _resposta_automatizada(alertas_criticos: list[str]) -> list[str]:
    """
    Gera ações automatizadas com base nos alertas críticos identificados.
    Estas ações são executadas automaticamente pelo sistema de controle.
    """
    acoes = []

    if "temperatura_payload" in alertas_criticos:
        acoes.append("🔴 [AUTO] Payload óptico desligado — modo proteção térmica ativo.")

    if "energia_disponivel" in alertas_criticos:
        acoes.append("🔴 [AUTO] Modo economia de energia ativado — sensores secundários offline.")

    if "armazenamento" in alertas_criticos:
        acoes.append("🟠 [AUTO] Fila de downlink priorizada — transmissão iniciada na próxima janela.")

    if "estabilidade_atitude" in alertas_criticos:
        acoes.append("🔴 [AUTO] Captura de imagens suspensa — recalibração do ADCS em andamento.")

    if "saude_ndvi" in alertas_criticos:
        acoes.append("🔴 [AUTO] Alerta enviado à equipe técnica — diagnóstico do sensor multiespectral necessário.")

    if "janela_downlink" in alertas_criticos:
        acoes.append("🟠 [AUTO] Protocolo de transmissão prioritária iniciado.")

    return acoes


# ─────────────────────────────────────────────
#  Função principal de avaliação
# ─────────────────────────────────────────────

def avaliar(dados: dict) -> dict:
    """
    Avalia os dados de telemetria e retorna um relatório de alertas.

    Retorna:
        dict com:
          - 'detalhes'       : lista de dicts {parametro, nivel, mensagem}
          - 'nivel_geral'    : nível geral da missão (NORMAL / ALERTA / CRÍTICO)
          - 'resumo_texto'   : string formatada para exibição
          - 'acoes_auto'     : lista de ações automatizadas disparadas
          - 'criticos'       : lista de parâmetros em estado crítico
          - 'em_alerta'      : lista de parâmetros em estado de alerta
    """
    avaliacoes = {
        "saude_ndvi":          _avaliar_saude_ndvi(dados["saude_ndvi"]),
        "temperatura_payload": _avaliar_temperatura_payload(dados["temperatura_payload"]),
        "armazenamento":       _avaliar_armazenamento(dados["armazenamento"]),
        "janela_downlink":     _avaliar_janela_downlink(dados["janela_downlink"]),
        "estabilidade_atitude":_avaliar_estabilidade_atitude(dados["estabilidade_atitude"]),
        "energia_disponivel":  _avaliar_energia(dados["energia_disponivel"]),
    }

    detalhes = []
    criticos = []
    em_alerta = []

    for param, (nivel, mensagem) in avaliacoes.items():
        detalhes.append({"parametro": param, "nivel": nivel, "mensagem": mensagem})
        if nivel == CRITICO:
            criticos.append(param)
        elif nivel == ALERTA:
            em_alerta.append(param)

    # Nível geral: pior caso
    if criticos:
        nivel_geral = CRITICO
    elif em_alerta:
        nivel_geral = ALERTA
    else:
        nivel_geral = NORMAL

    # Ações automatizadas
    acoes_auto = _resposta_automatizada(criticos)

    # Resumo textual
    icone = {"NORMAL": "✅", "ALERTA": "⚠️", "CRÍTICO": "🚨"}[nivel_geral]
    linhas_resumo = [
        f"{icone} STATUS GERAL DA MISSÃO: {nivel_geral}",
    ]
    for d in detalhes:
        prefixo = {"NORMAL": "  ✅", "ALERTA": "  ⚠️ ", "CRÍTICO": "  🚨"}[d["nivel"]]
        linhas_resumo.append(f"{prefixo} {d['mensagem']}")

    if acoes_auto:
        linhas_resumo.append("")
        linhas_resumo.append("── Ações Automatizadas Disparadas ──")
        for acao in acoes_auto:
            linhas_resumo.append(f"  {acao}")

    return {
        "detalhes": detalhes,
        "nivel_geral": nivel_geral,
        "resumo_texto": "\n".join(linhas_resumo),
        "acoes_auto": acoes_auto,
        "criticos": criticos,
        "em_alerta": em_alerta,
    }
