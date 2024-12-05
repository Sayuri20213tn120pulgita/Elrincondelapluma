class Libro():

    def __init__(self, isbn, titulo, autor, anoedicion, precio, img_portada):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.anoedicion = anoedicion
        self.precio = precio
        self.unidades_vendidas = 0
        self.img_portada = img_portada