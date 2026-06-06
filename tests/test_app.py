"""Pruebas automatizadas para la API Sky Fase 2."""

import pytest

from app.main import create_app
from app.models import GestorClientes


@pytest.fixture
def cliente_prueba(tmp_path, monkeypatch):
    """Crea cliente de prueba usando un JSON temporal."""
    ruta_temporal = tmp_path / "clientes_test.json"

    def gestor_temporal():
        return GestorClientes(ruta_archivo=ruta_temporal)

    monkeypatch.setattr("app.routes.gestor", gestor_temporal())

    app = create_app()
    app.config.update({"TESTING": True})

    return app.test_client()


def test_health_check(cliente_prueba):
    respuesta = cliente_prueba.get("/health")

    assert respuesta.status_code == 200
    cuerpo = respuesta.get_json()
    assert cuerpo["status"] == "ok"
    assert cuerpo["version"] == "1.1.0"


def test_crear_cliente_valido(cliente_prueba):
    datos = {
        "nombre": "Ana Maria Lopez",
        "email": "ana@ejemplo.com",
        "rfc": "LOMA900101XYZ",
        "telefono": "5512345678",
    }

    respuesta = cliente_prueba.post("/api/clientes", json=datos)
    cuerpo = respuesta.get_json()

    assert respuesta.status_code == 201
    assert cuerpo["cliente"]["nombre"] == "Ana Maria Lopez"
    assert cuerpo["cliente"]["rfc"] == "LOMA900101XYZ"


def test_listar_clientes(cliente_prueba):
    datos = {
        "nombre": "Carlos Perez",
        "email": "carlos@ejemplo.com",
        "rfc": "PECA880101ABC",
        "telefono": "5588889999",
    }

    cliente_prueba.post("/api/clientes", json=datos)
    respuesta = cliente_prueba.get("/api/clientes")
    cuerpo = respuesta.get_json()

    assert respuesta.status_code == 200
    assert cuerpo["total"] == 1


def test_obtener_cliente_por_id(cliente_prueba):
    datos = {
        "nombre": "Laura Torres",
        "email": "laura@ejemplo.com",
        "rfc": "TOLA910101DEF",
        "telefono": "5577778888",
    }

    creado = cliente_prueba.post("/api/clientes", json=datos).get_json()
    cliente_id = creado["cliente"]["id"]

    respuesta = cliente_prueba.get(f"/api/clientes/{cliente_id}")

    assert respuesta.status_code == 200
    assert respuesta.get_json()["cliente"]["id"] == cliente_id


def test_rfc_invalido_debe_fallar(cliente_prueba):
    datos = {
        "nombre": "Cliente Invalido",
        "email": "cliente@ejemplo.com",
        "rfc": "RFCMAL",
        "telefono": "5511112222",
    }

    respuesta = cliente_prueba.post("/api/clientes", json=datos)

    assert respuesta.status_code == 400
    assert "RFC" in respuesta.get_json()["error"]


def test_actualizar_cliente(cliente_prueba):
    datos = {
        "nombre": "Miguel Sanchez",
        "email": "miguel@ejemplo.com",
        "rfc": "SAMI850101GHI",
        "telefono": "5566667777",
    }

    creado = cliente_prueba.post("/api/clientes", json=datos).get_json()
    cliente_id = creado["cliente"]["id"]

    respuesta = cliente_prueba.put(
        f"/api/clientes/{cliente_id}",
        json={"telefono": "5599990000"},
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["cliente"]["telefono"] == "5599990000"


def test_eliminar_cliente(cliente_prueba):
    datos = {
        "nombre": "Sofia Ramirez",
        "email": "sofia@ejemplo.com",
        "rfc": "RASO870101JKL",
        "telefono": "5544443333",
    }

    creado = cliente_prueba.post("/api/clientes", json=datos).get_json()
    cliente_id = creado["cliente"]["id"]

    respuesta = cliente_prueba.delete(f"/api/clientes/{cliente_id}")
    consulta = cliente_prueba.get(f"/api/clientes/{cliente_id}")

    assert respuesta.status_code == 200
    assert consulta.status_code == 404
