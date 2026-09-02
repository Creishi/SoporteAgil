# SoporteAgil

Sistema de gestión y soporte ágil diseñado para optimizar la atención, seguimiento y administración de requerimientos. El proyecto está estructurado con una API en PHP y desplegado completamente mediante contenedores Docker.

---

## 📐 Arquitectura del Proyecto

El repositorio está organizado con la siguiente estructura de archivos y directorios principales:

```text
SoporteAgil/
├── Soporte-agil-api/    # Código fuente de la API Backend
│   └── src/             # Lógica de la aplicación
│       └── index.php    # Punto de entrada principal de la API
├── Dockerfile           # Configuración de la imagen Docker para el entorno PHP/Servidor
├── docker-compose.yml   # Definición y orquestación de servicios (API + Base de Datos)
├── init.sql             # Script de inicialización de esquemas y tablas de la base de datos
└── README.md            # Documentación del repositorio
📋 Requisitos Previos
Antes de comenzar, asegúrate de tener instalados los siguientes componentes en tu entorno local:

Docker Desktop (v20.10 o superior)

Docker Compose (v2.0 o superior)

Git para el control de versiones

⚙️ Variables de Entorno
Crea un archivo .env en la raíz del proyecto tomando como base la siguiente configuración para la conexión:

Fragmento de código
# Configuración de la Base de Datos
DB_HOST=db
DB_PORT=3306
DB_NAME=soporte_agil_db
DB_USER=soporte_user
DB_PASSWORD=soporte_password

# Configuración de la API
API_PORT=8000
APP_ENV=local
🚀 Guía de Instalación con Docker Compose
Sigue estos pasos para levantar todo el entorno de desarrollo de manera automatizada:

1. Clonar el repositorio
Bash
git clone [https://github.com/Creishi/SoporteAgil.git](https://github.com/Creishi/SoporteAgil.git)
cd SoporteAgil
2. Construir y levantar los contenedores
Ejecuta el comando de Docker Compose para compilar la imagen del servidor PHP y desplegar la base de datos ejecutando el script init.sql:

Bash
docker-compose up -d --build
3. Verificar el estado de los servicios
Asegúrate de que todos los contenedores estén corriendo correctamente:

Bash
docker-compose ps
4. Acceder a la aplicación
API Backend: http://localhost:8000 (o el puerto expuesto en tu docker-compose.yml)

🛠️ Comandos Útiles
Ver logs en tiempo real:

Bash
docker-compose logs -f
Detener los servicios:

Bash
docker-compose down
Detener y reiniciar desde cero (borrando volúmenes):

Bash
docker-compose down -v
docker-compose up -d --build
