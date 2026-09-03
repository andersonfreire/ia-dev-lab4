## Registro de Ferramenta e Abordagem de Especificação (SDD)

**Ferramenta Utilizada:** 
OpenSpec - executado de forma integrada ao Antigravity IDE, orquestrado pelo modelo LLM Gemini 3.1 Pro através do comando automatizado `/opsx-propose`.

**Justificativa:**
A escolha pelo OpenSpec baseou-se na sua característica de ser um *framework* que mantém a especificação estruturada e versionada diretamente no repositório local, junto ao código-fonte da aplicação. 

O uso dessa abordagem SDD foi essencial para afastar o desenvolvimento do improviso do *Vibe Coding*, um risco crítico considerando que o escopo da API de Auditoria ML/XAI exige validações matemáticas estritas e regras de governança. A ferramenta garantiu a separação da intenção em artefatos revisáveis:

1. **O Porquê e O Quê (`proposal.md`)**: Traduziu a necessidade de negócio, justificando a transparência nas decisões automatizadas e o monitoramento contínuo de predições de alto risco.
2. **Critérios de Aceite (`specs/model-explainability/spec.md`)**: Definiu os cenários BDD para a ingestão de métricas XAI, detalhando o "caminho feliz" e as condições para o bloqueio preventivo de modelos.
3. **Decisões Técnicas (`design.md`)**: Estabeleceu a arquitetura antes da codificação, optando pelo uso de tabelas relacionais (`audit_metrics`), processamento de logs assíncrono para mitigar a latência e a adoção de um *circuit breaker* baseado em médias móveis.
4. **Plano de Ação (`tasks.md`)**: Decompôs a implementação técnica em três fases (Configuração e Banco de Dados, Coleta Assíncrona e Lógica de Bloqueio).

Esta segmentação baseada em artefatos viabilizou o checkpoint humano crítico para o projeto. A revisão manual permitiu a edição estrutural do `tasks.md` e do `spec.md`, substituindo abstrações geradas pela IA (como "diferentes thresholds") por limites matemáticos determinísticos — como a trava de *confidence score* em `[0.0, 1.0]`, a janela móvel de 50 requisições com *threshold* de 0.70 e o retorno forçado de HTTP 400. Isso garantiu que as definições de infraestrutura e governança permanecessem sob controle humano antes do início da codificação.