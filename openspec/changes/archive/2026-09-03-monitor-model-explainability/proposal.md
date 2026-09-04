## Why

A governança de IA exige transparência total nas decisões automatizadas, especialmente em predições de alto risco. Sem o registro adequado de métricas de explicabilidade e o monitoramento contínuo dos níveis de confiança, não é possível auditar os modelos eficazmente nem intervir quando eles começam a degradar, expondo o sistema a riscos de conformidade e segurança.

## What Changes

- Implementação do registro de métricas de explicabilidade para predições de alto risco.
- Adição de monitoramento contínuo do nível de confiança dos modelos.
- Implementação de um mecanismo de bloqueio preventivo de modelos que apresentam degradação em suas métricas de confiança e explicabilidade.

## Capabilities

### New Capabilities
- `model-explainability`: Define os requisitos para registro de métricas de explicabilidade, monitoramento de confiança e o mecanismo de bloqueio preventivo de modelos em degradação.

### Modified Capabilities
- 

## Impact

- Novos endpoints e serviços para receber, armazenar e consultar métricas de explicabilidade.
- Modificações no fluxo de predição (inference) para coletar as métricas de confiança e acionar o bloqueio quando necessário.
- Possíveis impactos em bancos de dados para armazenar o log de explicabilidade e histórico de confiança.
