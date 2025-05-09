from flask import Flask
import requests

app = Flask(__name__)

# CONFIGURA ESTOS DATOS:
API_KEY = 'f81e31ac31548c509513ff64bf8ac69e'  # LOGIN
API_SECRET = '32dccd572071807ab324fb3824cb056a1253f87470eefa0e12'  # AUTH
STORE_NAME = 'granventagarage'  # sin ".jumpseller.com"

BASE_URL = "https://api.jumpseller.com/v1/products/"
AUTH_PARAMS = {
    'login': API_KEY,
    'authtoken': API_SECRET
}

GET_BASE_URL = 'https://api.jumpseller.com/v1/products/search.json?query=*&status=available'

# Paso 1: Obtener todos los productos
def get_all_products():
    products = []
    available_products = []
    page = 1

    while True:
        params = {
            **AUTH_PARAMS,
            'page': page,
            'status': 'available',
            'limit': 100,
        }
        response = requests.get(GET_BASE_URL, params=params)
        if response.status_code != 200:
            raise Exception(f'Error en la solicitud: {response.status_code}')
        
        data = response.json()
        
        if not data:
            break
        
        for product in data:
            if product['product']['status'] == 'available':
                available_products.append(product)
        page += 1

    return available_products

# Paso 2: Desactivar productos uno a uno
def disable_products(products):
    for product in products:
        product_id = product['product']['id']
        product_response = requests.get(f'{BASE_URL}/{product_id}.json', params=AUTH_PARAMS)
        
        if product_response.status_code == 200:
            json_product = product_response.json()
            status = json_product['product']['status']
            
            if status == 'disabled':
                continue
            
            response = requests.put(
                f'{BASE_URL}/{product_id}.json',
                params=AUTH_PARAMS,
                json={'product': {'status': 'disabled'}}
            )
            if response.status_code == 200:
                print(f'Producto ID {product_id} desactivado.')
            else:
                print(f'Error al desactivar ID {product_id}')
        else:
            print(f'Error al obtener el producto ID {product_id}')

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        print('🔄 Obteniendo productos...')
        products = get_all_products()
        print(f'📦 Total productos encontrados: {len(products)}')

        print('🔻 Desactivando productos...')
        # disable_products(products)
        return '🚫 Todos los productos han sido marcados como no publicados.'
    except Exception as e:
        return f'Error al ejecutar el script: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
