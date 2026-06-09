# 🚀 Mission Control AI — AgroSat

## Integrantes

* Gustavo Lima — RM: 571709 — Turma: CCPG

---

## O que o projeto faz

O AgroSat é um sistema inteligente de monitoramento de missão espacial desenvolvido para acompanhar o estado operacional de um satélite multiespectral de sensoriamento agrícola.

A solução utiliza telemetria simulada, regras automatizadas de detecção de alertas e Inteligência Artificial Generativa para interpretar o estado da missão e traduzir impactos técnicos em consequências reais para o agronegócio brasileiro.

---

## Persona atendida

### Operador de Missão Espacial

O sistema foi desenvolvido para auxiliar operadores responsáveis pelo monitoramento do satélite AgroSat. A IA atua como suporte à tomada de decisão, transformando dados técnicos de telemetria em análises operacionais claras e objetivas.

---

Impacto da Missão e Modelo de Negócio
1. Qual o problema real terrestre que esta missão resolve?

O AgroSat busca resolver a dificuldade de monitoramento contínuo e em larga escala das áreas agrícolas. Atualmente, muitos produtores dependem de inspeções presenciais ou imagens esporádicas, o que dificulta a identificação rápida de problemas nas lavouras. Com o monitoramento orbital e análise por Inteligência Artificial, é possível detectar precocemente sinais de estresse hídrico, pragas e falhas de produtividade, permitindo ações corretivas mais rápidas e eficientes.

2. Quem paga pela solução?

O modelo é híbrido. O setor público pode utilizar os dados para monitoramento agrícola, planejamento territorial e políticas de segurança alimentar. O setor privado inclui cooperativas agrícolas, seguradoras rurais, consultorias agronômicas e grandes produtores que necessitam de informações frequentes e confiáveis para apoiar a tomada de decisão.

3. Métrica de impacto

Considerando um satélite operando de forma saudável durante um ano, estima-se a capacidade de monitorar mais de 1 milhão de hectares de áreas agrícolas. Esse acompanhamento contínuo permite identificar problemas mais rapidamente, reduzir perdas de produtividade e melhorar a eficiência do uso de recursos como água e fertilizantes, contribuindo para uma agricultura mais sustentável e competitiva.

4. Modelo de negócio

O modelo de negócio proposto é Dados como Serviço (Data as a Service - DaaS). Os clientes contratam assinaturas para acessar imagens processadas, indicadores agrícolas e análises geradas pela Inteligência Artificial. Dessa forma, cooperativas, seguradoras e produtores podem receber informações atualizadas sem a necessidade de manter infraestrutura própria de sensoriamento remoto.


## Tecnologias utilizadas

* Python 3.13
* Ollama Cloud API (modelo gpt-oss:120b)
* Python Dotenv
* Rich
* Prompt Toolkit
* PyFiglet
* Telemetria simulada em Python
* Engenharia de Prompt

---

## Como executar

### Requisitos

* Python 3.10+
* Chave de acesso Ollama Cloud

### Instalação

1. Clone o repositório

```bash
git clone <url-do-repositorio>
```

2. Entre na pasta do projeto

```bash
cd mission-control-ai
```

3. Crie o ambiente virtual

```bash
python -m venv .venv
```

4. Ative o ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

5. Instale as dependências

```bash
pip install -r requirements.txt
```

6. Crie um arquivo `.env`

```env
OLLAMA_API_KEY=sua_chave_aqui
```

7. Execute o sistema

```bash
python main.py
```

---

## Checklist de Entrega

* [x] README.md completo
* [x] Código Python funcional
* [x] requirements.txt configurado
* [x] .env.example criado
* [x] .gitignore configurado
* [x] Pasta assets com screenshots
* [x] Repositório público

---

## Demonstração

### Banner da Aplicação

![Banner](assets/screenshot_banner.png)

### Exemplo de Análise

![Análise](assets/screenshot_análise.png)

### Exemplo de Alerta

### Análise de Telemetria em Estado de Alerta

![Análise de Alerta](assets/screenshot_alerta.png)
--- 

## System Prompt

O system prompt foi desenvolvido para orientar a IA a atuar como especialista em operações do satélite AgroSat, analisando telemetria orbital e traduzindo impactos técnicos para produtores rurais, seguradoras agrícolas e equipes de missão.

Arquivo:

```text
prompts/system_prompt.md
```

---

## Cenários de teste demonstrados

### 1. Operação Normal

Todos os parâmetros dentro da faixa operacional.

### 2. Sensor NDVI em Alerta

Redução da qualidade dos índices vegetativos utilizados no monitoramento agrícola.

### 3. Temperatura Crítica do Payload

Ativação automática do modo de proteção térmica.

### 4. Baixo Nível de Energia

Entrada em modo de economia de energia.

### 5. Instabilidade de Atitude

Possível degradação da qualidade das imagens capturadas.

### 6. Armazenamento Próximo do Limite

Priorização automática de downlink.

---

## Limitações conhecidas

* Utiliza telemetria simulada..
* Não armazena histórico persistente das análises.
* Dependente da disponibilidade da API Ollama Cloud.
* Não executa comandos reais sobre sistemas espaciais.

---

## Vídeo de demonstração

🎥 Link da apresentação:

```text
(https://www.youtube.com/watch?v=sXNsWkDkpaA)
```

---

## Global Solution 2026.1

FIAP — Inteligência Artificial e Computação Espacial

Trilha 1 — AgroSat (Sensoriamento Agrícola)
