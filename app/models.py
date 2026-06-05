"""Modelos y gestor de clientes para la API Sky Fase 2."""

import json
import uuid
from datetime import datetime
from pathlib import Path

from app.validators import validar_email, validar_nombre, validar_rfc, validar_telefono


class Cliente:
    """Representa un cliente de Sky."""

    def __init__(self, nombre, email, rfc, telefono, cliente_id=None, fecha_creacion=None):
        self.id = cliente_id or f"CLI-{uuid.uuid4().hex[:8].upper()}"
        self.nombre = nombre.strip()
        self.email = email.strip()
        self.rfc = rfc.strip().upper()
        self.telefono = telefono.strip()
        self.fecha_creacion = fecha_creacion or datetime.utcnow().isoformat()

        self.validar()

    def validar(self):
        """Valida los datos principales del cliente."""
        if not validar_nombre(self.nombre):
            raise ValueError("El nombre del cliente no es válido.")

        if not validar_email(self.email):
            raise ValueError("El email del cliente no es válido.")

        if not validar_rfc(self.rfc):
            raise ValueError("El RFC del cliente no es válido.")

        if not validar_telefono(self.telefono):
            raise ValueError("El teléfono del cliente no es válido.")

    def actualizar(self, datos):
        """Actualiza datos permitidos del cliente."""
        nuevo_nombre = datos.get("nombre", self.nombre)
        nuevo_email = datos.get("email", self.email)
        nuevo_rfc = datos.get("rfc", self.rfc)
        nuevo_telefono = datos.get("telefono", self.telefono)

        cliente_actualizado = Cliente(
            nombre=nuevo_nombre,
            email=nuevo_email,
            rfc=nuevo_rfc,
            telefono=nuevo_telefono,
            cliente_id=self.id,
            fecha_creacion=self.fecha_creacion,
        )

        self.nombre = cliente_actualizado.nombre
        self.email = cliente_actualizado.email
        self.rfc = cliente_actualizado.rfc
        self.telefono = cliente_actualizado.telefono

    def to_dict(self):
        """Convierte el cliente a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rfc": self.rfc,
            "telefono": self.telefono,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un Cliente desde un diccionario."""
        return cls(
            nombre=datos["nombre"],
            email=datos["email"],
            rfc=datos["rfc"],
            telefono=datos["telefono"],
            cliente_id=datos.get("id"),
            fecha_creacion=datos.get("fecha_creacion"),
        )


class GestorClientes:
    """Gestiona clientes y persistencia en JSON."""

    def __init__(self, ruta_archivo="data/clientes.json"):
        self.ruta_archivo = Path(ruta_archivo)
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        self.clientes = {}
        self.cargar()

    def cargar(self):
        """Carga clientes desde el archivo JSON."""
        if not self.ruta_archivo.exists() or self.ruta_archivo.stat().st_size == 0:
            self.guardar()
            return

        with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)

        self.clientes = {
            datos["id"]: Cliente.from_dict(datos)
            for datos in contenido.get("clientes", [])
        }

    def guardar(self):
        """Guarda clientes en el archivo JSON."""
        contenido = {
            "clientes": [cliente.to_dict() for cliente in self.clientes.values()]
        }

        with self.ruta_archivo.open("w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, indent=2, ensure_ascii=False)

    def listar(self):
        """Lista todos los clientes."""
        return [cliente.to_dict() for cliente in self.clientes.values()]

    def crear(self, datos):
        """Crea un cliente nuevo."""
        cliente = Cliente(
            nombre=datos.get("nombre", ""),
            email=datos.get("email", ""),
            rfc=datos.get("rfc", ""),
            telefono=datos.get("telefono", ""),
        )
        self.clientes[cliente.id] = cliente
        self.guardar()
        return cliente.to_dict()

    def obtener(self, cliente_id):
        """Obtiene un cliente por ID."""
        cliente = self.clientes.get(cliente_id)
        return cliente.to_dict() if cliente else None

    def actualizar(self, cliente_id, datos):
        """Actualiza un cliente existente."""
        cliente = self.clientes.get(cliente_id)
        if not cliente:
            return None

        cliente.actualizar(datos)
        self.guardar()
        return cliente.to_dict()

    def eliminar(self, cliente_id):
        """Elimina un cliente por ID."""
        if cliente_id not in self.clientes:
            return False

        del self.clientes[cliente_id]
        self.guardar()
        return True
