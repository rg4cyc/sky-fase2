# Infraestructura - Sky Fase 2

## Descripcion general

La aplicacion Sky Fase 2 se despliega como una API REST en Python usando Flask. La solucion utiliza persistencia en archivo JSON y se prepara para ejecutarse en una instancia EC2 de AWS.

## Arquitectura

Cliente HTTP / navegador / curl
        |
        v
API Flask en EC2
        |
        v
GestorClientes
        |
        v
data/clientes.json

## Componentes

- Aplicacion Flask: atiende solicitudes HTTP.
- Archivo JSON: almacena clientes.
- GitHub: repositorio de codigo.
- GitHub Actions: integracion continua con pruebas y lint.
- Docker: empaquetado de la aplicacion.
- AWS EC2: servidor cloud para despliegue.
- Security Group: controla acceso a SSH y puerto de aplicacion.

## Configuracion AWS esperada

- Region: us-east-1
- Instancia: t2.micro
- Sistema operativo: Amazon Linux 2023
- Puerto SSH: 22, restringido a mi IP
- Puerto aplicacion: 5000, abierto temporalmente para demostracion
- Tags:
  - Project = SkyFase2
  - Environment = lab
  - Owner = rg4cyc

## Flujo de despliegue manual

1. Crear instancia EC2.
2. Configurar Security Group.
3. Conectarse por SSH.
4. Instalar Python, pip y git.
5. Clonar repositorio desde GitHub.
6. Instalar dependencias.
7. Ejecutar la aplicacion con Gunicorn.
8. Probar el endpoint /health desde navegador usando IP publica.

## Roles considerados

- Desarrolladores: implementan cambios de codigo y abren Pull Requests.
- Equipo TI: administra despliegue, EC2, Security Group y ejecucion de la aplicacion.
- Atencion al cliente: consulta la aplicacion para registrar o revisar clientes.

## Seguridad

- El acceso SSH debe limitarse a la IP del estudiante.
- El puerto 5000 se abre temporalmente solo para la demostracion.
- La instancia EC2 debe detenerse o terminarse al finalizar para evitar costos innecesarios.

## Nota de costos

Al finalizar la demostracion, la instancia EC2 debe detenerse o terminarse para evitar cargos innecesarios.
