# 0001 - Manter Arquitetura de Monólito Modular

## Contexto
O projeto `ia-dev-lab4` (API de Auditoria) gerencia o bloqueio de modelos de IA baseado em métricas de degradação (XAI). A base de código atual possui acoplamento forte entre o roteamento (FastAPI) e o banco de dados (SQLAlchemy). Foi verificada a necessidade de quebrar a aplicação em microsserviços (separar a ingestão de métricas do processo de circuit breaker, por exemplo) para forçar o desacoplamento.

## Decisão
Decidimos não adotar microsserviços e manter a aplicação como um **Monólito Modular**. A refatoração focará na criação de interfaces organizadas entre a camada de apresentação (`main.py`) e a camada de serviços/domínio (`services.py`).

## Consequências
*   **Ganhos:** Mantém a carga cognitiva e o uso de tokens da IA (agentes) baixos, pois todo o contexto reside em um único repositório. Reduz a complexidade de deploy e infraestrutura.
*   **Perdas:** Exige disciplina estrita e ferramentas adicionais (como hooks de CI/CD ou TDD) para garantir que os limites arquiteturais não sejam violados.