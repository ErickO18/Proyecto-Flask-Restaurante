from flask import Blueprint, render_template , request, redirect, url_for,session, flash
import  sqlite3
from utils import get_connection, login_required, admin_required, roles_required,mesero_required

paginas_bp = Blueprint('paginas', __name__)

@paginas_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)", (username, password,rol))
            conn.commit()
            flash(' Cuenta creada con éxito. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('paginas.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya existe.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

##login
@paginas_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_login']
        password = request.form['contraseña_login']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['rol'] = user[3]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('paginas.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')


@paginas_bp.route('/logout')
def logout():
    session.clear()  # elimina toda la información de sesión
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('paginas.login'))



@paginas_bp.route('/')
@login_required
def index ():
    return render_template('inicio.html')

@paginas_bp.route('/platos')
@login_required
def platos():
    conn = get_connection()
    platos = conn.execute("SELECT * FROM plato").fetchall()
    conn.close()
    return render_template('platos.html',platos = platos)

@paginas_bp.route('/proveedores')
@login_required
def proveedores():
    conn = get_connection()
    qproveedores = """
        SELECT p.nombre_proveedor, p.producto, pl.nombre_plato 
        FROM proveedor p
        INNER JOIN plato pl ON p.id_plato = pl.id_plato
    """
    prov = conn.execute(qproveedores).fetchall()
    
    platos = conn.execute("SELECT * FROM plato").fetchall()
    
    conn.close() 
    return render_template('proveedor.html', proveedores=prov, platos=platos)

@paginas_bp.route('/registro_proveedor',methods=['POST'])
@login_required
@admin_required
def registro_proveedor():
    nombre_prov = request.form['nombre_proveedor']
    prod = request.form['producto']
    plat = request.form['plato_selected']
    conn = get_connection()
    resultado = conn.execute("SELECT id_plato FROM plato WHERE nombre_plato = ?",(plat,)).fetchone()
    
    id_plat = resultado['id_plato']
    
    conn.execute("INSERT INTO proveedor (nombre_proveedor,producto,id_plato) VALUES(?,?,?)",(nombre_prov,prod,id_plat))
    conn.commit()
    conn.close()
    return redirect('/proveedores')
    
@paginas_bp.route('/pedido')
@login_required
@roles_required(['mesero', 'cocinero', 'admin'])
def pedido():
    conn = get_connection()

    lista_platos = conn.execute("SELECT * FROM plato").fetchall()
    query = """
        SELECT 
            p.cantidad,
            c.nombre_cliente,
            pl.nombre_plato
        FROM pedido p
        JOIN cliente c ON p.id_cliente = c.id_cliente
        JOIN plato pl ON p.id_plato = pl.id_plato
    """
    pedidos_con_datos = conn.execute(query).fetchall()

    conn.close()
    
    return render_template('pedido.html', platos=lista_platos, pedidos=pedidos_con_datos)


@paginas_bp.route('/pidiendo', methods=['POST'])
@login_required
@mesero_required
def pidiendo():
    conn = get_connection()

    nombre_us = request.form['nombre']
    telefo_us = request.form['telefono']
    plato = request.form['plato_selected']
    cantidad = request.form['cantidad']

    conn.execute("INSERT INTO cliente (nombre_cliente, telefono_cliente) VALUES (?,?)",(nombre_us, telefo_us))
    conn.commit()

    resultado = conn.execute("SELECT id_cliente FROM cliente WHERE telefono_cliente = ?", (telefo_us,)).fetchone()

    id_us = resultado['id_cliente']

    conn.execute("INSERT INTO pedido (id_cliente, id_plato, cantidad) VALUES (?, ?, ?)", (id_us, plato, cantidad))
    conn.commit()
    
    conn.close()

    return redirect('/pedido')