# Etapa 4: Revisão Arquitetural com Apoio de IA

## 1. Resumo da Arquitetura Atual
**Módulos Principais:**
*   `app/main.py`: Atua como Composition Root e Controller. Gerencia as rotas FastAPI, o ciclo de vida do banco de dados e a ingestão assíncrona.
*   `app/services.py`: Contém a lógica central, incluindo a persistência de métricas e o gatilho do *Circuit Breaker* (cálculo de degradação).
*   `app/schemas.py`: Define os contratos de entrada/saída e validações via Pydantic.
*   `app/database.py`: Configura o SQLAlchemy ORM e o banco SQLite síncrono.

**Pontos Críticos de Acoplamento (Vazamento de Responsabilidades):**
*   **Bypass da Camada de Serviço:** O `main.py` acessa o ORM diretamente em várias rotas, acoplando a camada HTTP aos detalhes das tabelas e gerando problemas graves de performance (N+1 queries na rota de sumário).
*   **Regras Hardcoded:** Limiares matemáticos (0.70) e status ("BLOCKED") estão espalhados e duplicados, sem o uso de constantes ou objetos de domínio ricos.
*   **Falta de Inversão de Dependência:** O `services.py` depende de instâncias concretas do SQLAlchemy e Pydantic, impossibilitando testes unitários isolados da lógica do *Circuit Breaker*.

## 2. Decisão Arquitetural
**Decisão:** O projeto não deve ser dividido em microsserviços. Ele deve permanecer em um único repositório, mas ser refatorado para um **Monólito Modular**.

**Justificativa:**
A adoção de uma arquitetura baseada em microsserviços neste estágio adicionaria uma complexidade operacional desnecessária. Como agentes de IA dedicam a maior parte de sua capacidade de processamento à leitura de contexto, fragmentar o código em serviços independentes resultaria num aumento de complexidade no entendimento das fronteiras de negócio e na manutenção automatizada.

Em sistemas de gestão cibernética, onde as métricas de explicabilidade (XAI) determinam o bloqueio imediato de uma ameaça, as regras matemáticas não podem tolerar vazamentos. O monólito modular mantém a lógica, as transações e as dependências localizadas em um único contexto para a IA. O foco da refatoração será estabelecer interfaces mais organizadas entre o roteamento e o domínio, impedindo que os agentes pulem a camada de serviço e criem acoplamentos diretos com o banco de dados.