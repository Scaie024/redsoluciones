# Red Soluciones ISP

Sistema integral de gestión ISP con inteligencia artificial integrada.

## 🚀 Despliegue en Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Scaie024/redsoluciones)

## ✨ Características

- **API REST** completa con FastAPI
- **Inteligencia Artificial** con Google Gemini
- **Bot de Telegram** integrado
- **Interfaz Web** responsive
- **Despliegue automático** en Vercel

## 🛠️ Tecnologías

- **Backend**: FastAPI + Python
- **Frontend**: HTML5 + CSS3 + JavaScript
- **IA**: Google Gemini AI
- **Mensajería**: Telegram Bot API
- **Deployment**: Vercel

## 📁 Estructura del Proyecto

```
redsoluciones/
├── api/
│   └── index.py          # Endpoint principal para Vercel
├── frontend/
│   ├── index.html        # Página principal
│   ├── admin.html        # Panel de administración
│   ├── dashboard.html    # Dashboard
│   └── assets/           # CSS y JavaScript
├── backend/
│   └── app/              # Aplicación FastAPI completa
├── requirements.txt      # Dependencias Python
├── vercel.json          # Configuración de Vercel
└── README.md            # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (Opcionales)

El sistema funciona automáticamente, pero puedes configurar:

```bash
GEMINI_API_KEY=tu_api_key_aqui
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

## 🌐 Endpoints API

- `GET /` - Información de la API
- `GET /health` - Estado del sistema
- `GET /api/status` - Estado de servicios
- `POST /api/contact` - Formulario de contacto

## 🚀 Despliegue Local

```bash
# Clonar repositorio
git clone https://github.com/Scaie024/redsoluciones.git
cd redsoluciones

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn backend.app.main:app --reload --port 8004
```

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico, contacta a través de los canales oficiales de Red Soluciones ISP.

---

Desarrollado con ❤️ para Red Soluciones ISP