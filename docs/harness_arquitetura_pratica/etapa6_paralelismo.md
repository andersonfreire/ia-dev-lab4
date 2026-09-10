# Etapa 6: Agentes em Paralelo (Git Worktrees)

## Investigação
**Opção Escolhida:** C (Agentes em Paralelo)

**Ferramenta:** `git worktree`

**O que foi investigado:**
Criamos uma *worktree* paralela (`ia-dev-lab4-worker`) para simular a execução concorrente de dois agentes autônomos operando na mesma base de código. O objetivo foi mapear como recursos compartilhados (portas de rede e banco de dados SQLite) se comportam quando múltiplos agentes tentam rodar a aplicação ou a suíte de testes simultaneamente.

**Evidências e Aprendizados:**

1. **Conflito de Rede (Port Binding):**
   Ao tentar iniciar a aplicação em ambos os terminais simultaneamente usando `uvicorn app.main:app --port 8000`, o agente secundário sofreu uma falha imediata de colisão de porta.
   
   *Logs do Agente 1 e do Agente 2 (Contendo o erro):*
```text
   (venv) PS C:\Users\ander\Documents\ia-dev-lab4> uvicorn app.main:app --port 8000
INFO:     Started server process [9228]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)


(venv) PS C:\Users\ander\Documents\ia-dev-lab4-worker> uvicorn app.main:app --port 8000
INFO:     Started server process [20676]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
ERROR:    [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): normalmente é permitida apenas uma utilização de cada endereço de soquete (protocolo/endereço de rede/porta)   
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete. 
```
   
   *Aprendizado:* Agentes não podem usar portas *hardcoded* (como 8000). Em um ambiente multiagente, é necessária a alocação dinâmica de portas ou a conteinerização (Docker) para isolar as instâncias.

2. **Gargalo de I/O (Database Locking):**
   No Terminal 1, bloqueamos o banco simulando uma alta transação de escrita (`BEGIN EXCLUSIVE` com 15 segundos de retenção). No Terminal 2, disparamos a suíte de testes do módulo de auditoria.
   
   *Logs de Execução do Agente 1 e do Agente 2:*
```text
(venv) PS C:\Users\ander\Documents\ia-dev-lab4> python -c "import sqlite3, time; conn = sqlite3.connect('audit.db'); conn.execute('BEGIN EXCLUSIVE'); time.sleep(15)"
(venv) PS C:\Users\ander\Documents\ia-dev-lab4> 


(venv) PS C:\Users\ander\Documents\ia-dev-lab4-worker> pytest tests/test_audit.py
====================== test session starts ======================
platform win32 -- Python 3.11.0, pytest-9.1.1, pluggy-1.6.0       
rootdir: C:\Users\ander\Documents\ia-dev-lab4-worker
plugins: anyio-4.15.0
collected 1 item                                                 
tests\test_audit.py .                                      [100%]

======================= warnings summary ======================== 

..\ia-dev-lab4\venv\Lib\site-packages\fastapi\testclient.py:1     

C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
from starlette.testclient import TestClient as TestClient  # noqa
..\ia-dev-lab4\venv\Lib\site-packages\starlette\testclient.py:53  

C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.

_PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]
app\schemas.py:16

C:\Users\ander\Documents\ia-dev-lab4-worker\app\schemas.py:16: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
class AuditMetricResponse(AuditMetricCreate):
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

================= 1 passed, 3 warnings in 1.17s ================= 
```
   
   *Aprendizado:* Neste experimento, o teste passou. Isso ocorreu porque o `test_audit.py` aciona uma rota de leitura (`GET`). O SQLite foi capaz de gerenciar a concorrência para a leitura, evidenciando que testes unitários read-only são mais resistentes ao paralelismo do que testes que forçam a escrita intensiva. Ainda assim, em cenários de gravação concorrente (como a inserção das 50 métricas da degradação), o SQLite bloquearia, exigindo um banco robusto como PostgreSQL para arquiteturas multiagente.