# 🐍 FastAPI Backend - Sistema de Usuarios, Personas Ventas, Inventario y Facturación

Este proyecto es un backend desarrollado con **FastAPI** y **MySQL**, que permite registrar personas junto con usuarios, realizar autenticación y consultar la información almacenada, por el momento he hecho esas funciones, pero sigo desarrollándolo en un sistema.

## 🚀 Tecnologías

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn
- python-dotenv

---

## 📦 Instalación y Configuración

### 1. Clona el repositorio
```bash
git clone https://github.com/tuusuario/tu-backend.git
cd tu-backend
```

### 2. Crea un entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate     # En Linux/macOS
.venv\Scripts\activate        # En Windows
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Crea un archivo `.env`
```env
DB_HOST=localhost
DB_USER=miusuario
DB_PASS=
DB_PORT=mipuerto
DB_NAME=midatabase
PORT=8000
```

> ✅ Asegúrate de agregar el archivo `.env` a tu `.gitignore` para proteger tus credenciales.

### 5. Ejecuta con el siguiente comando al activar el entorno
```bash
uvicorn app.main:app --reload
```

---

## 📂 Estructura del Proyecto

```
.
├── app/
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   ├── model_person.py
│   │   └── model_user.py
│   ├── schemas/
│   │   ├── schemas_person.py
│   │   └── schemas_user.py
│   ├── services/
│   │   ├── crud_person.py
│   │   └── crud_user.py
│   ├── router/
│   │   ├── person_routes.py
│   │   └── user_routes.py
│   └── utils/
│       └── security.py
│
├── .env
├── .gitignore
├── main.py (o app/main.py)
├── requirements.txt
└── README.md
```

---

## 🛡️ Seguridad

- 🔐 Las contraseñas se almacenan de forma segura con hash (`bcrypt`).
- 📄 Las rutas privadas pueden protegerse fácilmente con JWT y middlewares (próximo paso sugerido).

---

## 📫 Contacto

Si tenés dudas o sugerencias, podés contactarme en [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com) o abrir un Issue en el repositorio.

---

¡Listo para usar! 🚀
