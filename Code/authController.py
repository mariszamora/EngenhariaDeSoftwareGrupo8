# auth_controller.py
from Usuario import Senior, Tutor


def realizar_login(email: str, senha: str) -> dict:
    """
    Valida as credenciais e retorna a instância correta da classe.
    No futuro, aqui é onde você fará a chamada ao banco de dados via SQLAlchemy.
    """

    # Simulando um banco de dados em memória para teste
    banco_fake = [
        Senior(
            id=1,
            senha="123",
            nome_completo="Roberto Silva",
            telefone="5599692735",
            email="roberto@email.com",
            tamanho_fonte=16,
            alto_contraste=True,
            contato_emergencia="Filha Maria - (55) 9999-9999",
        ),
        Tutor(
            id=2,
            senha="321",
            nome_completo="Carlos Souza",
            telefone="5598123456",
            email="carlos@email.com",
            tamanho_fonte=12,
            alto_contraste=False,
            especialidade="Fisioterapeuta",
        ),
    ]

    # Busca o usuário na nossa lista "falsa"
    for usuario in banco_fake:
        if usuario.email == email and usuario.senha == senha:
            # Retornamos sucesso e o OBJETO reconstruído
            return {"sucesso": True, "usuario": usuario}

    # Se terminar o loop e não achar ninguém:
    return {"sucesso": False, "erro": "E-mail ou senha incorretos."}
