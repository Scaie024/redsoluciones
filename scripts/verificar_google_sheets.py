#!/usr/bin/env python3
"""
Script para verificar configuración de Google Sheets
Red Soluciones ISP
"""

import os
import json
from pathlib import Path

def verificar_configuracion():
    """Verificar toda la configuración de Google Sheets"""
    print("🔍 VERIFICANDO CONFIGURACIÓN DE GOOGLE SHEETS")
    print("=" * 50)
    
    # 1. Verificar archivo de credenciales
    service_account_path = Path("service_account.json")
    if service_account_path.exists():
        print("✅ service_account.json encontrado")
        try:
            with open(service_account_path, 'r') as f:
                creds = json.load(f)
                print(f"   📧 Email: {creds.get('client_email', 'NO ENCONTRADO')}")
                print(f"   🆔 Project ID: {creds.get('project_id', 'NO ENCONTRADO')}")
        except Exception as e:
            print(f"❌ Error leyendo credenciales: {e}")
    else:
        print("❌ service_account.json NO ENCONTRADO")
        print("   📥 Necesitas descargar este archivo desde Google Cloud Console")
        print("   🔗 https://console.cloud.google.com/")
    
    print()
    
    # 2. Verificar .env
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env encontrado")
        with open(env_path, 'r') as f:
            content = f.read()
            if "GOOGLE_SHEET_ID" in content:
                # Extraer el ID
                for line in content.split('\n'):
                    if line.startswith('GOOGLE_SHEET_ID='):
                        sheet_id = line.split('=')[1]
                        print(f"   📊 Sheet ID: {sheet_id}")
                        print(f"   🔗 URL: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
            else:
                print("❌ GOOGLE_SHEET_ID no encontrado en .env")
    else:
        print("❌ .env NO ENCONTRADO")
    
    print()
    
    # 3. Verificar estructura necesaria
    print("📋 ESTRUCTURA NECESARIA DE GOOGLE SHEETS:")
    print("   📄 Hoja '01_Clientes' con columnas:")
    print("      - Nombre, Email, Telefono, Zona, Pago_Mensual, Estado")
    print("   📄 Hoja '02_Prospectos' con columnas:")
    print("      - Nombre, Telefono, Zona, Email, Prioridad, Estado")
    print("   📄 Hoja '03_Incidentes' con columnas:")
    print("      - Cliente, Descripcion, Tipo, Prioridad, Estado, Fecha")
    
    print()
    print("🔧 PASOS PARA ARREGLAR:")
    if not service_account_path.exists():
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto o selecciona uno existente")
        print("3. Habilita Google Sheets API")
        print("4. Crea una cuenta de servicio")
        print("5. Descarga el JSON y guárdalo como 'service_account.json'")
        print("6. Comparte tu Google Sheet con el email de la cuenta de servicio")

if __name__ == "__main__":
    verificar_configuracion()
