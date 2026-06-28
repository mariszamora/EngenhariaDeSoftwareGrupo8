# app.py - COMPLETO COM BOTOES PARA SENIOR E TUTOR
import streamlit as st
import telas.calendario as calendario
import telas.pageatividades as atividades
import telas.mural as mural
from models.usuario import Senior, Tutor
from services.atividade_service import (
    get_usuario_atual, set_usuario_atual, get_all_usuarios,
    carregar_todos_dados
)

st.set_page_config(
    page_title="Comunidade 65+",
    page_icon="",
    layout="wide"
)

# ==========================================
# CARREGA DADOS DO JSON
# ==========================================
carregar_todos_dados()

# ==========================================
# INICIALIZA PAGINA
# ==========================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Calendario"

# ==========================================
# VERIFICA SE TEM USUARIO LOGADO
# ==========================================
usuario = get_usuario_atual()

# ==========================================
# TELA DE ESCOLHA DE PERFIL (SE NAO TIVER USUARIO)
# ==========================================
if usuario is None:
    st.title("Comunidade 65+")
    st.caption("Escolha um perfil para acessar o sistema")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sênior")
        st.write("Acesse o calendário, veja atividades e se inscreva!")
        if st.button("Entrar como SÊNIOR", use_container_width=True):
            senior = None
            for u in get_all_usuarios():
                if isinstance(u, Senior):
                    senior = u
                    break
            
            if senior is None:
                senior = Senior(
                    id=1,
                    nome="Antonio Silva",
                    email="antonio@email.com",
                    telefone="(11) 99999-9999",
                    senha="123",
                    contato_emergencia="Maria - (11) 98888-8888"
                )
            
            set_usuario_atual(senior)
            st.rerun()
    
    with col2:
        st.subheader(" Tutor")
        st.write("Gerencie atividades, crie eventos e acompanhe alunos!")
        if st.button("Entrar como TUTOR", use_container_width=True):
            tutor = None
            for u in get_all_usuarios():
                if isinstance(u, Tutor):
                    tutor = u
                    break
            
            if tutor is None:
                tutor = Tutor(
                    id=2,
                    nome="Carlos Souza",
                    email="carlos@email.com",
                    telefone="(11) 98888-7777",
                    senha="321",
                    especialidade="Educacao Fisica"
                )
            
            set_usuario_atual(tutor)
            st.rerun()
    
    st.stop()


usuario = get_usuario_atual()

if usuario is None:
    st.warning("Erro ao carregar usuário. Tente novamente.")
    st.stop()


with st.sidebar:
    st.title("Comunidade 65+")
    st.divider()
    st.write(f"**Olá, {usuario.nome}!**")
    st.caption(f" {usuario.email}")
    st.caption(f"{'SENIOR' if isinstance(usuario, Senior) else 'TUTOR'}")
    
    if isinstance(usuario, Senior):
        st.caption(f" Inscrito em {len(usuario.atividades_inscritas)} atividades")
    
    st.divider()
    
 
    st.subheader("Trocar Perfil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sênior", use_container_width=True):
            senior = None
            for u in get_all_usuarios():
                if isinstance(u, Senior):
                    senior = u
                    break
            
            if senior is None:
                senior = Senior(
                    id=1,
                    nome="Antonio Silva",
                    email="antonio@email.com",
                    telefone="(11) 99999-9999",
                    senha="123",
                    contato_emergencia="Maria - (11) 98888-8888"
                )
            
            set_usuario_atual(senior)
            st.rerun()
    
    with col2:
        if st.button("Tutor", use_container_width=True):
            tutor = None
            for u in get_all_usuarios():
                if isinstance(u, Tutor):
                    tutor = u
                    break
            
            if tutor is None:
                tutor = Tutor(
                    id=2,
                    nome="Carlos Souza",
                    email="carlos@email.com",
                    telefone="(11) 98888-7777",
                    senha="321",
                    especialidade="Educacao Fisica"
                )
            
            set_usuario_atual(tutor)
            st.rerun()
    
    st.divider()
    
    # ==========================================
    # BOTOES DE NAVEGACAO
    # ==========================================
   

st.title("Comunidade 65+")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" CALENDÁRIO", use_container_width=True):
        st.session_state.pagina = "Calendario"
        st.rerun()

with col2:
    if st.button(" MINHAS ATIVIDADES", use_container_width=True):
        st.session_state.pagina = "Atividades"
        st.rerun()

with col3:
    if st.button("📢 MURAL DE AVISOS", use_container_width=True):
        st.session_state.pagina = "Mural"
        st.rerun()

with col4:
    if isinstance(usuario, Tutor):
        if st.button("➕ ADICIONAR EVENTO", use_container_width=True):
            st.session_state.pagina = "Calendario"
            st.session_state.abrir_formulario = True
            st.rerun()
    else:
        st.button("➕ ADICIONAR EVENTO", use_container_width=True, disabled=True)

st.divider()


if st.session_state.pagina == "Calendario":
    calendario.renderizar()
elif st.session_state.pagina == "Atividades":
    atividades.renderizar()
elif st.session_state.pagina == "Mural":
    mural.renderizar()
else:
    st.info("Página em desenvolvimento...")