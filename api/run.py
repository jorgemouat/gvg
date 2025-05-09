from fastapi import FastAPI
import requests
from datetime import datetime

app = FastAPI()

# CONFIGURA ESTOS DATOS:
API_KEY = 'f81e31ac31548c509513ff64bf8ac69e'
API_SECRET = '32dccd572071807ab324fb3824cb056a1253f87470eefa0e12'
STORE_NAME = 'granventagarage'

BASE_URL = "https://api.jumpseller.com/v1/products/"
AUTH_PARAMS = {
    'login': API_KEY,
    'authtoken': API_SECRET
}
GET_BASE_URL = 'https://api.jumpseller.com/v1/products/search.json?query=*&status=available'
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/XXX/YYY/ZZZ'  # reemplaza por tu webhook real

def get_all_products():
    available_products = []
    page = 1
    while True:
        params = {**AUTH_PARAMS, 'page': page, 'status': 'available', 'limit': 100}
        response = requests.get(GET_BASE_URL, params=params)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        for product in data:
            if product['product']['status'] == 'available':
                available_products.append(product)
        page += 1
    return available_products

def disable_products(products):
    logs = []
    for product in products:
        product_id = product['product']['id']
        product_name = product['product']['name']
        response = requests.get(f'{BASE_URL}/{product_id}.json', params=AUTH_PARAMS)
        if response.status_code == 200:
            json_product = response.json()
            if json_product['product']['status'] == 'disabled':
                continue
            disable_response = requests.put(
                f'{BASE_URL}/{product_id}.json',
                params=AUTH_PARAMS,
                json={'product': {'status': 'disabled'}}
            )
            if disable_response.status_code == 200:
                logs.append(f'✅ {product_name} desactivado')
            else:
                logs.append(f'❌ Error desactivando {product_name}')
        else:
            logs.append(f'❌ Error obteniendo ID {product_id}')
    return logs

def notify_slack():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = {
        "text": f"✅ GVG script ejecutado correctamente en {timestamp}"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    
    if response.status_code == 200:
        print("📩 Notificación enviada a Slack")
    else:
        print(f"❌ Error al enviar a Slack: {response.status_code} - {response.text}")


@app.get("/")
def run_script():
    products = get_all_products()
    # result = disable_products(products)
    notify_slack()
    return {"message": "Proceso completado", "resultados": len(products)}
