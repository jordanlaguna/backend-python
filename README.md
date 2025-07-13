# 🐍 FastAPI Backend - Sistema de Ventas, Usuarios, Personas, Inventario y Facturación

Este proyecto es un backend desarrollado con **FastAPI** y **MySQL**, diseñado para manejar:

- Registro de personas y usuarios
- Autenticación segura con JWT
- Gestión de productos e inventario
- Registro de ventas y facturas
- Integración con frontend de escritorio (Windows Forms)

---

## 🚀 Tecnologías

- Python 3.11+
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Passlib (bcrypt)
- python-dotenv
- Uvicorn
- python-jose (para JWT)

---

## 📦 Instalación y Configuración

### 1. Clona el repositorio

```bash
git clone https://github.com/jordanlaguna/backend-python.git
cd tu-backend
```

### 2. Crea un entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate        # Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura el archivo `.env`

```env
DB_HOST=localhost
DB_USER=miusuario
DB_PASS=miclave
DB_PORT=3306
DB_NAME=posdb
PORT=8000
```

> ✅ Asegurate de agregar el archivo `.env` al `.gitignore`.

---

## ⚙️ Ejecución del Servidor

```bash
uvicorn app.main:app --reload
```

---

## 📂 Estructura del Proyecto

```
.
├── app/
│   ├── database/
│   │   └── database.py              # Conexión SQLAlchemy
│   ├── models/
|   |   |-- model_categories.py
|   |   |-- model_client.py
│   │   ├── model_person.py
│   │   ├── model_product.py
│   │   ├── model_sale_details.py
│   │   ├── model_sale.py
│   │   ├── model_user.py
│   ├── router/
│   │   ├── categories_routes.py
│   │   ├── client_routes.py
│   │   ├── person_routes.py
│   │   ├── product_routes.py
│   │   ├── sale_routes.py
│   │   └── user_routes.py
│   ├── schemas/
│   │   ├── schemas_categories.py
│   │   ├── schemas_clients.py
│   │   ├── schemas_person.py
│   │   ├── schemas_product.py
│   │   ├── schemas_sale_details.py
│   │   ├── schemas_sales.py
│   │   └── schemas_user.py
│   ├── services/
│   │   ├── crud_categories.py
│   │   ├── crud_client.py
│   │   ├── crud_product.py
│   │   ├── crud_person.py
│   │   ├── crud_sale.py
│   │   └── crud_user.py
│   └── utils/
│       ├── security.py              # Hash de contraseñas
│       └── jwt_handler.py           # JWT token utils
├── .env
├── .gitignore
└── main.py
```

---

## 🔑 Autenticación JWT

El login retorna un token JWT firmado con tu clave secreta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer",
  "user_id": 1
}
```

Ese token se debe usar en encabezados `Authorization` en rutas protegidas:

```
Authorization: Bearer <access_token>
```

---

## ✅ Funcionalidades disponibles

### Usuarios

- POST `/users/` – Crear usuario
- POST `/users/login` – Login con JWT
- GET `/users/{id}` – Consultar usuario

### Personas

- CRUD completo de personas (`/persons/`)
- POST `/persons/register`
- GET `/persons/person_list`

### Productos

- POST `/products/` – Crear productos
- GET `/products/` – Listar productos
- GET `/products/product/{barcode}` – Buscar por código de barras

### Ventas

- POST `/sales/add_sale` – Registrar venta
- Incluye detalles (productos vendidos, cantidades, subtotales, impuestos, etc.)

### Categories

- GET `/categories/categories_list` – Listar categorias

---

## 🖥️ Integración con Frontend

Este backend está integrado con una **aplicación de escritorio C# (Windows Forms)** que:

- Consulta productos por código de barras
- Añade productos a la venta
- Calcula totales con IVA
- Realiza POST a `/sales/add_sale` con los datos de facturación

Además, el frontend guarda el token JWT en memoria y lo utiliza para acceder a rutas protegidas.

---

## 🛡️ Seguridad

- 🔐 Contraseñas encriptadas con bcrypt (`passlib`)
- 🔑 Autenticación con JWT (`HS256`)
- 🧪 Tokens con expiración (1 hora por defecto)
- 🔒 Preparado para proteger rutas mediante dependencias `Depends(get_current_user)`

---

## 🛠️ Próximas mejoras

- Protección de rutas con verificación de token
- CRUD completo para categorías
- Registro de clientes y cuentas por cobrar
- Reportes de facturación

---

## 📫 Contacto

Si tenés dudas o sugerencias, escribime a [jordanlaguna10@gmail.com](mailto:jordanlaguna10@gmail.com) o abrí un Issue.

---

¡Listo para facturar! 💸🧾
