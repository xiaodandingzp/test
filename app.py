from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def index():
    return jsonify(True)

@app.route('/products')
def products():
    return jsonify([
        {"name": "商品一", "price": 10},
        {"name": "商品二", "price": 20}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
