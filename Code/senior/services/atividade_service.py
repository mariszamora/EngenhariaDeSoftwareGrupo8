# services/atividade_service.py - VERSÃO SIMPLES E FUNCIONAL
import streamlit as st
import json
import os
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Senior, Tutor

ARQUIVO_ATIVIDADES = "data/atividades.json"
ARQUIVO_USUARIOS = "data/usuarios.json"

# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_todos_dados():
    """Carrega atividades e usuarios do JSON para o session_state"""
    os.makedirs("data", exist_ok=True)
    
    # Carrega atividades
    if "atividades" not in st.session_state:
        if os.path.exists(ARQUIVO_ATIVIDADES):
            with open(ARQUIVO_ATIVIDADES, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                st.session_state.atividades = []
                st.session_state.proximo_id = dados.get("proximo_id", 1)
                for item in dados.get("atividades", []):
                    if item["tipo"] == "Remota":
                        atividade = AtividadeRemota(
                            id=item["id"],
                            titulo=item["titulo"],
                            descricao=item["descricao"],
                            data=item["data"],
                            horario=item["horario"],
                            tutor=None,
                            local=item["local"],
                            vagas=item["vagas"],
                            link=item.get("link", "")
                        )
                    else:
                        atividade = AtividadePresencial(
                            id=item["id"],
                            titulo=item["titulo"],
                            descricao=item["descricao"],
                            data=item["data"],
                            horario=item["horario"],
                            tutor=None,
                            local=item["local"],
                            vagas=item["vagas"],
                            endereco=item.get("endereco", "")
                        )
                    st.session_state.atividades.append(atividade)
        else:
            st.session_state.atividades = []
            st.session_state.proximo_id = 1
            _criar_atividades_padrao()
    
    # Carrega usuarios
    if "usuarios" not in st.session_state:
        if os.path.exists(ARQUIVO_USUARIOS):
            with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                st.session_state.usuarios = []
                for item in dados:
                    if item["tipo"] == "senior":
                        usuario = Senior(
                            id=item["id"],
                            nome=item["nome"],
                            email=item["email"],
                            telefone=item["telefone"],
                            senha=item["senha"],
                            contato_emergencia=item["contato_emergencia"]
                        )
                        usuario.atividades_inscritas = []
                        for ativ_id in item.get("atividades_inscritas", []):
                            ativ = buscar_atividade_por_id(ativ_id)
                            if ativ:
                                usuario.atividades_inscritas.append(ativ)
                    else:
                        usuario = Tutor(
                            id=item["id"],
                            nome=item["nome"],
                            email=item["email"],
                            telefone=item["telefone"],
                            senha=item["senha"],
                            especialidade=item["especialidade"]
                        )
                    st.session_state.usuarios.append(usuario)
        else:
            st.session_state.usuarios = [
                Senior(
                    id=1,
                    nome="Antonio Silva",
                    email="antonio@email.com",
                    telefone="(11) 99999-9999",
                    senha="123",
                    contato_emergencia="Maria - (11) 98888-8888"
                ),
                Tutor(
                    id=2,
                    nome="Carlos Souza",
                    email="carlos@email.com",
                    telefone="(11) 98888-7777",
                    senha="321",
                    especialidade="Educacao Fisica"
                )
            ]
    
    # Seta usuario atual se nao existir
    if "usuario_atual" not in st.session_state and st.session_state.usuarios:
        st.session_state.usuario_atual = st.session_state.usuarios[0]

def _criar_atividades_padrao():
    """Cria atividades padrao"""
    ativ1 = AtividadeRemota(
        id=0,
        titulo="Roda de Conversa",
        descricao="Conversa entre os participantes.",
        data="01/06",
        horario="13:30",
        tutor=None,
        local="Sala Virtual",
        vagas=30,
        link="https://meet.google.com/"
    )
    ativ1.id = 1
    st.session_state.atividades.append(ativ1)
    st.session_state.proximo_id = 2
    
    ativ2 = AtividadePresencial(
        id=0,
        titulo="Pilates",
        descricao="Pilates para terceira idade.",
        data="04/06",
        horario="13:30",
        tutor=None,
        local="Parque Central",
        vagas=20,
        endereco="Parque Central"
    )
    ativ2.id = 2
    st.session_state.atividades.append(ativ2)
    st.session_state.proximo_id = 3
    
    ativ3 = AtividadeRemota(
        id=0,
        titulo="Yoga",
        descricao="Alongamento e relaxamento.",
        data="08/06",
        horario="08:00",
        tutor=None,
        local="Google Meet",
        vagas=40,
        link="https://meet.google.com/"
    )
    ativ3.id = 3
    st.session_state.atividades.append(ativ3)
    st.session_state.proximo_id = 4
    
    _salvar_atividades()

# ==========================================
# SALVAR DADOS
# ==========================================

def _salvar_atividades():
    """Salva atividades no JSON"""
    dados = {
        "proximo_id": st.session_state.proximo_id,
        "atividades": []
    }
    for atividade in st.session_state.atividades:
        item = {
            "id": atividade.id,
            "titulo": atividade.titulo,
            "descricao": atividade.descricao,
            "data": atividade.data,
            "horario": atividade.horario,
            "local": atividade.local,
            "vagas": atividade.vagas,
            "tipo": atividade.tipo()
        }
        if isinstance(atividade, AtividadeRemota):
            item["link"] = atividade.link
        else:
            item["endereco"] = atividade.endereco
        dados["atividades"].append(item)
    
    os.makedirs("data", exist_ok=True)
    with open(ARQUIVO_ATIVIDADES, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def _salvar_usuarios():
    """Salva usuarios no JSON"""
    dados = []
    for usuario in st.session_state.usuarios:
        item = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "senha": usuario.senha,
        }
        if isinstance(usuario, Senior):
            item["tipo"] = "senior"
            item["contato_emergencia"] = usuario.contato_emergencia
            item["atividades_inscritas"] = [a.id for a in usuario.atividades_inscritas]
        else:
            item["tipo"] = "tutor"
            item["especialidade"] = usuario.especialidade
        dados.append(item)
    
    os.makedirs("data", exist_ok=True)
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ==========================================
# API PUBLICA
# ==========================================

def get_usuario_atual():
    carregar_todos_dados()
    return st.session_state.get("usuario_atual")

def set_usuario_atual(usuario):
    carregar_todos_dados()
    st.session_state.usuario_atual = usuario
    _salvar_usuarios()

def get_all_usuarios():
    carregar_todos_dados()
    return st.session_state.usuarios

def listar_atividades():
    carregar_todos_dados()
    return st.session_state.atividades

def buscar_atividade_por_id(id):
    carregar_todos_dados()
    for atividade in st.session_state.atividades:
        if atividade.id == id:
            return atividade
    return None

def criar_atividade(atividade):
    carregar_todos_dados()
    atividade.id = st.session_state.proximo_id
    st.session_state.proximo_id += 1
    st.session_state.atividades.append(atividade)
    _salvar_atividades()

def inscrever_senior(senior_id, atividade_id):
    carregar_todos_dados()
    
    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return {"sucesso": False, "mensagem": "Atividade nao encontrada."}
    
    senior = None
    for u in st.session_state.usuarios:
        if u.id == senior_id and isinstance(u, Senior):
            senior = u
            break
    
    if not senior:
        return {"sucesso": False, "mensagem": "Senior nao encontrado."}
    
    for inscrito in atividade.inscritos:
        if inscrito.id == senior_id:
            return {"sucesso": False, "mensagem": "Voce ja esta inscrito."}
    
    if not atividade.possui_vaga():
        return {"sucesso": False, "mensagem": "Turma lotada."}
    
    atividade.inscritos.append(senior)
    senior.atividades_inscritas.append(atividade)
    
    _salvar_atividades()
    _salvar_usuarios()
    
    return {"sucesso": True, "mensagem": "Inscricao realizada com sucesso!"}

def listar_atividades_do_senior(senior_id):
    carregar_todos_dados()
    for u in st.session_state.usuarios:
        if u.id == senior_id and isinstance(u, Senior):
            return u.atividades_inscritas
    return []