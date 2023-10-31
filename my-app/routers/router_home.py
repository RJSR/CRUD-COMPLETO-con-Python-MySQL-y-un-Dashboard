from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/productos"


@app.route('/registrar-producto', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-producto', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
            resultado = procesar_form_producto(request.form)
            if resultado:
                return redirect(url_for('lista_productos'))
            else:
                flash('El producto NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-productos', methods=['GET'])
def lista_productos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_productos.html', productos=sql_lista_productosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-producto/", methods=['GET'])
@app.route("/detalles-producto/<int:idProducto>", methods=['GET'])
def detalleProducto(idProducto=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idProducto es None o no está presente en la URL
        if idProducto is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_productosBD(idProducto) or []
            return render_template(f'{PATH_URL}/detalles_producto.html', detalle_empleado = detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de empleados
@app.route("/buscando-producto", methods=['POST'])
def viewBuscarProductoBD():
    resultadoBusqueda = buscarproductoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_producto.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-producto/<int:id>", methods=['GET'])
def viewEditarProducto(id):
    if 'conectado' in session:
        respuestaProducto = buscarproductoUnico(id)
        if respuestaProducto:
            return render_template(f'{PATH_URL}/form_producto_update.html', respuestaProducto=respuestaProducto)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de producto
@app.route('/actualizar-producto', methods=['POST'])
def actualizarProducto():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_productos'))
    
@app.route('/actualizar-precio', methods=['GET','POST'])
def actualizarPrecio():
    resultData = procesar_actualizacion_form_precio(request)
    if resultData:
        return redirect(url_for('lista_productos'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-producto/<string:id_producto>', methods=['GET'])
def borrarProducto(id_producto):
    resp = eliminarproducto(id_producto)
    if resp:
        flash('El Producto fue eliminado correctamente', 'success')
        return redirect(url_for('lista_productos'))


@app.route("/descargar-informe-productos/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
