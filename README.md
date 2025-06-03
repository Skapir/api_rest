# API REST de Consulta de Pacientes - Skapir

Este proyecto es una API REST desarrollada con Django y Django REST Framework para permitir la **consulta de información de pacientes** por número de DNI. El backend se encuentra desplegado en Railway y está protegido mediante **autenticación por token**.

---

## 🔧 Funcionalidades principales

- Autenticación por token para controlar el acceso a la API.
- Endpoint para buscar pacientes por DNI (`hi_ndocum`).
- Panel para visualizar tokens activos y controlar la cantidad de consultas realizadas por token.
- Protección contra consultas no autorizadas.

---

## 🚀 Despliegue

Este proyecto está desplegado en:  
🔗 `https://api-rest-skapir-production.up.railway.app/`

---

## 📦 Instalación local

```bash
git clone https://github.com/Skapir/api_rest.git
cd api_rest
python -m venv venv
source venv/bin/activate    # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🔐 Autenticación

Todas las solicitudes requieren autenticación por **token**.

### Formato del header:

```http
Authorization: Token tu_token_aquí
```

### Ejemplo con `curl`:

```bash
curl -H "Authorization: Token tu_token_aquí" https://api-rest-skapir-production.up.railway.app/api/pacientes/?search=12345678
```

---

## 📡 Endpoints

### 🔍 Buscar paciente por DNI

```
GET /api/pacientes/?search=<DNI>
```

**Respuesta exitosa:**

```json
[
  {
    "hi_nreg": "123456",
    "hi_ndocum": "12345678",
    "hi_nombre": "JUAN PEREZ LOPEZ",
    "hi_fecnac": "1985-05-10",
    "hi_sexo": "M"
  }
]
```

**Respuesta cuando el DNI no existe:**

```json
[]
```

---

## 🧩 Estructura del Proyecto

- `core/`: Configuración general del proyecto Django.
- `web/`: Aplicación principal de la API, contiene modelos, vistas y autenticación.
- `requirements.txt`: Librerías necesarias.
- `.gitignore`: Archivos excluidos del control de versiones.

---

## ✉️ Contacto

Desarrollado por **Skapir (Sergio P.)**  
📧 skapir.dev@gmail.com

---

> _Este proyecto fue desarrollado con fines de integración entre sistemas médicos y API REST para consulta de pacientes._
