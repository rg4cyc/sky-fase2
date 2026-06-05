"""Rutas REST para la API de clientes Sky Fase 2."""

from flask import Blueprint, jsonify, request

from app.models import GestorClientes

api = Blueprint("api", __name__)
gestor = GestorClientes()


@api.route("/", methods=["GET"])
def inicio():
    """Endpoint raíz con información básica de la API."""
    return jsonify({
        "mensaje": "Bienvenido a Sky Fase 2",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "listar_clientes": "/api/clientes",
            "crear_cliente": "/api/clientes",
            "obtener_cliente": "/api/clientes/<id>",
            "actualizar_cliente": "/api/clientes/<id>",
            "eliminar_cliente": "/api/clientes/<id>",
        },
    }), 200


@api.route("/health", methods=["GET"])
def health():
    """Endpoint de salud usado para validar que la API está activa."""
    return jsonify({
        "status": "ok",
        "service": "sky-fase2-api",
    }), 200


@api.route("/api/clientes", methods=["GET"])
def listar_clientes():
    """Lista todos los clientes registrados."""
    return jsonify({
        "clientes": gestor.listar(),
        "total": len(gestor.listar()),
    }), 200


@api.route("/api/clientes", methods=["POST"])
def crear_cliente():
    """Crea un nuevo cliente."""
    datos = request.get_json(silent=True) or {}

    try:
        cliente = gestor.crear(datos)
        return jsonify({
            "mensaje": "Cliente creado correctamente.",
            "cliente": cliente,
        }), 201
    except ValueError as error:
        return jsonify({
            "error": str(error),
        }), 400


@api.route("/api/clientes/<cliente_id>", methods=["GET"])
def obtener_cliente(cliente_id):
    """Obtiene un cliente por ID."""
    cliente = gestor.obtener(cliente_id)

    if not cliente:
        return jsonify({
            "error": "Cliente no encontrado.",
        }), 404

    return jsonify({
        "cliente": cliente,
    }), 200


@api.route("/api/clientes/<cliente_id>", methods=["PUT"])
def actualizar_cliente(cliente_id):
    """Actualiza un cliente existente."""
    datos = request.get_json(silent=True) or {}

    try:
        cliente = gestor.actualizar(cliente_id, datos)
    except ValueError as error:
        return jsonify({
            "error": str(error),
        }), 400

    if not cliente:
        return jsonify({
            "error": "Cliente no encontrado.",
        }), 404

    return jsonify({
        "mensaje": "Cliente actualizado correctamente.",
        "cliente": cliente,
    }), 200


@api.route("/api/clientes/<cliente_id>", methods=["DELETE"])
def eliminar_cliente(cliente_id):
    """Elimina un cliente existente."""
    eliminado = gestor.eliminar(cliente_id)

    if not eliminado:
        return jsonify({
            "error": "Cliente no encontrado.",
        }), 404

    return jsonify({
        "mensaje": "Cliente eliminado correctamente.",
    }), 200
