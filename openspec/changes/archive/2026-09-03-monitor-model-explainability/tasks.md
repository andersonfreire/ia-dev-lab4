## 1. Configuração e Validação Estrita (Pydantic)
- [x] 1.1 Atualizar os esquemas de validação (Pydantic) para incluir `confidence_score` (float com limite estrito de 0.0 a 1.0) e `explanations` (lista/array não vazia se risco for "Crítico").
- [x] 1.2 Sobrescrever o tratador de exceções de validação no FastAPI para que erros no payload retornem HTTP 400 Bad Request, implementando testes unitários para confirmar a rejeição de matrizes vazias e scores fora do limite.
- [x] 1.3 Atualizar o esquema do banco de dados relacional (`audit_metrics`) para suportar a gravação das novas colunas de explicabilidade, confiança e o status atual do modelo (ex: "ACTIVE", "BLOCKED").

## 2. Coleta Assíncrona
- [x] 2.1 Implementar a rota de ingestão que valida os dados via Pydantic e despacha a gravação no banco de dados como uma tarefa em background (assíncrona), retornando HTTP 201 Created imediatamente para não impactar a latência.

## 3. Lógica de Bloqueio Preventivo (Circuit Breaker)
- [x] 3.1 Implementar o serviço de cálculo de degradação: consultar as últimas 50 predições (janela móvel) do modelo; se a média do `confidence_score` for menor que 0.70, alterar o status do modelo para "BLOCKED".
- [x] 3.2 Implementar a interceptação de predições: verificar o status do modelo no banco/cache antes da inferência; se "BLOCKED", rejeitar requisições de imediato e emitir um log de sistema nível CRITICAL (não integrar APIs externas de alerta).
- [x] 3.3 Escrever testes unitários (Pytest) comprovando que o cálculo matemático ativa o status "BLOCKED" corretamente ao cruzar o threshold e que o log CRITICAL é disparado.