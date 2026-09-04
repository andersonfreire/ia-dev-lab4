## Context

O projeto atual necessita integrar mecanismos de monitoramento para os modelos de inteligência artificial em produção. Conforme definido na proposal (veja proposal.md), o foco está na coleta da métrica de explicabilidade e no monitoramento de nível de confiança de forma contínua para predições consideradas de alto risco.

## Goals / Non-Goals

**Goals:**
- Prover uma arquitetura de serviço para coletar logs de predições de alto risco de forma assíncrona.
- Integrar um sistema de alerta e bloqueio preventivo (circuit breaker) na pipeline de predição baseado em limiares (thresholds) de degradação.

**Non-Goals:**
- Implementação de rotinas para retreinar ou atualizar automaticamente o modelo de ML bloqueado.
- Criação e experimentação de novas técnicas de ML para explicabilidade (serão usadas bibliotecas/padrões existentes como SHAP).

## Decisions

- **Armazenamento das Métricas:** Utilizar a base de dados relacional atual acoplada à estrutura de auditoria (`audit_metrics` ou similar) para centralizar a persistência de explicabilidade e confiança.
  - *Alternativas:* Usar um banco NoSQL (ex: MongoDB ou ElasticSearch). Descartado por enquanto para aproveitar a infraestrutura e simplificar a adoção inicial, priorizando consistência.
- **Mecanismo de Bloqueio (Preventive Lock):** O bloqueio será efetivado atualizando o status do modelo no banco de dados e invalidando seu estado no cache da API de predição, funcionando como um circuit breaker. 
  - *Alternativas:* Bloqueio assíncrono atrasado. Rejeitado pois predições de alto risco exigem reação imediata em caso de degradação severa.

## Risks / Trade-offs

- [Risk] Aumento na latência das requisições de predição devido ao cálculo de métricas de explicabilidade. → **Mitigação**: O log de explicabilidade será calculado e enviado para gravação em background (assíncrono), após a resposta imediata da predição, ou apenas em amostras específicas de alto risco.
- [Risk] Disparo falso de bloqueio preventivo inviabilizando a operação. → **Mitigação**: A regra de degradação será baseada em médias móveis sobre janelas de tempo/amostra e não em anomalias pontuais exclusivas, acompanhado de envio de alerta imediato aos auditores com opção de destravamento manual.
