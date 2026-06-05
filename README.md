# Sky Fase 2 - API de Gestion de Clientes

API REST desarrollada en Python con Flask para la gestion de clientes de Sky en la Fase 2 del proyecto DevOps.

## Tecnologias

- Python
- Flask
- JSON
- pytest
- flake8
- Docker
- GitHub Actions
- AWS EC2

## Estructura del proyecto

sky-fase2/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── validators.py
├── tests/
│   └── test_app.py
├── data/
├── docs/
├── .github/workflows/
├── Dockerfile
├── requirements.txt
└── README.md

## Endpoints principales

GET     /
GET     /health
GET     /api/clientes
POST    /api/clientes
GET     /api/clientes/<id>
PUT     /api/clientes/<id>
DELETE  /api/clientes/<id>

## Ejecucion local

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m flask --app app.main run --host 0.0.0.0 --port 8000 --debug

## Pruebas

pytest tests/ -v

## Lint

flake8 app tests

## Docker

docker build -t sky-fase2:v1 .
docker run -d -p 8000:5000 --name sky_fase2_app sky-fase2:v1
curl http://127.0.0.1:8000/health

## CI/CD

El proyecto incluye un workflow de GitHub Actions en .github/workflows/ci.yml que ejecuta:

- Validacion de estilo con flake8.
- Pruebas automatizadas con pytest.

## Despliegue

La aplicacion esta preparada para ejecutarse en una instancia EC2 de AWS usando Gunicorn y el puerto 5000.

## Flujo DevOps

El proyecto utiliza ramas main, develop y ramas feature para organizar el trabajo. Los cambios se integran mediante Pull Requests y son validados automaticamente por GitHub Actions antes de ser fusionados.
