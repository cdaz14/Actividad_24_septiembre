import pytest
from biblioteca_sistema import BibliotecaSistema
from stubs.database_stub import DatabaseStub
from stubs.auth_stub import AuthStub

def test_prestamo_exitoso():
    """Prueba el flujo exitoso usando stubs"""
    # ARRANGE: Configurar stubs
    db_stub = DatabaseStub()
    auth_stub = AuthStub()
    sistema = BibliotecaSistema(db_stub, auth_stub)

    # ACT: Ejecutar operación
    resultado = sistema.prestar_libro(usuario_id=1, libro_id=2)

    # ASSERT: Verificar resultado
    assert resultado == "Préstamo exitoso"

def test_usuario_no_autorizado():
    """Prueba rechazo por usuario no autorizado"""
    db_stub = DatabaseStub()
    auth_stub = AuthStub()
    sistema = BibliotecaSistema(db_stub, auth_stub)

    resultado = sistema.prestar_libro(usuario_id=0, libro_id=2)
    assert resultado == "Usuario no autorizado"

def test_libro_no_disponible():
    """Usuario autorizado pero libro no disponible (ID impar)"""
    sistema = BibliotecaSistema(DatabaseStub(), AuthStub())
    assert sistema.prestar_libro(usuario_id=1, libro_id=3) == "Libro no disponible"

def test_no_llama_db_si_no_autorizado():
    """Se valida auth ANTES de consultar BD (orden correcto)"""
    class ExplodingDB:
        def libro_disponible(self, *_):
            raise AssertionError("No debería consultar disponibilidad si el usuario no está autorizado")
        def registrar_prestamo(self, *_):
            raise AssertionError("No debería registrar si el usuario no está autorizado")
    sistema = BibliotecaSistema(ExplodingDB(), AuthStub())
    assert sistema.prestar_libro(usuario_id=0, libro_id=2) == "Usuario no autorizado"

def test_registrar_prestamo_invocado_una_vez():
    """Happy path: registrar_prestamo se invoca una sola vez con args correctos"""
    class SpyDB(DatabaseStub):
        def __init__(self):
            self.calls = []
        def registrar_prestamo(self, usuario_id, libro_id):
            self.calls.append((usuario_id, libro_id))
            return True

    spy_db = SpyDB()
    sistema = BibliotecaSistema(spy_db, AuthStub())
    out = sistema.prestar_libro(usuario_id=42, libro_id=10)
    assert out == "Préstamo exitoso"
    assert spy_db.calls == [(42, 10)]

@pytest.mark.parametrize("usuario_id, libro_id, esperado", [
    (1, 2, "Préstamo exitoso"),
    (1, 5, "Libro no disponible"),
    (0, 2, "Usuario no autorizado"),
    (-7, 100, "Usuario no autorizado"),
])
def test_tabla_decision_basica(usuario_id, libro_id, esperado):
    """Cobertura rápida de combinaciones clave"""
    sistema = BibliotecaSistema(DatabaseStub(), AuthStub())
    assert sistema.prestar_libro(usuario_id=usuario_id, libro_id=libro_id) == esperado

def test_captura_log_stub(capsys):
    """Verifica el print del stub de registro (documenta el side-effect esperado)"""
    sistema = BibliotecaSistema(DatabaseStub(), AuthStub())
    sistema.prestar_libro(usuario_id=1, libro_id=2)
    captured = capsys.readouterr().out
    assert "[STUB] Préstamo: User=1, Book=2" in captured