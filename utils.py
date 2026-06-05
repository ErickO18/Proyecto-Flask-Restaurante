import sqlite3
from functools import wraps
from flask import session, flash, redirect, url_for

def get_connection():
    conn = sqlite3.connect("database_restaurant.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS cliente(
        id_cliente INTEGER,
	    nombre_cliente TEXT NOT NULL,
	    telefono_cliente INTEGER,
	    PRIMARY KEY("id_cliente" AUTOINCREMENT)
        )''')
    conn.close()

def plato_db():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS plato(
        id_plato INTEGER,
	    nombre_plato TEXT NOT NULL,
	    precio_plato INTEGER NOT NULL,
        img TEXT,
	    PRIMARY KEY(id_plato AUTOINCREMENT)
        )''')
    conn.close()

def pedido_db():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS pedido(
        id_pedido INTEGER,
        id_cliente INTEGER,
        id_plato INTEGER,
        cantidad INTEGER NOT NULL,
        PRIMARY KEY(id_pedido AUTOINCREMENT),
        FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente),
        FOREIGN KEY(id_plato) REFERENCES plato(id_plato)
        )''')
    conn.close()
    
def proveedores_db():
    conn = get_connection()
    conn.execute(''' CREATE TABLE IF NOT EXISTS proveedor(
                 id_proveedor INTEGER,
                 nombre_proveedor TEXT NOT NULL,
                 producto TEXT NOT NULL,
                 id_plato INTEGER,
                 PRIMARY KEY(id_proveedor AUTOINCREMENT),
                 FOREIGN KEY(id_plato) REFERENCES plato(id_plato)
                 )''')
    conn.close()
    
def users_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'mesero'
        )
    ''')
    cursor = conn.execute("SELECT * FROM usuarios WHERE username=?",('admin',))
    if cursor.fetchone() is None:
        conn.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)", ('admin', '1234', 'admin'))
    conn.commit()
    conn.close()



##sesion
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('paginas.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rol' not in session or session['rol'] != 'admin':
            flash('No tienes permisos para acceder a esta función.', 'danger')
            return redirect(url_for('paginas.index'))
        return f(*args, **kwargs)
    return decorated_function

def mesero_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rol' not in session or session['rol'] not in ['mesero', 'admin']:
            flash('No tienes permisos para acceder a esta función.', 'danger')
            return redirect(url_for('paginas.index'))
        return f(*args, **kwargs)
    return decorated_function

def cocinero_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rol' not in session or session['rol'] not in ['cocinero', 'admin']:
            flash('No tienes permisos para acceder a esta función.', 'danger')
            return redirect(url_for('paginas.index'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if 'rol' not in session or session['rol'] not in roles:
                flash('No tienes permisos para acceder a esta función.', 'danger')
                return redirect(url_for('paginas.index'))

            return f(*args, **kwargs)

        return decorated_function
    return decorator