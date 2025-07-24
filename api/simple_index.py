"""
Versión Simplificada para Vercel - Solo API básica
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import json

app = FastAPI(
    title="Red Soluciones ISP - API Simplificada",
    description="API básica para Vercel deployment",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Red Soluciones ISP API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-07-24",
        "environment": "production"
    }

@app.get("/api/status")
async def api_status():
    return {
        "api": "operational",
        "services": {
            "web": "active",
            "database": "connected"
        }
    }

# Endpoint básico para pruebas
@app.post("/api/contact")
async def contact_form(data: dict):
    return {
        "message": "Formulario recibido",
        "data": data,
        "status": "processed"
    }

# Vercel handler
def handler(request, response):
    return app
