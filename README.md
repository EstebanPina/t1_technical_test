# Sistema de Gestión de Tarjetas

API REST para la gestión de tarjetas de crédito/débito con validación Luhn y generación de números de tarjeta.

## 🚀 Características Principales

- Validación de números de tarjeta usando el algoritmo de Luhn
- Generación de números de tarjeta válidos a partir de un BIN
- Almacenamiento seguro de información de tarjetas
- API RESTful con documentación interactiva
- Autenticación y autorización
- Contenedorización con Docker

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.11
- **Framework**: FastAPI
- **Base de datos**: MongoDB
- **ODM**: Beanie (MongoDB ODM)
- **Validación de datos**: Pydantic v2
- **Contenedores**: Docker y Docker Compose
- **Documentación**: OpenAPI (Swagger UI y ReDoc)
- **Pruebas**: Pytest con asyncio

## 🚀 Configuración del Entorno

### Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.11+ (solo para desarrollo local sin Docker)

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB_NAME=fastapi_db
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐳 Ejecución con Docker (Recomendado)

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd t1_technical_test
   ```

2. Inicia los servicios con Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. La aplicación estará disponible en:
   - API: http://localhost:8000
   - Documentación Swagger UI: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc
   - MongoDB Express: http://localhost:8081

## 🛠️ Desarrollo Local (Sin Docker)

1. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📚 Documentación de la API

La documentación interactiva está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints Principales

#### Tarjetas
- `POST /api/v1/tarjetas/` - Crear una nueva tarjeta
- `GET /api/v1/tarjetas/` - Listar todas las tarjetas
- `GET /api/v1/tarjetas/{tarjeta_id}` - Obtener detalles de una tarjeta
- `POST /api/v1/tarjetas/generate` - Generar números de tarjeta válidos

#### Clientes
- `POST /api/v1/clientes/` - Crear un nuevo cliente
- `GET /api/v1/clientes/` - Listar todos los clientes
- `GET /api/v1/clientes/{cliente_id}` - Obtener detalles de un cliente

## 🧪 Ejecución de Pruebas

Para ejecutar las pruebas unitarias:

```bash
# Con Docker (recomendado)
docker-compose exec web pytest tests/ -v

# O localmente (con el entorno virtual activado)
pytest tests/ -v
```

## 📁 Estructura del Proyecto

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── clientes.py
│   │       │   └── tarjetas.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   ├── crud_cliente.py
│   │   └── crud_tarjeta.py
│   ├── db/
│   │   └── mongodb.py
│   ├── models/
│   │   ├── cliente.py
│   │   └── tarjeta.py
│   ├── schemas/
│   │   ├── cliente.py
│   │   ├── tarjeta.py
│   │   └── base.py
│   ├── utils/
│   │   └── card_utils.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_card_utils.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
# TARJETAS DE PRUEBA
4505899976198082
5177125383167484
5180043159066456