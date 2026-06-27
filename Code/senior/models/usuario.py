# models/usuario.py
class Usuario:
    def __init__(
        self,
        id,
        nome,
        email,
        telefone,
        senha,
        tamanho_fonte=16,
        alto_contraste=False
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.tamanho_fonte = tamanho_fonte
        self.alto_contraste = alto_contraste

class Senior(Usuario):
    def __init__(
        self,
        contato_emergencia,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.contato_emergencia = contato_emergencia
        self.atividades_inscritas = []

    def inscrever_em_atividade(self, atividade) -> bool:
        # já inscrito?
        if atividade in self.atividades_inscritas:
            return False

        # tenta inscrever na atividade
        if not atividade.inscrever(self):
            return False

        self.atividades_inscritas.append(atividade)
        return True

    def cancelar_inscricao(self, atividade) -> bool:
        if atividade not in self.atividades_inscritas:
            return False

        atividade.cancelar(self)
        self.atividades_inscritas.remove(atividade)
        return True

    def listar_atividades_inscritas(self):
        return self.atividades_inscritas


class Tutor(Usuario):
    def __init__(
        self,
        especialidade,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.especialidade = especialidade
        self.atividades_criadas = []
    
    def criar_atividade(self, atividade) -> bool:
        for existente in self.atividades_criadas:
            if existente.id == atividade.id:
                return False
        
        self.atividades_criadas.append(atividade)
        return True
    
    def listar_atividades_criadas(self):
        return self.atividades_criadas
    
    def remover_atividade(self, atividade) -> bool:
        self.atividades_criadas = [a for a in self.atividades_criadas if a.id != atividade.id]
        return True