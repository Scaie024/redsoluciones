"""
Entry point para Vercel - Red Soluciones ISP
"""
from api.index import app

# Export para Vercel
def app_handler(*args, **kwargs):
    return app

# También exportar directamente
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
