## TESTE ANTES DA IMPLEMENTAÇÃO

(venv) PS C:\Users\ander\Documents\ia-dev-lab4> pytest tests/test_audit.py
================================================== test session starts ===================================================
platform win32 -- Python 3.11.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ander\Documents\ia-dev-lab4
plugins: anyio-4.15.0
collected 1 item                                                                                                          

tests\test_audit.py F                                                                                               [100%]

======================================================== FAILURES ======================================================== 
____________________________________________ test_get_model_status_not_found _____________________________________________ 

    def test_get_model_status_not_found():
        response = client.get("/api/v1/audit/models/modelo_inexistente/status")
        assert response.status_code == 404
>       assert response.json() == {"detail": "Model not found"}
E       AssertionError: assert {'detail': 'Not Found'} == {'detail': 'Model not found'}
E
E         Differing items:
E         {'detail': 'Not Found'} != {'detail': 'Model not found'}
E         Use -v to get more diff

tests\test_audit.py:9: AssertionError
==================================================== warnings summary ==================================================== 
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

venv\Lib\site-packages\starlette\testclient.py:53
  C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

app\schemas.py:16
  C:\Users\ander\Documents\ia-dev-lab4\app\schemas.py:16: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    class AuditMetricResponse(AuditMetricCreate):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================ short test summary info ================================================= 
FAILED tests/test_audit.py::test_get_model_status_not_found - AssertionError: assert {'detail': 'Not Found'} == {'detail': 'Model not found'}
============================================= 1 failed, 3 warnings in 3.45s ============================================== 

## TESTE APÓS A IMPLEMENTAÇÃO:

(venv) PS C:\Users\ander\Documents\ia-dev-lab4> pytest tests/test_audit.py
================================================== test session starts ===================================================
platform win32 -- Python 3.11.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ander\Documents\ia-dev-lab4
plugins: anyio-4.15.0
collected 1 item                                                                                                          

tests\test_audit.py .                                                                                               [100%]

==================================================== warnings summary ==================================================== 
venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

venv\Lib\site-packages\starlette\testclient.py:53
  C:\Users\ander\Documents\ia-dev-lab4\venv\Lib\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

app\schemas.py:16
  C:\Users\ander\Documents\ia-dev-lab4\app\schemas.py:16: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    class AuditMetricResponse(AuditMetricCreate):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================= 1 passed, 3 warnings in 0.93s ============================================== 
(venv) PS C:\Users\ander\Documents\ia-dev-lab4> 