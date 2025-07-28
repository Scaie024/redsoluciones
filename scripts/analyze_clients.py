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
            first_client = clients[0]
            print('\nPrimer cliente:')
            for key, value in first_client.items():
                print(f'  {key}: {value} (tipo: {type(value)})')
            
            # Analizar campos activos
            active_clients = [c for c in clients if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí', 'yes', '1', 'true']]
            print(f'\nClientes activos: {len(active_clients)}')
            
            # Analizar pagos
            payments = []
            for c in clients:
                pago = c.get('Pago', '0')
                if pago and str(pago) != '0':
                    try:
                        payments.append(float(str(pago).replace(',', '')))
                    except:
                        pass
            
            print(f'Clientes con pago: {len(payments)}')
            if payments:
                print(f'Pago promedio: ${sum(payments)/len(payments):.2f}')
    else:
        print('Error:', data)
        
except Exception as e:
    print(f'Error: {e}')
