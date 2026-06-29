import streamlit as st
import json
import os
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Senior, Tutor

PASTA_DADOS    = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ARQUIVO_ATIVIDADES = os.path.join(PASTA_DADOS, "atividades.json")
ARQUIVO_USUARIOS   = os.path.join(PASTA_DADOS, "usuarios.json")
ARQUIVO_SESSAO     = os.path.join(PASTA_DADOS, "sessao.json")


# ══════════════════════════════════════════
# PERSISTÊNCIA — CARREGAR
# ══════════════════════════════════════════

def carregar_todos_dados():
    """Carrega atividades e usuários do JSON para o session_state (apenas uma vez por sessão)."""
    os.makedirs(PASTA_DADOS, exist_ok=True)

    if "atividades" not in st.session_state:
        if os.path.exists(ARQUIVO_ATIVIDADES):
            with open(ARQUIVO_ATIVIDADES, "r", encoding="utf-8") as f:
                dados = json.load(f)
            st.session_state.atividades = []
            st.session_state.proximo_id = dados.get("proximo_id", 1)
            for item in dados.get("atividades", []):
                if item["tipo"] == "Remota":
                    a = AtividadeRemota(
                        id=item["id"], titulo=item["titulo"], descricao=item["descricao"],
                        data=item["data"], horario=item["horario"], tutor=None,
                        local=item["local"], vagas=item["vagas"], link=item.get("link", "")
                    )
                else:
                    a = AtividadePresencial(
                        id=item["id"], titulo=item["titulo"], descricao=item["descricao"],
                        data=item["data"], horario=item["horario"], tutor=None,
                        local=item["local"], vagas=item["vagas"], endereco=item.get("endereco", "")
                    )
                st.session_state.atividades.append(a)
        else:
            st.session_state.atividades = []
            st.session_state.proximo_id = 1
            _criar_atividades_padrao()

    if "usuarios" not in st.session_state:
        if os.path.exists(ARQUIVO_USUARIOS):
            with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
            st.session_state.usuarios = []
            for item in dados:
                if item["tipo"] == "senior":
                    u = Senior(
                        id=item["id"], nome=item["nome"], email=item["email"],
                        telefone=item["telefone"], senha=item["senha"],
                        contato_emergencia=item["contato_emergencia"]
                    )
                    u.atividades_inscritas = []
                    for ativ_id in item.get("atividades_inscritas", []):
                        a = _buscar_atividade_raw(ativ_id)
                        if a:
                            u.atividades_inscritas.append(a)
                else:
                    u = Tutor(
                        id=item["id"], nome=item["nome"], email=item["email"],
                        telefone=item["telefone"], senha=item["senha"],
                        especialidade=item["especialidade"]
                    )
                st.session_state.usuarios.append(u)
        else:
            st.session_state.usuarios = [
                Senior(id=1, nome="Antonio Silva", email="antonio@email.com",
                       telefone="(11) 99999-9999", senha="123",
                       contato_emergencia="Maria - (11) 98888-8888"),
                Tutor(id=2, nome="Carlos Souza", email="carlos@email.com",
                      telefone="(11) 98888-7777", senha="321",
                      especialidade="Educacao Fisica"),
            ]
            _salvar_usuarios()

    # Reconecta o objeto Tutor às atividades após carregar os usuários
    if not st.session_state.get("_tutores_vinculados", False):
        if os.path.exists(ARQUIVO_ATIVIDADES):
            try:
                with open(ARQUIVO_ATIVIDADES, "r", encoding="utf-8") as f:
                    dados_ativ = json.load(f)
                for item in dados_ativ.get("atividades", []):
                    tutor_id = item.get("tutor_id")
                    if tutor_id:
                        # Busca atividade e tutor carregados na sessão
                        a = next((ativ for ativ in st.session_state.atividades if ativ.id == item["id"]), None)
                        t = next((u for u in st.session_state.usuarios if u.id == tutor_id), None)
                        if a and t:
                            a.tutor = t
            except Exception:
                pass
        st.session_state._tutores_vinculados = True


