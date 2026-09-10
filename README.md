# Audit API - XAI Circuit Breaker

## 📌 Sobre o Projeto
A **Audit API** é um sistema de governança e auditoria para modelos de Inteligência Artificial. Ela atua como um *Circuit Breaker*, monitorando continuamente as métricas de explicabilidade (XAI) e o nível de confiança das predições. Caso um modelo apresente degradação (ex: confiança média abaixo de 0.70 em uma janela de 50 requisições), a API bloqueia o modelo automaticamente para evitar decisões automatizadas de alto risco.

Este projeto foi desenvolvido como laboratório prático  para validar práticas de desenvolvimento guiado por IA, SDD, autonomia segura, TDD como *guardrail* e orquestração de agentes.

## 🏗️ Arquitetura
O sistema foi desenhado sob o padrão de **Monólito Modular** (conforme [ADR 0001](docs/adr/0001-manter-monolito-modular.md)), visando manter a carga cognitiva e o consumo de tokens baixos para agentes de IA, centralizando o contexto em um único repositório.

**Stack Tecnológico:**
* **Framework Web:** FastAPI (Python 3.11+)
* **Validação de Contratos:** Pydantic v2
* **Persistência:** SQLAlchemy ORM com SQLite (Síncrono)
* **Testes:** Pytest e HTTPX

**Estrutura de Diretórios:**
```text
ia-dev-lab4/
├── .githooks/          # Scripts de proteção de governança (XAI Circuit Breaker)
├── app/
│   ├── main.py         # Roteamento (Composition Root) e Injeção de Dependências
│   ├── services.py     # Lógica de Negócio e regras de degradação
│   ├── schemas.py      # Contratos de I/O
│   └── database.py     # Configuração do banco de dados SQLite
├── docs/               # ADRs, Logs de Sessão, e Documentação Arquitetural
└── tests/              # Suíte de testes automatizados
```

## 🚀 Como Executar

### Pré-requisitos
* Python 3.11 ou superior
* Git

### Configuração do Ambiente (PowerShell)
1. **Clone o repositório:**
   ```powershell
   git clone [https://github.com/andersonfreire/ia-dev-lab4.git](https://github.com/andersonfreire/ia-dev-lab4.git)
   cd ia-dev-lab4
   ```

2. **Crie e ative o ambiente virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```powershell
   pip install fastapi[standard] sqlalchemy pytest httpx pydantic
   ```

4. **Inicie o servidor local:**
   ```powershell
   uvicorn app.main:app --port 8000
   ```
   A documentação interativa da API (Swagger) estará disponível em: `http://127.0.0.1:8000/docs`

## 🧪 Testes e Qualidade
O projeto utiliza **TDD (Test-Driven Development)** como mecanismo de governança primário para evitar derivação arquitetural (Architectural Drift) durante a geração de código por IA.

Para rodar a suíte de testes:
```powershell
pytest tests/
```

## 🛡️ Governança e Segurança
Este repositório utiliza *Git Hooks* para evitar modificações destrutivas por agentes autônomos.
Para garantir que os hooks locais sejam aplicados, execute uma única vez após clonar:
```powershell
git config core.hooksPath .githooks
```
Isso impedirá a exclusão acidental do banco de auditoria (`audit.db`) e o uso de comandos nocivos (como `DROP TABLE`).