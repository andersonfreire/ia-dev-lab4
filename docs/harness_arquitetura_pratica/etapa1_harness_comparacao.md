# Etapa 1: Harness Mínimo - Autonomia e Guardrail

## Comparação de Modos de Autonomia (Tarefa 2)
**Funcionalidade:** Implementação da rota `GET /api/v1/audit/models/blocked` para listar modelos com status "BLOCKED".
**Ferramenta:** Antigravity

*   **Modo Supervisionado (Chat-assistido / Plan Mode):**
    *   **Tempo:** 44.3 segundos de geração pela IA + tempo de intervenção humana para inserção manual (2 minutos).
    *   **Sensação de Controle:** Alta. A arquitetura pôde ser validada visualmente antes da aplicação, garantindo a separação correta de responsabilidades proposta pela IA (consulta em `services.py` e rota no `main.py`).
    *   **Risco Percebido:** Baixo. Sem permissão de escrita, a ferramenta não apresentou risco de sobrescrever código crítico.

*   **Modo Autônomo (Auto-Apply):**
    *   **Tempo:** 1 minuto e 12 segundo de execução direta.
    *   **Sensação de Controle:** Reduzida. A IA manipulou os arquivos de forma independente.
    *   **Risco Percebido:** Alto. Com liberdade total, o agente optou pelo caminho de menor esforço: não separou as responsabilidades e acoplou a regra de negócio (query do banco de dados) diretamente no roteador do FastAPI (`main.py`). 

**Conclusão:** O modo autônomo gerou dívida técnica ao não seguir o isolamento de camadas. O ganho de tempo não compensou a perda arquitetural, evidenciando que, neste estágio, o modo supervisionado atua como um *guardrail* humano importante.