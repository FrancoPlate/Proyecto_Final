"""
--------------------------------------
    Trabajo Final 
--------------------------------------
"""

import sqlite3


ruta_db = r"E:/Proyectos/Cursada/clases/Trabajo_Final/inventario.db"


# cada vez que se ejecute el programa se crea la base de datos
def crear_db():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()  # siempre igual
    """
        Si bien la consigna pide una "'id': Identificador único del producto (clave primaria, autoincremental)."
        En este caso, se utiliza el id del producto como clave primaria, pero no el autoincremental, ya que considero que los productos se 
        registraran con el codigo que tienen ("Código": 15, "Nombre": Toronja, "Precio": 15, etc) y me base en base a eso.
    """
    cursor.execute(  # ejecuta la consulta
        """
                CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
                )
        """
    )
    conexion.commit()
    conexion.close()


# funciona para saber si el producto ya existe o no
def existe_prod(cod):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT id FROM productos WHERE id = ?"  # hago una consulta para saber si el valor ya existe
    cursor.execute(query, (cod,))
    if cursor.fetchone():
        conexion.commit()
        conexion.close()
        return True

    else:
        conexion.commit()
        conexion.close()
        return False


# Tomar los datos de un producto
def reg_productos():

    nombre = input("Ingrese Nombre del producto: ")
    descripcion = input("Ingrese Descripcion del producto: ")
    precio = float(input("Ingrese Precio del producto: "))
    cantidad = int(input("Ingrese Cantidad del producto: "))
    categoria = input("Ingrese Categoria del producto: ")

    producto = {
        "Nombre": nombre,
        "Descripción": descripcion,
        "Cantidad": cantidad,
        "Precio": precio,
        "Categoria": categoria,
    }
    # print(producto)
    registrar_productos(producto)


# Registrar producot en la base de datos
def registrar_productos(producto):
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "INSERT INTO productos (nombre, categoria, descripcion, cantidad, precio) VALUES (?,?,?,?,?)"  # consulta
    plaseholder = (
        producto["Nombre"],
        producto["Categoria"],
        producto["Descripción"],
        producto["Cantidad"],
        producto["Precio"],
    )  # el valor de cada consulta
    cursor.execute(
        query, plaseholder
    )  # envio de la consulta. El plaseholder debe pasarse como una tupla o lista para que no de error
    conexion.commit()
    conexion.close()
    print("Producto registrado con exito!!")


# Mostrar todos los productos
def mostrar_productos():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")  # seleccionar todo de la tabla productos
    resultados = cursor.fetchall()  # pasa los resultados a la variable "resultados"
    for producto in resultados:
        print("Productos:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Categoria: {producto[2]}")
        print(f"Descripción: {producto[3]}")
        print(f"Cantidad: {producto[4]}")
        print(f"Precio: {producto[5]}")
        print("-" * 20)

    conexion.close()


# actualizar un producto
def actualizar_productos():

    # mensaje de lo que quiere actualizar del producto
    codigo = input("Codigo del producto: ")

    if existe_prod(codigo):

        print("-" * 20)
        print("1. Actualizar Descripción")
        print("2. Actualizar Cantidad")
        print("3. Actualizar Precio")
        print("4. Salir")
        print("-" * 20)

        opc = int(input("Seleccione la opcion que quiera cambiar: "))
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        # Opciones de las distintas actualizaciones
        if opc == 1:
            while True:
                plaseholder = input("Ingrese la nueva Descripción: ")
                if not plaseholder:
                    print("No se peude ingresar un valor nulo!!")
                else:
                    query = "UPDATE productos SET descripción = ? WHERE id = ?"
                    cursor.execute(query, plaseholder)
                    print("Dato guardado!\n")
                break

        elif opc == 2:
            while True:
                plaseholder = int(input("Ingrese la nueva Cantidad: "))
                if not plaseholder:
                    print("No se peude ingresar un valor nulo!!")
                elif plaseholder < 0:
                    print("No se puede ingresar un valor negativo!!")
                else:
                    query = "UPDATE productos SET cantidad = ? WHERE id = ?"
                    cursor.execute(query, plaseholder)
                    print("Dato guardado!\n")
                break
        elif opc == 3:
            while True:
                plaseholder = float(input("Ingrese la nueva Precio: "))
                if not plaseholder:
                    print("No se peude ingresar un valor nulo!!")
                elif plaseholder < 0:
                    print("No se puede ingresar un valor negativo!!")
                else:
                    query = "UPDATE productos SET precio = ? WHERE id = ?"
                    cursor.execute(query, plaseholder)
                    print("Dato guardado!\n")
                break
        elif opc == 4:
            print("saliendo...")
        else:
            print("Opcion invalida, por favor seleccione una opcion valida!!!")

        conexion.commit()
        conexion.close()
    else:
        print("El código no existe!!")


# eliminar un producto mediante su código
def elimiar_producto():
    # ingreso del codigo del producto a eliminar
    cod = int(input("Ingrese el código del producto: "))

    if existe_prod(cod):
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "DELETE FROM productos WHERE id = ?"
        cursor.execute(query, (cod,))
        conexion.commit()
        conexion.close()
        print("Producto eliminado!!")

    else:
        print("El producto no existe!!")


# Buscar productos por categoria
def buscar_productos_categoria():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    # ingreso de la categoria
    cat = input("Ingrese la categoria: ")
    # preparamos la consulta
    query = "SELECT * FROM productos WHERE categoria = ?"
    cursor.execute(query, (cat,))  # enviamos la consulta
    productos = cursor.fetchall()  # ponemos todos los resultados en productos
    # mostramos los productos
    for producto in productos:
        print("Productos:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Categoria: {producto[2]}")
        print(f"Descripción: {producto[3]}")
        print(f"Cantidad: {producto[4]}")
        print(f"Precio: {producto[5]}")
        print("-" * 20)

    conexion.close()


# reporte de los productos que tienen cantidad menor a 25 prudctos
def reporte_menores_productos():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM productos WHERE cantidad < 25"
    cursor.execute(query)  # enviamos la consulta
    productos = cursor.fetchall()  # ponemos todos los resultados en productos
    # mostramos los productos con bajo stock
    for producto in productos:
        print("Productos:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Categoria: {producto[2]}")
        print(f"Descripción: {producto[3]}")
        print(f"Cantidad: {producto[4]}")
        print(f"Precio: {producto[5]}")
        print("-" * 20)

    conexion.close()


while True:
    print(
        """
    --------------------------------------
                MENÚ PRINCIPAL 
    --------------------------------------
        """
    )
    crear_db()

    print("1. Agregar Producto")
    print("2. Actualizar Cantidad de Producto")
    print("3. ELiminar Producto")
    print("4. Reporte de bajo stok")
    print("5. Mostrar Producto")
    print("6. Salir")

    opcion = int(input("Seleccione la opcion que quiera ejecutar: "))
    print("\n")
    if opcion == 1:
        reg_productos()
    elif opcion == 2:
        actualizar_productos()
    elif opcion == 3:
        elimiar_producto()
    elif opcion == 4:
        reporte_menores_productos()
    elif opcion == 5:
        while True:

            print("1. Mostrar Todos los Producto")
            print("2. Mostrar Producto por Categoria")
            Maus = int(input("Seleccione una opcion: "))

            if Maus == 1:
                mostrar_productos()
                break
            elif Maus == 2:
                buscar_productos_categoria()
                break
            else:
                print("Opcion invalida, por favor seleccione una opcion valida!!!")

    elif opcion == 6:
        print("saliendo...")
        break
    else:
        print("Opcion invalida, por favor seleccione una opcion valida!!!")
