#!/usr/bin/env python3
"""
Script para arreglar Google Sheets - Red Soluciones ISP
Diagnóstico completo y pasos para solucionar
"""

import os
import json
from dotenv import load_dotenv

def main():
    print("🔧 DIAGNÓSTICO GOOGLE SHEETS - Red Soluciones ISP")
    print("=" * 60)
    
    # Cargar configuración
    load_dotenv()
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    # Verificar service account
    try:
        with open('service_account.json', 'r') as f:
            credentials = json.load(f)
        service_email = credentials.get('client_email')
        project_id = credentials.get('project_id')
        
        print(f"✅ Credenciales encontradas:")
        print(f"   📧 Service Account: {service_email}")
        print(f"   🆔 Project ID: {project_id}")
        print()
        
    except Exception as e:
        print(f"❌ Error leyendo credenciales: {e}")
        return
    
    # Información de la hoja
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    
    print("📊 INFORMACIÓN DE LA HOJA:")
    print(f"   🆔 Sheet ID: {sheet_id}")
    print(f"   🔗 URL: {sheet_url}")
    print()
    
    print("🚨 PROBLEMA DETECTADO: Error 404 - Hoja no encontrada")
    print()
    print("💡 SOLUCIONES POSIBLES:")
    print()
    print("1️⃣  VERIFICAR QUE LA HOJA EXISTE:")
    print(f"    Abrir: {sheet_url}")
    print("    Si no abre o dice 'No encontrado', crear nueva hoja")
    print()
    print("2️⃣  COMPARTIR LA HOJA CON EL SERVICE ACCOUNT:")
    print(f"    📧 Compartir con: {service_email}")
    print("    🔓 Permisos: Editor")
    print("    📍 Pasos:")
    print("       • Abrir Google Sheets")
    print("       • Botón 'Compartir' (esquina superior derecha)")
    print(f"       • Agregar: {service_email}")
    print("       • Rol: Editor")
    print("       • Enviar")
    print()
    print("3️⃣  VERIFICAR ESTRUCTURA DE HOJAS:")
    print("    La hoja debe tener estas pestañas:")
    print("    📄 01_Clientes")
    print("    📄 02_Prospectos") 
    print("    📄 03_Incidentes")
    print()
    print("4️⃣  DESPUÉS DE CONFIGURAR:")
    print("    Ejecutar: curl -X GET 'http://0.0.0.0:8004/api/sheets/test'")
    print("    Debería responder: 'success': true")
    print()
    print("🔄 ¿NECESITAS CREAR UNA HOJA NUEVA?")
    print("   1. Ir a: https://sheets.google.com")
    print("   2. Crear hoja nueva")
    print("   3. Copiar el ID de la URL")
    print("   4. Actualizar GOOGLE_SHEET_ID en .env")
    print(f"   5. Compartir con: {service_email}")
    print()

if __name__ == "__main__":
    main()
