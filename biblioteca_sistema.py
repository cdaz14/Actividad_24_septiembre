class BibliotecaSistema:
    def __init__(self, db, auth):
        self.db = db      # Inyección de dependencia
        self.auth = auth  # Inyección de dependencia

    def prestar_libro(self, usuario_id, libro_id):
        # Verificar autorización (usará stub)
        if not self.auth.verificar_usuario(usuario_id):
            return "Usuario no autorizado"

        # Verificar disponibilidad (usará stub)
        if not self.db.libro_disponible(libro_id):
            return "Libro no disponible"

        # Registrar préstamo (usará stub)
        self.db.registrar_prestamo(usuario_id, libro_id)
        return "Préstamo exitoso"
