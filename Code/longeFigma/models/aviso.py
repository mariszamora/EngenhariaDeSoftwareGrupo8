class Aviso:
    """
    Aviso publicado no mural pela equipe de tutores.
    """

    def __init__(
        self,
        id: int,
        titulo: str,
        mensagem: str,
        autor: str,
        data: str
    ):

        self.id = id
        self.titulo = titulo
        self.mensagem = mensagem
        self.autor = autor
        self.data = data

    def to_dict(self):

        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "autor": self.autor,
            "data": self.data
        }
