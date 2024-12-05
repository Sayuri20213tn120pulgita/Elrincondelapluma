from wtforms.validators import none_of

from .entities.Autor import Autor
from .entities.Libro import Libro

class ModeloLibro():

    @classmethod
    def listar_libros(self, db):
        try:
            print(f"Estoy devolviendo algo {db}")
            cursor = db.connection.cursor()
            sql = """SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio, LIB.imagen_portada,
                    AUT.apellidos, AUT.nombres
                    FROM libros LIB JOIN autor AUT ON LIB.autor_id = AUT.id
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros = []
            for row in data:
                aut = Autor(0, row[4], row[5])
                lib = Libro(row[0], row[1],aut, row[2], row[3], row[4])
                print(lib.img_portada)
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def leer_libro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, titulo, anoedicion, precio 
                    FROM libros WHERE isbn = {0}""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            libro = Libro(data[0], data[1], None, data[2], data[3], None)
            return libro
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listar_libros_vendidos(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COM.libro_isbn, LIB.titulo, LIB.precio,
                    COUNT(COM.libro_isbn) AS Unidades_Vendidas
                    FROM compra COM JOIN libros LIB on COM.libro_isbn = LIB.isbn
                    GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros = []
            for row in data:
                lib = Libro(row[0], row[1],None, None, row[2],None)
                lib.unidades_vendidas = int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_libro(self, db, libro):
        try:
            titulo = libro.titulo
            precio = libro.precio
            imagen = libro.img_portada


            if imagen:
                cursor = db.connection.cursor()
                sql = """UPDATE libros 
                         SET titulo = '{0}', 
                             anoedicion = '{1}', 
                             precio = {2}, 
                             imagen_portada = '{3}' 
                         WHERE isbn = '{4}'""".format(titulo, anoedicion, precio, imagen, libro.isbn)
                cursor.execute(sql)
                db.connection.commit()
                return True
            else:
                cursor = db.connection.cursor()
                sql = """UPDATE libros 
                         SET titulo = '{0}', 
                             anoedicion = '{1}', 
                             precio = {2} 
                        WHERE isbn = '{3}'""".format(titulo, anoedicion, precio, libro.isbn)
                cursor.execute(sql)
                db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_datos_libro(self, db, isbn):

        try:
            cursor = db.connection.cursor()
            sql = "CALL obtener_libro_por_isbn(%s)"
            cursor.execute(sql, (isbn,))
            data = cursor.fetchone()  # Obtiene solo el primer registro

            libro_con_gemma = {
                "isbn": data[0],
                "titulo": data[1],
                "precio": data[2],
                "imagen_portada": data[3],
            }

            return libro_con_gemma
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def verificar_libro_en_compra(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) AS total FROM compra WHERE libro_isbn = %s"
            cursor.execute(sql, (isbn,))
            resultado = cursor.fetchone()
            return resultado[0] > 0  # Devuelve True si el libro existe, False si no
        except Exception as ex:
            print(f"Error al verificar el libro: {ex}")
            return False

    @classmethod
    def borrar_book(self, db, isbn):
         try:
             cursor = db.connection.cursor()
             sql = """DELETE FROM libros WHERE isbn = {0}""".format(isbn)
             cursor.execute(sql)
             db.connection.commit()
             return True
         except Exception as ex:
             raise Exception(ex)

    @classmethod
    def registrar_libro(self, db, libro):
        try:
            # Llamar al procedimiento almacenado
            cursor = db.connection.cursor()
            sql = "CALL registrar_libro(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                libro.isbn,
                libro.titulo,
                1,
                libro.precio,
                libro.img_portada
            ))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"Error al registrar libro: {ex}")