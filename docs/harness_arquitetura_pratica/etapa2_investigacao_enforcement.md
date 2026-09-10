# Etapa 2: TDD como Guard-Rail

## Investigação de Enforcement: TDD Guard (Tarefa 6)
O `tdd-guard` atua como um hook de interceptação (PreToolUse). No cenário do nosso projeto `ia-dev-lab4`, se um agente tentasse escrever uma nova rota antes de escrever o arquivo de teste correspondente, o hook acionaria um modelo "juiz" independente para analisar o *diff*. Ao detectar a ausência da fase "Red", ele bloquearia a gravação dos arquivos do sistema e retornaria um erro obrigando o agente a retroceder, impedindo a geração de código sem cobertura.
