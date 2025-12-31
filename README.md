# 🔗 API REST de Consulta de Pacientes

API REST desarrollada con **Django** y **Django REST Framework** para la consulta segura de información de pacientes por número de DNI, orientada a la integración entre sistemas clínicos y administrativos.

El backend se encuentra desplegado en **Railway** y protegido mediante **autenticación por token**.

---

## 🎯 Problema que resuelve
En entornos de salud, múltiples sistemas requieren consultar información básica de pacientes de forma rápida y segura, evitando accesos directos a bases de datos o procesos manuales.

Esta API centraliza la consulta de pacientes por DNI, permitiendo la integración controlada entre sistemas internos, reduciendo errores y mejorando la interoperabilidad.

---

## 🔧 Funcionalidades principales
- Autenticación por token para control de acceso.
- Consulta de pacientes por DNI (`hi_ndocum`).
- Filtros de búsqueda mediante parámetros GET.
- Control de accesos no autorizados.
- Backend desplegado y accesible públicamente.
- Pensada para integración entre sistemas.

---

## 👨‍💻 Mi rol en el proyecto
- Diseño de la arquitectura de la API.
- Desarrollo completo del backend con Django REST Framework.
- Implementación de autenticación por token.
- Definición de endpoints y validaciones.
- Despliegue del servicio en Railway.
- Enfoque en seguridad y reutilización por terceros.

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
📧 sperezn.dev@gmail.com

---

> _Este proyecto fue desarrollado con fines de integración entre sistemas médicos y API REST para consulta de pacientes._
