## Etapa 5: Comparação de Abordagens SDD

**Abordagens Comparadas:** 
1. Markdown Manual (Gemini + Intervenção Humana)
2. OpenSpec Framework (Extensão Antigravity)

**1. Estratégias de Especificação e Gestão de Artefatos**
A experiência de aplicar o Spec-Driven Development sob duas metodologias distintas evidenciou trade-offs claros entre flexibilidade e governança. 

Na abordagem **Markdown Manual**, houvecflexibilidade na estruturação. A geração dos artefatos (`proposal.md`, `design.md`, `tasks.md`) foi conduzida via prompt, exigindo intervenção humana constante para criar arquivos, organizar pastas e garantir que o modelo não perdesse o contexto das tarefas anteriores. Embora ótimo para ideação, o custo cognitivo de manter o sincronismo entre a documentação e o código gerado foi mais alto.

Já com o **OpenSpec**, a estruturação dos artefatos foi centralizada pelo framework. A utilização de comandos (`/opsx-propose`, `/opsx-apply`, `/opsx-archive`) reduziu a responsabilidade de gestão de arquivos e impôs uma padronização. O framework demonstrou maior controle, rastreando o estado de cada tarefa e pausando a execução autonomamente quando o plano divergiu do estado do diretório atual, forçando uma tomada de decisão arquitetural. 

**2. Comparação do Código Gerado e Arquitetura**
Ao analisar a execução técnica e o código final produzido por cada abordagem, podemos destacar:

*   **Código via Markdown Manual:** O código gerado tendia a ser fragmentado. O LLM entregava blocos funcionais baseados na janela de contexto do chat, e a responsabilidade de integrar a arquitetura (unir rotas, *schemas* e banco de dados) e garantir que as restrições da especificação fossem respeitadas recaía totalmente sobre a revisão humana, aumentando o risco de *vibe coding* e perda de contexto.
*   **Código via OpenSpec (`/opsx-apply`):** A geração foi estritamente guiada pelos artefatos. A ferramenta construiu a estrutura do FastAPI e atendeu com precisão os requisitos matemáticos passados no `tasks.md`. No entanto, a comparação demonstrou que a vinculação cega aos requisitos pode gerar falhas de design: o agente implementou a lógica de negócio corretamente, mas cometeu um desvio arquitetural ao posicionar o alerta `CRITICAL` na camada de roteamento em vez da camada de serviços (o que causaria uma degradação silenciosa, evitada no nosso Checkpoint da Etapa 4).

**Conclusão Geral:** 
O SDD via *Markdown manual* funciona bem para provas de conceito e escopos isolados, mas o uso de um *framework integrado* como o OpenSpec provou ser fundamental para escalar o desenvolvimento com IA. O framework traduz fielmente os requisitos para o código e reduz os desvios, liberando o desenvolvedor humano da gestão de arquivos para focar onde sua revisão é indispensável: na validação e correção do design e da arquitetura do software.