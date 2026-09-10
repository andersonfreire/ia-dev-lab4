# Etapa 5: Documentação como Contrato (Diagramas C4)

## Versão 1: Diagrama Básico (Prompt Genérico)
**Prompt utilizado:** "Gere um diagrama C4 da arquitetura atual do projeto."

```mermaid
graph TD
    User(Usuário/Sistema Externo) --> API[FastAPI - main.py]
    API --> Services[Regras de Negócio - services.py]
    API --> DB[(SQLite - audit.db)]
    Services --> DB
    Services --> Schemas[Pydantic - schemas.py]
```

## Versão 2: Diagrama Refinado (Prompt Contextualizado com Padrão C4)
**Prompt utilizado:** "Gere um diagrama C4 Container em Mermaid da nossa API. Separe explicitamente o contexto do usuário, os limites do container da API e os componentes internos (Rotas, Background Tasks, Serviços de Degradação) e a base de dados. Use a sintaxe nativa do Mermaid."

```mermaid
flowchart TD
    %% Atores
    User["Sistemas Clientes / Monitores de ML"]:::person

    %% Fronteira do Sistema
    subgraph SystemBoundary [Audit API System]
        
        %% Containers Internos
        subgraph AppContainer [FastAPI Application]
            Router["Roteador HTTP (main.py)"]:::component
            BGTask["Background Tasks (Ingestão Assíncrona)"]:::component
            Service["Audit Service & Circuit Breaker (services.py)"]:::component
            Validator["Validador Pydantic (schemas.py)"]:::component
        end

        Database[("SQLite (audit.db)")]:::database
    end

    %% Relacionamentos
    User -- "Envia métricas / Consulta status via JSON/HTTPS" --> Router
    Router -- "Valida payload" --> Validator
    Router -- "Delega persistência assíncrona" --> BGTask
    Router -- "Consulta status / bypassa regras (Dívida Técnica)" --> Database
    BGTask -- "Executa persistência" --> Service
    Service -- "Calcula degradação e bloqueia" --> Database

    %% Estilização C4 Básica
    classDef person fill:#08427b,color:#fff,stroke:#052e56
    classDef component fill:#85bbf0,color:#000,stroke:#5b82a3
    classDef database fill:#438dd5,color:#fff,stroke:#2e6295
```

## Comparação das Versões (Tarefa 14)
A **Versão 1** foi gerada de forma simples e apenas espelhou a árvore de arquivos, criando setas genéricas sem especificar a intenção da comunicação. Ela falha em documentar eventos críticos, como as *Background Tasks*.
A **Versão 2** (Refinada com ajuste manual e fornecimento de contexto) exibe os detalhes da arquitetura de forma superior. Ela delimita a fronteira do sistema (`SystemBoundary`), utiliza um esquema de cores padrão C4 e, o mais importante, documenta visualmente a dívida técnica atual: a seta direta entre o `Router` e o `Database` ilustrando o vazamento de responsabilidade discutido no ADR 0001.