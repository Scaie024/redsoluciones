#!/usr/bin/env python3
import json
import sys
import requests

try:
    response = requests.get('http://localhost:8004/api/clients')
    data = response.json()
    
    if data.get('success'):
        clients = data.get('data', [])
        print(f'Total clientes encontrados: {len(clients)}')
        if clients:
            # Obtener todas las claves únicas
            all_keys = set()
            for client in clients:
                all_keys.update(client.keys())
            
            print('\nTodos los campos disponibles:')
            for key in sorted(all_keys):
                print(f'  - {key}')
            
            # Buscar campos que puedan contener información de pago
            payment_fields = [key for key in all_keys if 'pago' in key.lower() or 'price' in key.lower() or 'cost' in key.lower() or 'payment' in key.lower()]
            print(f'\nCampos relacionados con pago: {payment_fields}')
            
            # Mostrar ejemplos de datos de algunos clientes
            print('\nEjemplos de datos de clientes (primeros 3):')
            for i, client in enumerate(clients[:3]):
                print(f'\nCliente {i+1}:')
                for key, value in client.items():
                    if 'pago' in key.lower() or 'activo' in key.lower():
                        print(f'  {key}: {value}')
                        
    else:
        print('Error:', data)
        
except Exception as e:
    print(f'Error: {e}')
