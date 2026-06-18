class Usuario:
    def __init__(
        self,
        id: int,
        senha: str,
        nome_completo: str,
        telefone: str,
        email: str,
        tamanho_fonte: int,
        alto_contraste: bool,
    ):
        self.id = id
        self.senha = senha
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.email = email
        self.tamanho_fonte = tamanho_fonte
        self.alto_contraste = alto_contraste


class Senior(Usuario):
    def __init__(
        self,
        id: int,
        senha: str,
        nome_completo: str,
        telefone: str,
        email: str,
        tamanho_fonte: int,
        alto_contraste: bool,
        contato_emergencia: str,
    ):
        super().__init__(
            id, senha, nome_completo, telefone, email, tamanho_fonte, alto_contraste
        )
        # Atributo exclusivo senior
        self.contato_emergencia = contato_emergencia


class Tutor(Usuario):
    def __init__(
        self,
        id: int,
        senha: str,
        nome_completo: str,
        telefone: str,
        email: str,
        tamanho_fonte: int,
        alto_contraste: bool,
        especialidade: str,
    ):
        super().__init__(
            id, senha, nome_completo, telefone, email, tamanho_fonte, alto_contraste
        )
        self.especialidade = especialidade
