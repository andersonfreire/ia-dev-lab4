# Etapa 3: Observabilidade e Checkpoint Humano

## Definição do Checkpoint Humano (Tarefa 9)
**Checkpoint Obrigatório:** Pausa e revisão de diffs antes de qualquer alteração na lógica de cálculo de degradação do *Circuit Breaker* ou na emissão de alertas de segurança (logs críticos).

**Papel Humano Assumido:** *Approver* (Aprovador). Neste nível de Human-in-the-Loop, o desenvolvedor atua como um *gate* de revisão arquitetural, verificando se a IA não comprometeu a segurança antes de aprovar a inserção do código na aplicação.

**Decisão (Cenário Real):**
*   **Ação Proposta pelo Agente:** Durante uma solicitação para refatorar o monitoramento, o agente moveu a emissão do log `CRITICAL` (que avisa que um modelo foi bloqueado) da função de cálculo assíncrono no `services.py` para dentro da camada de roteamento no `main.py`. 
*   **Decisão Tomada:** **Rejeitar (Reject)** e exigir correção.
*   **Justificativa:** Aceitar essa mudança criaria uma "degradação silenciosa". O modelo seria bloqueado no banco de dados, mas o alerta de segurança só seria disparado passivamente caso um usuário chamasse a rota da API. O checkpoint humano garantiu que o disparo do alerta permanecesse acoplado ao exato momento do cálculo matemático no serviço, mantendo a integridade.