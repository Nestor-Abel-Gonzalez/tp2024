'''
Desafío 1: Sistema de Gestión de Productos

Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:
    •Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
    •Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
    •Implementar operaciones CRUD para gestionar productos del inventario.
    •Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    •Persistir los datos en archivo JSON.
'''
import json

class Producto:
    def __init__(self, id_producto, nombre, precio, cantidad):
        self.__id_producto = self.validar_id(id_producto)
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    @property
    def id_producto(self):
        return self.__id_producto
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    @property
    def cantidad(self):
        return self.__cantidad
    
    def validar_id(self, id_producto):
        if not id_producto:
            raise ValueError("El ID no puede estar vacío.")
        return id_producto

    def validar_precio(self, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser un valor positivo.")
        return precio
    
    def validar_cantidad(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        return cantidad

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }

    def __str__(self):
        return f"(ID: {self.id_producto}){self.nombre}  Cantidad: {self.cantidad}"

class ProductoElectronico(Producto):
    def __init__(self, id_producto, nombre, precio, cantidad, garantia):
        super().__init__(id_producto, nombre, precio, cantidad)
        self.__garantia = garantia

    @property
    def garantia(self):
        return self.__garantia

    def to_dict(self):
        data = super().to_dict()
        data["garantia"] = self.garantia
        return data

    def __str__(self):
        return f"{super().__str__()} - Garantía: {self.garantia}"

class ProductoAlimenticio(Producto):
    def __init__(self, id_producto, nombre, precio, cantidad, fecha_expiracion):
        super().__init__(id_producto, nombre, precio, cantidad)
        self.__fecha_expiracion = fecha_expiracion

    @property
    def fecha_expiracion(self):
        return self.__fecha_expiracion

    def to_dict(self):
        data = super().to_dict()
        data["fecha_expiracion"] = self.fecha_expiracion
        return data

    def __str__(self):
        return f"{super().__str__()} - Fecha de Expiración: {self.fecha_expiracion}"

class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            id_producto = producto.id_producto
            if not str(id_producto) in datos.keys():
                datos[id_producto] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"\nProducto {producto.nombre} creado correctamente.")
            else:
                print(f"Ya existe un producto con ID '{id_producto}'.")
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, id_producto):
        try:
            datos = self.leer_datos()
            if id_producto in datos:
                producto_data = datos[id_producto]
                if 'garantia' in producto_data:

                        producto = ProductoElectronico(**producto_data)
                else:
                    producto = ProductoAlimenticio(**producto_data)
                print(f'PRODUCTO ENCONTRADO: {producto}')
            else:
                print(f'¡¡No se encontró producto con ID!! {id_producto}')
        except Exception as e:
            print(f'Error al leer producto: {e}')

    def actualizar_producto(self, id_producto, nuevo_precio):
        try:
            datos = self.leer_datos()
            if str(id_producto) in datos.keys():
                 datos[id_producto]['precio'] = nuevo_precio
                 self.guardar_datos(datos)
                 print(f'Precio actualizado para el producto ID:{id_producto}')
            else:
                print(f'No se encontró producto con ID:{id_producto}')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, id_producto):
        try:
            datos = self.leer_datos()
            if str(id_producto) in datos.keys():
                 del datos[id_producto]
                 self.guardar_datos(datos)
                 print(f'Producto ID:{id_producto} eliminado correctamente')
            else:
                print(f'No se encontró producto con ID:{id_producto}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')