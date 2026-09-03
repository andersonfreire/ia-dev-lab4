## Purpose
Define os requisitos para registro de métricas de explicabilidade, monitoramento de confiança e o mecanismo de bloqueio preventivo de modelos em degradação para garantir total transparência.

## ADDED Requirements

### Requirement: Registro de Métricas e Restrições (Edge Cases)
O sistema SHALL registrar métricas de explicabilidade para predições de alto risco, validando rigorosamente o payload de entrada.

#### Scenario: Ingestão com Sucesso (Caminho Feliz)
- **GIVEN** um payload de alto risco com `confidence_score` válido (ex: 0.85) e uma matriz `explanations` preenchida
- **WHEN** enviado para a API de auditoria
- **THEN** os dados são armazenados assincronamente e a API retorna HTTP 201 Created.

#### Scenario: Rejeição por Má Formação (Caso de Borda)
- **GIVEN** um payload onde `confidence_score` está fora do intervalo [0.0, 1.0] (ex: 1.5) OU a matriz `explanations` está vazia `[]`
- **WHEN** enviado para a API de auditoria
- **THEN** a validação intercepta a requisição e retorna explicitamente HTTP 400 Bad Request (sobrescrevendo o 422 padrão).

### Requirement: Bloqueio Preventivo (Circuit Breaker)
O sistema SHALL monitorar a degradação e travar o modelo automaticamente caso a confiança caia abaixo da média tolerável.

#### Scenario: Degradação detectada em janela móvel
- **GIVEN** que a média do `confidence_score` das últimas 50 predições caia para um valor inferior a 0.70
- **WHEN** o monitoramento assíncrono avalia a janela de métricas
- **THEN** o status do modelo no banco é alterado para "BLOCKED", e o sistema emite um log local de nível CRITICAL.