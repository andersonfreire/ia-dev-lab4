## Comparação de Tarefas: Com TDD vs Sem TDD (Tarefas 5 e 7)

*   **Implementação COM TDD (`/api/v1/audit/models/{model_name}/status`):**
    A exigência de fazer o teste `test_get_model_status_not_found` passar forçou o agente a ser preciso. Ele respeitou a arquitetura do projeto, isolando a consulta SQLAlchemy em `services.py` e mantendo o `main.py` limpo apenas para o roteamento e injeção de dependência. O código gerado foi coeso e atendeu exatamente ao requisito.

*   **Implementação SEM TDD (`/api/v1/audit/summary`):**
    Com liberdade total e sem testes para limitar as ações de acordo o design, o agente gerou dívida técnica:
    1. **Quebra de Arquitetura:** Acoplou toda a lógica de banco de dados diretamente no roteador (`main.py`), ignorando a camada de serviços.
    2. **Problema de Performance:** Fez uma consulta inicial e, em seguida, disparou um loop `for` realizando uma nova consulta ao banco para cada modelo encontrado, isso degradaria a performance em larga escala.
    3. **Código "Sujo":** Retornou chaves duplicadas no payload JSON (`"blocked"`/`"BLOCKED"`).

**Conclusão:** O TDD atua não apenas como garantia de corretude lógica, mas como um *guardrail* arquitetural contra a tendência natural dos LLMs de adotarem o caminho de menor resistência.