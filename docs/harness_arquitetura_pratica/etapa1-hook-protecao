## Hook de Proteção (Tarefas 3 e 4)
**Risco Mitigado:** Exclusão acidental ou indevida do banco de dados de auditoria (`.db` ou `.sqlite`), o que comprometeria o histórico de métricas do *Circuit Breaker*.

**Implementação:** Script `pre-commit` configurado via `core.hooksPath` no diretório `.githooks/`.

**Evidência de Bloqueio (simulação):**
Ao tentar deletar o arquivo de banco de dados e realizar o commit, o hook abortou a operação com a seguinte saída no PowerShell:
```text
PS C:\Users\ander\Documents\ia-dev-lab4> mkdir -p .githooks



Diretório: C:\Users\ander\Documents\ia-dev-lab4



Mode                 LastWriteTime         Length Name

----                 -------------         ------ ----

d-----        09/09/2026     17:07                .githooks



PS C:\Users\ander\Documents\ia-dev-lab4> New-Item -Path .githooks\pre-commit -ItemType File



Diretório: C:\Users\ander\Documents\ia-dev-lab4\.githooks



Mode                 LastWriteTime         Length Name

----                 -------------         ------ ----

-a----        09/09/2026     17:10              0 pre-commit





PS C:\Users\ander\Documents\ia-dev-lab4> git config core.hooksPath .githooks

PS C:\Users\ander\Documents\ia-dev-lab4> New-Item -Path audit_data.db -ItemType File



    Diretório: C:\Users\ander\Documents\ia-dev-lab4





Mode                 LastWriteTime         Length Name

----                 -------------         ------ ----

-a----        09/09/2026     17:16              0 audit_data.db





PS C:\Users\ander\Documents\ia-dev-lab4> git add audit_data.db

PS C:\Users\ander\Documents\ia-dev-lab4> git commit -m "chore: adiciona banco de dados"

[main cbbf903] chore: adiciona banco de dados

 1 file changed, 0 insertions(+), 0 deletions(-)

 create mode 100644 audit_data.db

PS C:\Users\ander\Documents\ia-dev-lab4> git rm audit_data.db

rm 'audit_data.db'

PS C:\Users\ander\Documents\ia-dev-lab4> git commit -m "feat: limpa base de dados"

🚨 ERRO DE GOVERNANÇA: Tentativa de exclusão do banco de auditoria bloqueada pelo hook!

Arquivos protegidos: audit_data.db