def _buscar_atividade_raw(id_atividade):
    """Busca sem chamar carregar_todos_dados (evita recursão durante o carregamento)."""
    for a in st.session_state.get("atividades", []):
        if a.id == id_atividade:
            return a
    return None


def _criar_atividades_padrao():
    st.session_state.atividades = [
        AtividadeRemota(id=1, titulo="Roda de Conversa", descricao="Conversa entre participantes.",
                        data="01/06", horario="13:30", tutor=None, local="Sala Virtual",
                        vagas=30, link="https://meet.google.com/"),
        AtividadePresencial(id=2, titulo="Pilates", descricao="Pilates para terceira idade.",
                            data="04/06", horario="13:30", tutor=None, local="Parque Central",
                            vagas=20, endereco="Parque Central"),
        AtividadeRemota(id=3, titulo="Yoga", descricao="Alongamento e relaxamento.",
                        data="08/06", horario="08:00", tutor=None, local="Google Meet",
                        vagas=40, link="https://meet.google.com/"),
    ]
    st.session_state.proximo_id = 4
    _salvar_atividades()


# ══════════════════════════════════════════
# PERSISTÊNCIA — SALVAR
# ══════════════════════════════════════════

def _salvar_atividades():
    if "atividades" not in st.session_state:
        return
    dados = {"proximo_id": st.session_state.proximo_id, "atividades": []}
    for a in st.session_state.atividades:
        item = {"id": a.id, "titulo": a.titulo, "descricao": a.descricao,
                "data": a.data, "horario": a.horario, "local": a.local,
                "vagas": a.vagas, "tipo": a.tipo()}
        
        # SALVA O ID DO TUTOR
        if a.tutor:
            item["tutor_id"] = a.tutor.id
            
        if isinstance(a, AtividadeRemota):
            item["link"] = a.link
        else:
            item["endereco"] = a.endereco
        dados["atividades"].append(item)
    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(ARQUIVO_ATIVIDADES, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _salvar_usuarios():
    if "usuarios" not in st.session_state:
        return
    dados = []
    for u in st.session_state.usuarios:
        item = {"id": u.id, "nome": u.nome, "email": u.email,
                "telefone": u.telefone, "senha": u.senha}
        if isinstance(u, Senior):
            item["tipo"] = "senior"
            item["contato_emergencia"] = u.contato_emergencia
            item["atividades_inscritas"] = [a.id for a in u.atividades_inscritas]
        else:
            item["tipo"] = "tutor"
            item["especialidade"] = u.especialidade
        dados.append(item)
    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════
# SESSÃO / AUTENTICAÇÃO
# ══════════════════════════════════════════

def get_usuario_atual():
    carregar_todos_dados()
    # 1. Já está no session_state
    if st.session_state.get("usuario_atual") is not None:
        return st.session_state.usuario_atual
    # 2. Recupera do arquivo de sessão (anti-refresh)
    if os.path.exists(ARQUIVO_SESSAO):
        try:
            with open(ARQUIVO_SESSAO, "r") as f:
                uid = json.load(f).get("usuario_id")
            for u in st.session_state.usuarios:
                if u.id == uid:
                    st.session_state.usuario_atual = u
                    return u
        except Exception:
            pass
    return None


def set_usuario_atual(usuario):
    carregar_todos_dados()
    st.session_state.usuario_atual = usuario
    os.makedirs(PASTA_DADOS, exist_ok=True)
    if usuario is not None:
        with open(ARQUIVO_SESSAO, "w") as f:
            json.dump({"usuario_id": usuario.id}, f)
    else:
        if os.path.exists(ARQUIVO_SESSAO):
            os.remove(ARQUIVO_SESSAO)
    _salvar_usuarios()


def get_all_usuarios():
    carregar_todos_dados()
    return st.session_state.usuarios


# ══════════════════════════════════════════
# ATIVIDADES
# ══════════════════════════════════════════

def listar_atividades():
    carregar_todos_dados()
    return st.session_state.atividades


def buscar_atividade_por_id(id_atividade):
    carregar_todos_dados()
    return next((a for a in st.session_state.atividades if a.id == id_atividade), None)


def criar_atividade(atividade):
    carregar_todos_dados()
    atividade.id = st.session_state.proximo_id
    st.session_state.proximo_id += 1
    st.session_state.atividades.append(atividade)
    _salvar_atividades()


def deletar_atividade(atividade_id: int) -> bool:
    """Deleta totalmente uma atividade do sistema e remove a inscrição de todos os seniores."""
    carregar_todos_dados()
    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return False

    # Remove da lista geral de atividades
    st.session_state.atividades = [a for a in st.session_state.atividades if a.id != atividade_id]

    # Remove a atividade da lista de inscrições de todos os seniores cadastrados
    for u in st.session_state.usuarios:
        if isinstance(u, Senior):
            u.atividades_inscritas = [a for a in u.atividades_inscritas if a.id != atividade_id]

    # Garante a atualização também se o usuário logado atualmente for o sênior afetado
    if st.session_state.get("usuario_atual") and isinstance(st.session_state.usuario_atual, Senior):
        st.session_state.usuario_atual.atividades_inscritas = [
            a for a in st.session_state.usuario_atual.atividades_inscritas if a.id != atividade_id
        ]

    # Persiste as alterações nos arquivos correspondentes
    _salvar_atividades()
    _salvar_usuarios()
    return True


def inscrever_senior(senior_id: int, atividade_id: int) -> dict:
    """Inscreve um sênior em uma atividade com verificação dupla de duplicidade."""
    carregar_todos_dados()

    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return {"sucesso": False, "mensagem": "Atividade não encontrada."}

    senior = next(
        (u for u in st.session_state.usuarios if u.id == senior_id and isinstance(u, Senior)),
        None
    )
    if not senior:
        return {"sucesso": False, "mensagem": "Sênior não encontrado."}

    # Verificação dupla de duplicidade
    if any(i.id == senior_id for i in atividade.inscritos):
        return {"sucesso": False, "mensagem": "Você já está inscrito nesta atividade!"}
    if any(a.id == atividade_id for a in senior.atividades_inscritas):
        return {"sucesso": False, "mensagem": "Você já está inscrito nesta atividade!"}

    if not atividade.possui_vaga():
        return {"sucesso": False, "mensagem": "Turma lotada."}

    # Realiza a inscrição nos dois lados
    atividade.inscritos.append(senior)
    senior.atividades_inscritas.append(atividade)

    # Garante que o usuario_atual também reflita a mudança
    if st.session_state.get("usuario_atual") and st.session_state.usuario_atual.id == senior_id:
        st.session_state.usuario_atual = senior

    # Persiste
    _salvar_atividades()
    _salvar_usuarios()

    return {"sucesso": True, "mensagem": f"Inscrição realizada em: {atividade.titulo}!"}


def cancelar_inscricao(senior_id: int, atividade_id: int) -> dict:
    """Cancela a inscrição de um sênior em uma atividade."""
    carregar_todos_dados()

    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return {"sucesso": False, "mensagem": "Atividade não encontrada."}

    senior = next(
        (u for u in st.session_state.usuarios if u.id == senior_id and isinstance(u, Senior)),
        None
    )
    if not senior:
        return {"sucesso": False, "mensagem": "Sênior não encontrado."}

    if not any(a.id == atividade_id for a in senior.atividades_inscritas):
        return {"sucesso": False, "mensagem": "Você não está inscrito nesta atividade."}

    atividade.inscritos = [i for i in atividade.inscritos if i.id != senior_id]
    senior.atividades_inscritas = [a for a in senior.atividades_inscritas if a.id != atividade_id]

    if st.session_state.get("usuario_atual") and st.session_state.usuario_atual.id == senior_id:
        st.session_state.usuario_atual = senior

    _salvar_atividades()
    _salvar_usuarios()

    return {"sucesso": True, "mensagem": "Inscrição cancelada com sucesso!"}


def listar_atividades_do_senior(senior_id: int):
    carregar_todos_dados()
    for u in st.session_state.usuarios:
        if u.id == senior_id and isinstance(u, Senior):
            return u.atividades_inscritas
    return []