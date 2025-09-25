# Sistema de Gestión de Biblioteca — Testing Top Down con Stubs (Python + Pytest)

> **One-liner:** Flujo de préstamo implementado Top-Down con *stubs* para `auth` y `db`. Tests listos con `pytest` y CI opcional.

## 🎯 Objetivo
Implementar pruebas **Top Down** de un sistema de biblioteca usando **stubs** para simular módulos no implementados: autenticación y base de datos.

## 🧱 Estructura
```
proyecto_biblioteca/
├── biblioteca_sistema.py
├── requirements.txt
├── stubs/
│   ├── __init__.py
│   ├── database_stub.py
│   └── auth_stub.py
├── test_top_down.py
├── test_top_down_extra.py
├── docs/
│   ├── tests_ok.png
│   ├── analisis_top_down.pdf
│   └── pytest_output.txt
└── .github/workflows/python-tests.yml
```
> **Tip:** `.gitignore` incluido para Python/pytest/venv.

## 🧠 Implementación (Top Down)
- `BibliotecaSistema` orquesta el flujo `prestar_libro(usuario_id, libro_id)`.
- Dependencias **inyectadas**: `db`, `auth` (permiten intercambiar *stubs*, *fakes*, *mocks*).
- Orden de validaciones: **auth → disponibilidad → registro**.
- Respuestas de negocio:
  - `"Usuario no autorizado"`
  - `"Libro no disponible"`
  - `"Préstamo exitoso"`

## 🧪 Pruebas incluidas
- `test_prestamo_exitoso` — happy path.
- `test_usuario_no_autorizado` — rechazo por auth.
- `test_libro_no_disponible` — disponibilidad (ID impar).
- `test_no_llama_db_si_no_autorizado` — asegura orden de validación (no toca BD si falla auth).
- `test_registrar_prestamo_invocado_una_vez` — *spy* simple para verificar llamada y argumentos.
- `test_tabla_decision_basica` — parametrizado de combinaciones clave.
- `test_captura_log_stub` — valida *side-effect* del stub (print).

👉 Ver **screenshot** de ejecución y **análisis** de ventajas en [`/docs`](./docs).

## 🧩 Stubs
- `AuthStub.verificar_usuario`: autoriza IDs `> 0`.
- `DatabaseStub.libro_disponible`: disponible si `libro_id % 2 == 0`.
- `DatabaseStub.registrar_prestamo`: simula registro y deja traza por `print`.

## 🚀 Cómo correrlo

### Windows (PowerShell)
```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
py -m pip install -U pip -r requirements.txt
py -m pytest -v --tb=short
```

### Ubuntu / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip -r requirements.txt
python -m pytest -v --tb=short
```

> Alternativa rápida (Ubuntu): `sudo apt install -y python3-pytest && pytest -v`

## 🛠 CI (GitHub Actions)
Se incluye workflow en `/.github/workflows/python-tests.yml` para ejecutar `pytest` en PRs y en `main`.

## 🗂 Entregables (docs/)
- `tests_ok.png` — “screenshot” de ejecución.
- `analisis_top_down.pdf` — 1 página de ventajas, buenas prácticas y trade-offs.
- `pytest_output.txt` — salida completa de la corrida local.

## 📈 Roadmap corto
1. Casos límite: IDs inválidos (None/str/negativos) y errores de registro.
2. *Fake DB* en memoria para pruebas de integración ligeras.
3. *Mocks* donde importe la secuencia de llamadas.
4. Coverage + *badges* de CI.

---

**Licencia:** MIT • **Autor:** Tú ✨
