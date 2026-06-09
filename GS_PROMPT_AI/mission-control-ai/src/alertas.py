"""
src/telemetria.py — Geração de dados simulados de telemetria
Trilha: AgroSat · Satélite Multiespectral (similar a CBERS-4A / Planet Labs)

Parâmetros monitorados:
  1. saude_ndvi        — Saúde do sensor multiespectral (índice NDVI 0.0–1.0)
  2. temperatura_payload — Temperatura do payload óptico (°C)
  3. armazenamento      — Capacidade de armazenamento usada (%)
  4. janela_downlink    — Tempo restante para próxima janela de downlink (min)
  5. estabilidade_atitude — Desvio de atitude em arco-segundos (menor = melhor)
  6. energia_disponivel — Nível de energia dos painéis solares (%)
"""

import random
import time
from datetime import datetime


# ─────────────────────────────────────────────
#  Thresholds de operação normal (limites seguros)
# ─────────────────────────────────────────────
LIMITES = {
    "saude_ndvi": {
        "min": 0.85,   # sensor degradado abaixo disso
        "critico": 0.60
    },
    "temperatura_payload": {
        "max": 35.0,   # °C — acima disso o sensor aquece demais
        "critico": 45.0
    },
    "armazenamento": {
        "max": 80.0,   # % — acima disso precisa de downlink urgente
        "critico": 95.0
    },
    "janela_downlink": {
        "min": 10.0,   # minutos — abaixo disso downlink iminente
        "critico": 2.0
    },
    "estabilidade_atitude": {
        "max": 5.0,    # arco-segundos — acima disso imagens ficam borradas
        "critico": 15.0
    },
    "energia_disponivel": {
        "min": 30.0,   # % — abaixo disso modo economia ativo
        "critico": 15.0
    }
}


def _valor_normal():
    """Retorna um conjunto de valores dentro dos limites normais."""
    return {
        "saude_ndvi": round(random.uniform(0.88, 0.99), 3),
        "temperatura_payload": round(random.uniform(18.0, 30.0), 1),
        "armazenamento": round(random.uniform(20.0, 65.0), 1),
        "janela_downlink": round(random.uniform(15.0, 90.0), 1),
        "estabilidade_atitude": round(random.uniform(0.5, 3.5), 2),
        "energia_disponivel": round(random.uniform(55.0, 90.0), 1),
    }


def _valor_alerta():
    """Retorna um conjunto com pelo menos um parâmetro em estado de alerta."""
    dados = _valor_normal()
    # Escolhe aleatoriamente 1 a 2 parâmetros para colocar em alerta
    parametros_em_alerta = random.sample(list(LIMITES.keys()), k=random.randint(1, 2))
    for param in parametros_em_alerta:
        if param == "saude_ndvi":
            dados[param] = round(random.uniform(0.61, 0.84), 3)
        elif param == "temperatura_payload":
            dados[param] = round(random.uniform(36.0, 44.0), 1)
        elif param == "armazenamento":
            dados[param] = round(random.uniform(81.0, 94.0), 1)
        elif param == "janela_downlink":
            dados[param] = round(random.uniform(3.0, 9.9), 1)
        elif param == "estabilidade_atitude":
            dados[param] = round(random.uniform(5.1, 14.9), 2)
        elif param == "energia_disponivel":
            dados[param] = round(random.uniform(16.0, 29.9), 1)
    return dados


def _valor_critico():
    """Retorna um conjunto com pelo menos um parâmetro em estado crítico."""
    dados = _valor_normal()
    param_critico = random.choice(list(LIMITES.keys()))
    if param_critico == "saude_ndvi":
        dados[param_critico] = round(random.uniform(0.30, 0.59), 3)
    elif param_critico == "temperatura_payload":
        dados[param_critico] = round(random.uniform(45.1, 65.0), 1)
    elif param_critico == "armazenamento":
        dados[param_critico] = round(random.uniform(95.1, 99.9), 1)
    elif param_critico == "janela_downlink":
        dados[param_critico] = round(random.uniform(0.1, 1.9), 1)
    elif param_critico == "estabilidade_atitude":
        dados[param_critico] = round(random.uniform(15.1, 40.0), 2)
    elif param_critico == "energia_disponivel":
        dados[param_critico] = round(random.uniform(5.0, 14.9), 1)
    return dados


# ─────────────────────────────────────────────
#  Função principal de coleta
# ─────────────────────────────────────────────

# Contador de ciclos para simular variação temporal
_ciclo = 0

def coletar(modo: str = "auto") -> dict:
    """
    Coleta dados simulados da telemetria do AgroSat.

    Parâmetros:
        modo: "auto"    — alterna entre normal/alerta/critico ao longo dos ciclos
              "normal"  — sempre retorna valores normais
              "alerta"  — sempre retorna valores em alerta
              "critico" — sempre retorna valores críticos

    Retorna:
        dict com os 6 parâmetros de telemetria + metadados (timestamp, orbita, modo)
    """
    global _ciclo
    _ciclo += 1

    # Modo automático: simula ciclos variados para demonstração
    if modo == "auto":
        # Ciclo 1-4: normal, Ciclo 5-6: alerta, Ciclo 7: critico, repete
        fase = _ciclo % 7
        if fase in (0, 5):
            dados = _valor_alerta()
        elif fase == 6:
            dados = _valor_critico()
        else:
            dados = _valor_normal()
    elif modo == "normal":
        dados = _valor_normal()
    elif modo == "alerta":
        dados = _valor_alerta()
    elif modo == "critico":
        dados = _valor_critico()
    else:
        dados = _valor_normal()

    # Adiciona metadados da missão
    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["orbita"] = 14230 + _ciclo          # número de órbita simulado
    dados["altitude_km"] = 615                 # órbita baixa (LEO), estilo CBERS-4A
    dados["ciclo"] = _ciclo
    dados["modo_simulacao"] = modo

    return dados


def formatar_resumo(dados: dict) -> str:
    """
    Formata os dados de telemetria em texto legível para exibição no terminal.
    """
    linhas = [
        f"📡 AgroSat · Órbita #{dados['orbita']} · {dados['timestamp']}",
        f"🛰  Altitude: {dados['altitude_km']} km (LEO)",
        "",
        f"  🌿 Saúde NDVI (sensor multiespectral) : {dados['saude_ndvi']:.3f}",
        f"  🌡  Temperatura do payload óptico      : {dados['temperatura_payload']:.1f} °C",
        f"  💾  Armazenamento usado                : {dados['armazenamento']:.1f} %",
        f"  📶  Próxima janela de downlink          : {dados['janela_downlink']:.1f} min",
        f"  🎯  Estabilidade de atitude             : {dados['estabilidade_atitude']:.2f} arco-s",
        f"  ⚡  Energia disponível (painéis solares): {dados['energia_disponivel']:.1f} %",
    ]
    return "\n".join(linhas)
