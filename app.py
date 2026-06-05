from flask import Flask
from paginas.rutas import paginas_bp
from utils import init_db, plato_db, pedido_db, proveedores_db, users_db

app = Flask(__name__)
app.secret_key = 'ericksdelicious12345678910'

app.register_blueprint(paginas_bp)

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == '__main__':
    init_db()
    plato_db()
    pedido_db()
    proveedores_db()
    users_db()
    app.run(debug=True)