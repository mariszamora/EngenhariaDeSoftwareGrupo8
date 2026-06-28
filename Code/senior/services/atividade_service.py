# services/atividade_service.py - CORRIGIDO (FORÇA ATUALIZAÇÃO)
import streamlit as st
import json
import os
from datetime import datetime
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Senior, Tutor
from models.aviso import Aviso

PASTA_DADOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
ARQUIVO_ATIVIDADES = os.path.join(PASTA_DADOS, "atividades.json")
ARQUIVO_USUARIOS = os.path.join(PASTA_DADOS, "usuarios.json")
ARQUIVO_AVISOS = os.path.join(PASTA_DADOS, "avisos.json")

# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_todos_dados():
    """Carrega atividades e usuarios do JSON para o session_state"""
    os.makedirs(PASTA_DADOS, exist_ok=True)
    
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

    # Carrega avisos
    if "avisos" not in st.session_state:
        if os.path.exists(ARQUIVO_AVISOS):
            with open(ARQUIVO_AVISOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                st.session_state.avisos = [Aviso(**item) for item in dados.get("avisos", [])]
                st.session_state.proximo_aviso_id = dados.get("proximo_aviso_id", 1)
        else:
            st.session_state.avisos = []
            st.session_state.proximo_aviso_id = 1

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
    if "atividades" not in st.session_state:
        return
    
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
    
    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(ARQUIVO_ATIVIDADES, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def _salvar_usuarios():
    """Salva usuarios no JSON"""
    if "usuarios" not in st.session_state:
        return
    
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
    
    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)



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
    #aqui salva no joson



def inscrever_senior(senior_id, atividade_id):
    """Inscreve um senior em uma atividade e SALVA NO JSON"""
    carregar_todos_dados()
    
    # Busca atividade
    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return {"sucesso": False, "mensagem": "Atividade nao encontrada."}
    
    # Busca senior na lista
    senior = None
    senior_index = -1
    for i, u in enumerate(st.session_state.usuarios):
        if u.id == senior_id and isinstance(u, Senior):
            senior = u
            senior_index = i
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
    
 
    st.session_state.usuarios[senior_index] = senior
    

    if st.session_state.usuario_atual and st.session_state.usuario_atual.id == senior_id:
        st.session_state.usuario_atual = senior
    
    for a in senior.atividades_inscritas:
        print(a.id, a.titulo)
    _salvar_atividades()
    _salvar_usuarios()
    
    print(f" Inscricao salva: {senior.nome} -> {atividade.titulo}")
    print(f"   Atividades do senior: {[a.titulo for a in senior.atividades_inscritas]}")
    
    return {"sucesso": True, "mensagem": f"Inscricao realizada com sucesso em: {atividade.titulo}!"}

def cancelar_inscricao(senior_id, atividade_id):
    """Cancela a inscricao de um senior"""
    carregar_todos_dados()
    
    atividade = buscar_atividade_por_id(atividade_id)
    if not atividade:
        return {"sucesso": False, "mensagem": "Atividade nao encontrada."}
    
    senior = None
    senior_index = -1
    for i, u in enumerate(st.session_state.usuarios):
        if u.id == senior_id and isinstance(u, Senior):
            senior = u
            senior_index = i
            break
    
    if not senior:
        return {"sucesso": False, "mensagem": "Senior nao encontrado."}
    
    atividade.inscritos = [i for i in atividade.inscritos if i.id != senior_id]
    senior.atividades_inscritas = [a for a in senior.atividades_inscritas if a.id != atividade_id]
    
    st.session_state.usuarios[senior_index] = senior
    
    if st.session_state.usuario_atual and st.session_state.usuario_atual.id == senior_id:
        st.session_state.usuario_atual = senior
    
    _salvar_atividades()
    _salvar_usuarios()
    
    return {"sucesso": True, "mensagem": "Inscricao cancelada com sucesso!"}

def listar_atividades_do_senior(senior_id):
    carregar_todos_dados()
    for u in st.session_state.usuarios:
        if u.id == senior_id and isinstance(u, Senior):
            return u.atividades_inscritas
    return []


# ==========================================
# MURAL DE AVISOS
# ==========================================

def _salvar_avisos():
    """Salva avisos no JSON"""
    if "avisos" not in st.session_state:
        return

    dados = {
        "proximo_aviso_id": st.session_state.proximo_aviso_id,
        "avisos": [aviso.to_dict() for aviso in st.session_state.avisos]
    }

    os.makedirs(PASTA_DADOS, exist_ok=True)
    with open(ARQUIVO_AVISOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def listar_avisos():
    carregar_todos_dados()
    return st.session_state.avisos

def criar_aviso(titulo, mensagem, autor):
    """Publica um novo aviso no mural"""
    carregar_todos_dados()

    aviso = Aviso(
        id=st.session_state.proximo_aviso_id,
        titulo=titulo,
        mensagem=mensagem,
        autor=autor,
        data=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
    st.session_state.proximo_aviso_id += 1
    st.session_state.avisos.insert(0, aviso)
    _salvar_avisos()
    return aviso

def remover_aviso(aviso_id):
    """Remove um aviso do mural"""
    carregar_todos_dados()
    st.session_state.avisos = [a for a in st.session_state.avisos if a.id != aviso_id]
    _salvar_avisos()