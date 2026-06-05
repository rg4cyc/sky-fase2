"""Validadores para los datos de clientes de Sky Fase 2."""

import re


def validar_nombre(nombre: str) -> bool:
    """Valida que el nombre no esté vacío y tenga al menos dos caracteres."""
    return isinstance(nombre, str) and len(nombre.strip()) >= 2


def validar_email(email: str) -> bool:
    """Valida un formato básico de correo electrónico."""
    if not isinstance(email, str):
        return False

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(patron, email.strip()) is not None


def validar_rfc(rfc: str) -> bool:
    """Valida RFC mexicano básico: 4 letras, 6 dígitos y 3 alfanuméricos."""
    if not isinstance(rfc, str):
        return False

    patron = r"^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$"
    return re.match(patron, rfc.strip().upper()) is not None


def validar_telefono(telefono: str) -> bool:
    """Valida teléfono mexicano básico de 10 dígitos."""
    if not isinstance(telefono, str):
        return False

    return re.match(r"^\d{10}$", telefono.strip()) is not None
