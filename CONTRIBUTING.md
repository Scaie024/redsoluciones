# 🤝 Contribuir a Red Soluciones ISP

¡Gracias por tu interés en contribuir al proyecto! Este documento proporciona pautas para contribuir al sistema Red Soluciones ISP.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Guías de Estilo](#guías-de-estilo)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

## 🚀 ¿Cómo puedo contribuir?

### Reportar Bugs

Los bugs se rastrean como [GitHub issues](../../issues). Al crear un issue de bug, incluye:

- **Título claro y descriptivo**
- **Descripción exacta de los pasos** para reproducir el problema
- **Comportamiento esperado vs actual**
- **Capturas de pantalla** si es aplicable
- **Información del entorno** (OS, Python version, etc.)

### Sugerir Mejoras

Las mejoras también se rastrean como [GitHub issues](../../issues). Al crear un issue de mejora:

- **Describe la mejora** que te gustaría ver
- **Explica por qué sería útil** para la mayoría de usuarios
- **Proporciona ejemplos específicos** si es posible

## 🔧 Proceso de Desarrollo

1. **Fork** el repositorio
2. **Crea una rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Realiza tus cambios** siguiendo las guías de estilo
4. **Ejecuta las pruebas** (`python3 final_verification.py`)
5. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
6. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
7. **Crea un Pull Request**

### Configuración del Entorno de Desarrollo

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/red-soluciones-isp.git
cd red-soluciones-isp

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales (ver README.md)
# - service_account.json (Google Sheets)
# - Variables de entorno para Gemini AI

# 5. Ejecutar pruebas
python3 final_verification.py
```

## 📝 Guías de Estilo

### Python
- Seguir [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usar type hints cuando sea posible
- Documentar funciones y classes con docstrings
- Nombres de variables y funciones en español (consistente con el proyecto)

### Estructura de Archivos
```
backend/app/
├── main.py              # Aplicación principal FastAPI
├── core/                # Configuración y settings
├── services/            # Lógica de negocio
├── utils/               # Utilidades y helpers
└── __init__.py

frontend/
├── index.html           # Dashboard principal
├── assets/css/          # Estilos CSS
└── assets/js/           # JavaScript

tests/
└── test_suite.py        # Suite de pruebas automatizada
```

### Commits
- Usar el formato: `tipo(alcance): descripción`
- Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Ejemplos:
  - `feat(api): agregar endpoint para buscar clientes`
  - `fix(sheets): corregir error de conexión con Google Sheets`
  - `docs(readme): actualizar instrucciones de instalación`

### Pruebas
- Todas las nuevas funcionalidades deben incluir pruebas
- Ejecutar `python3 final_verification.py` antes de hacer commit
- Las pruebas deben pasar al 100%

## 🎯 Áreas de Contribución

### 🔧 Backend
- Nuevos endpoints de API
- Mejoras en la integración con Google Sheets
- Optimizaciones de rendimiento
- Manejo de errores mejorado

### 🎨 Frontend
- Mejoras en la UI/UX del dashboard
- Nuevas funcionalidades interactivas
- Optimizaciones para móviles
- Temas y personalización

### 🤖 Agente IA
- Mejoras en el procesamiento de lenguaje natural
- Nuevos tipos de consultas
- Optimización de respuestas
- Integración con otros modelos de IA

### 📱 Mensajería
- Mejoras en los bots de Telegram/WhatsApp
- Nuevas funcionalidades de notificación
- Integración con otros servicios de mensajería

### 🧪 Testing
- Nuevos casos de prueba
- Pruebas de integración
- Pruebas de rendimiento
- Automatización de testing

## ❓ ¿Tienes Preguntas?

Si tienes preguntas sobre cómo contribuir, puedes:

1. **Crear un issue** con la etiqueta `question`
2. **Revisar issues existentes** para ver si tu pregunta ya fue respondida
3. **Consultar la documentación** en el README.md

## 🙏 Reconocimientos

Todas las contribuciones, sin importar su tamaño, son valoradas y reconocidas. Los contribuidores serán listados en el README del proyecto.

¡Gracias por ayudar a hacer Red Soluciones ISP mejor para todos! 🚀
