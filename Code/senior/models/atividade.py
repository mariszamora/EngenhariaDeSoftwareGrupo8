from abc import ABC, abstractmethod


class Atividade(ABC):
    """
    Classe base para qualquer atividade da plataforma.
    """

    def __init__(
        self,
        id: int,
        titulo: str,
        descricao: str,
        data: str,
        horario: str,
        tutor,
        local: str,
        vagas: int = 50
    ):

        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.horario = horario
        self.tutor = tutor
        self.local = local
        self.vagas = vagas

        # lista de objetos Senior
        self.inscritos = []

    @abstractmethod
    def tipo(self):
        pass

    def possui_vaga(self):

        return len(self.inscritos) < self.vagas

    def inscrever(self, senior):

        if senior in self.inscritos:
            return False

        if not self.possui_vaga():
            return False

        self.inscritos.append(senior)

        return True

    def cancelar(self, senior):

        if senior in self.inscritos:
            self.inscritos.remove(senior)
            return True

        return False


class AtividadePresencial(Atividade):

    def __init__(
        self,
        endereco: str,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.endereco = endereco

    def tipo(self):

        return "Presencial"


class AtividadeRemota(Atividade):

    def __init__(
        self,
        link: str,
        gravacao=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.link = link
        self.gravacao = gravacao

    def tipo(self):

        return "Remota"


class AulaGravada:

    def __init__(self, titulo, url_video):

        self.titulo = titulo

        self.url_video = url_video