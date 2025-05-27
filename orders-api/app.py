from flask import Flask, jsonify, request
import redis
import requests
import mysql.connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/order')
def handle_order():
    order_id = request.args.get('id', type=int)

    # 🔍 Buscar pedido existente por ID
    if order_id:
        db = mysql.connector.connect(
            host="db",
            user="root",
            password="example",
            database="ecommerce"
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        db.close()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        return jsonify({
            "order_id": order["id"],
            "product_id": order["product_id"],
            "quantity": order["quantity"],
            "total_price": order["total_price"]
        })

    # 🛒 Criar novo pedido (como antes)
    product_id = request.args.get('product_id', default=1, type=int)
    quantity = request.args.get('quantity', default=2, type=int)

    cached = cache.get(f'product_{product_id}')
    if cached:
        product = eval(cached)
    else:
        r = requests.get('http://products:3001/products')
        products = r.json()['products']
        product = next((p for p in products if p['id'] == product_id), None)
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        cache.set(f'product_{product_id}', str(product))

    db = mysql.connector.connect(
        host="db",
        user="root",
        password="example",
        database="ecommerce"
    )
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity INT,
            total_price INT
        )
    """)
    cursor.execute(
        "INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s)",
        (product['id'], quantity, product['price'] * quantity)
    )
    db.commit()
    new_order_id = cursor.lastrowid
    cursor.close()
    db.close()

    return jsonify({
        "order_id": new_order_id,
        "product_id": product['id'],
        "quantity": quantity,
        "total_price": product['price'] * quantity
    })

@app.route('/test-redis')
def test_redis():
    cache.set("teste", "funcionando")
    value = cache.get("teste")
    return jsonify({"redis": value.decode()})


app.run(host='0.0.0.0', port=3002)
