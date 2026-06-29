import streamlit as st
import telas.calendario as calendario
import telas.pageatividades as atividades
import telas.mural as mural
from models.usuario import Senior, Tutor
from services.atividade_service import (
    get_usuario_atual,
    set_usuario_atual,
    get_all_usuarios,
    carregar_todos_dados,
)

st.set_page_config(page_title="Comunidade 65+", layout="wide")

# CSS para remover elementos nativos e ajustar layout
st.markdown(
    """
<style>
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stDeployButton"],
    #stDecoration,
    [data-testid="stSidebar"],
    #MainMenu,
    footer { display: none !important; }

    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"],
    .main {
        background-color: #d2e1eb !important;
        color: #1a4263 !important;
    }

    .block-container { padding: 3rem 1rem 1rem 1rem !important; max-width: 100% !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    iframe { border: none !important; display: block !important; }

    /* Estilo do perfil */
    .profile-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: white;
        border-radius: 20px;
        border: 1.5px solid #1a4263;
        padding: 6px 12px;
        gap: 4px;
    }
    .profile-name {
        font-weight: 700;
        font-size: 0.9rem;
        color: #1a4263;
        text-align: center;
    }
    .profile-sair {
        background: #e74c3c;
        color: white;
        border: none;
        border-radius: 999px;
        padding: 4px 16px;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
        width: 100%;
        text-align: center;
    }
    .profile-sair:hover {
        background: #c0392b;
    }
    /* Botões da navbar */
    .stButton > button {
        border-radius: 999px !important;
        padding: 10px 16px !important;
        color: #1a4263 !important;
        background-color: #ffffff !important;
        border: 1px solid #1a4263 !important;
        box-shadow: 0 6px 15px rgba(26,66,99,0.12) !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        transition: background-color 0.16s ease, transform 0.12s ease !important;
    }
    .stButton > button:hover {
        background-color: #eaf1f8 !important;
    }
    .stButton > button:active {
        transform: translateY(1px) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Carrega dados
carregar_todos_dados()

# Inicializa estado
if "pagina" not in st.session_state:
    st.session_state.pagina = "Calendario"
if "mes_atual" not in st.session_state:
    from datetime import datetime

    now = datetime.now()
    st.session_state.mes_atual = now.month
    st.session_state.ano_atual = now.year
if "mostra_painel_tutor" not in st.session_state:
    st.session_state.mostra_painel_tutor = False
if "mostra_painel_aviso" not in st.session_state:
    st.session_state.mostra_painel_aviso = False

usuario = get_usuario_atual()

# Tela de login
if usuario is None:
    st.markdown(
        """
        <style>
            .block-container { padding: 4rem !important; }
        </style>
    """,
        unsafe_allow_html=True,
    )
    st.title("Comunidade 65+")
    st.caption("Escolha um perfil para acessar o sistema")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sênior")
        st.write("Acesse o calendário, veja atividades e se inscreva!")
        if st.button("Entrar como SÊNIOR", use_container_width=True):
            senior = next(
                (u for u in get_all_usuarios() if isinstance(u, Senior)), None
            )
            if senior:
                set_usuario_atual(senior)
                st.rerun()
            else:
                st.error("Nenhum sênior encontrado.")
    with col2:
        st.subheader("Tutor")
        st.write("Gerencie atividades, crie eventos e acompanhe alunos!")
        if st.button("Entrar como TUTOR", use_container_width=True):
            tutor = next((u for u in get_all_usuarios() if isinstance(u, Tutor)), None)
            if tutor:
                set_usuario_atual(tutor)
                st.rerun()
            else:
                st.error("Nenhum tutor encontrado.")
    st.stop()

eh_tutor = isinstance(usuario, Tutor)

# Navbar
col1, col2, col3, col4, col5, col_spacer, col_tutor, col_aviso, col_profile = (
    st.columns([1, 1.5, 1.5, 1.5, 1.5, 1.5, 1.2, 1.2, 1.8])
)

with col1:
    st.markdown(
        """
    <div style="text-align: center; padding: 8px 0;">
        <span style="font-size: 1.1rem; font-weight: 900; background: linear-gradient(45deg, #f39c12, #9b59b6); 
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;">65+</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    if st.button("Calendário", use_container_width=True, key="btn_calendario"):
        st.session_state.pagina = "Calendario"
        st.rerun()

with col3:
    if st.button("Atividades", use_container_width=True, key="btn_atividades"):
        st.session_state.pagina = "Atividades"
        st.rerun()

with col4:
    if st.button("Mural", use_container_width=True, key="btn_mural"):
        st.session_state.pagina = "Mural"
        st.rerun()

with col5:
    if st.button("Ajuda", use_container_width=True, key="btn_ajuda"):
        st.session_state.pagina = "Ajuda"
        st.rerun()

with col_tutor:
    if eh_tutor:
        if st.button(
            "Nova Atividade", use_container_width=True, key="btn_nova_atividade"
        ):
            st.session_state.mostra_painel_tutor = (
                not st.session_state.mostra_painel_tutor
            )
            st.session_state.pagina = "Calendario"
            st.rerun()

with col_aviso:
    if eh_tutor:
        if st.button("Novo Aviso", use_container_width=True, key="btn_novo_aviso"):
            st.session_state.mostra_painel_aviso = (
                not st.session_state.mostra_painel_aviso
            )
            st.session_state.pagina = "Mural"
            st.rerun()

with col_profile:
    # Botão de perfil que abre o popover de Sair
    with st.popover(f"👤 Olá, {usuario.nome}", use_container_width=True):
        st.warning("Deseja realmente sair?")
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("Sim", use_container_width=True):
                set_usuario_atual(None)
                st.session_state.clear()
                st.rerun()
        with col_nao:
            if st.button("Não", use_container_width=True):
                st.rerun()

st.divider()

# Roteamento
if st.session_state.pagina == "Calendario":
    calendario.renderizar()
elif st.session_state.pagina == "Atividades":
    atividades.renderizar()
elif st.session_state.pagina == "Mural":
    mural.renderizar()
else:
    st.info("Página em desenvolvimento...")
