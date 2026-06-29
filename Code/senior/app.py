# app.py
import streamlit as st
import telas.calendario as calendario
import telas.pageatividades as atividades
from models.usuario import Senior, Tutor
from services.atividade_service import (
    get_usuario_atual, set_usuario_atual, get_all_usuarios,
    carregar_todos_dados
)

st.set_page_config(page_title="Comunidade 65+", layout="wide")

# ──────────────────────────────────────────────────────────────
# CSS GLOBAL — apaga absolutamente tudo do Streamlit nativo.
# O fundo preto vem do background padrão do Streamlit;
# forçamos #d2e1eb em todos os elementos possíveis.
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Esconde header, toolbar, sidebar, menu, footer */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stDeployButton"],
    #stDecoration,
    [data-testid="stSidebar"],
    #MainMenu,
    footer { display: none !important; }

    /* Fundo azul claro em TODA a página */
    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"],
    .main {
        background-color: #d2e1eb !important;
        color: #1a4263 !important;
    }

    /* Zera padding e largura do container */
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Remove gap entre elementos verticais */
    [data-testid="stVerticalBlock"] { gap: 0 !important; }

    /* Iframes: sem borda, display block para não criar linha extra */
    iframe { border: none !important; display: block !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# CARREGA DADOS
# ──────────────────────────────────────────
carregar_todos_dados()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Calendario"
if "mes_atual" not in st.session_state:
    from datetime import datetime
    now = datetime.now()
    st.session_state.mes_atual = now.month
    st.session_state.ano_atual = now.year
if "mostra_painel_tutor" not in st.session_state:
    st.session_state.mostra_painel_tutor = False

usuario = get_usuario_atual()

# ──────────────────────────────────────────
# TELA DE LOGIN
# ──────────────────────────────────────────
if usuario is None:
    # Na tela de login reativamos o padding para o conteúdo respirar
    st.markdown("""
        <style>
            [data-testid="stButton"],
            [data-testid="stHorizontalBlock"] { display: flex !important; }
            .block-container { padding: 4rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("Comunidade 65+")
    st.caption("Escolha um perfil para acessar o sistema")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sênior")
        st.write("Acesse o calendário, veja atividades e se inscreva!")
        if st.button("Entrar como SÊNIOR", use_container_width=True):
            senior = next((u for u in get_all_usuarios() if isinstance(u, Senior)), None)
            if senior is None:
                st.error("Nenhum sênior encontrado no sistema.")
            else:
                set_usuario_atual(senior)
                st.rerun()

    with col2:
        st.subheader("Tutor")
        st.write("Gerencie atividades, crie eventos e acompanhe alunos!")
        if st.button("Entrar como TUTOR", use_container_width=True):
            tutor = next((u for u in get_all_usuarios() if isinstance(u, Tutor)), None)
            if tutor is None:
                st.error("Nenhum tutor encontrado no sistema.")
            else:
                set_usuario_atual(tutor)
                st.rerun()
    st.stop()

# ──────────────────────────────────────────
# NAVBAR COM STREAMLIT BUTTONS (session_state puro, sem query_params)
# ──────────────────────────────────────────
eh_tutor = isinstance(usuario, Tutor)

st.markdown("""
<style>
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
    .stButton > button:focus-visible {
        outline: 3px solid #1a4263 !important;
        outline-offset: 2px !important;
    }
    .stButton > button:disabled {
        opacity: 0.65 !important;
        cursor: default !important;
    }
    .block-container {
        padding: 12px 16px 0 16px !important;
    }
    .stAppViewContainer {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col_spacer, col_tutor, col_profile = st.columns(
    [1, 1.5, 1.5, 1.5, 1.5, 2, 1.2, 1.5]
)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 8px 0;">
        <span style="font-size: 1.1rem; font-weight: 900; background: linear-gradient(45deg, #f39c12, #9b59b6); 
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;">65+</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Calendário", use_container_width=True, 
                 key="btn_calendario"):
        st.session_state.pagina = "Calendario"
        st.rerun()

with col3:
    if st.button("Atividades", use_container_width=True, 
                 key="btn_atividades"):
        st.session_state.pagina = "Atividades"
        st.rerun()

with col4:
    if st.button("Mural", use_container_width=True, 
                 key="btn_mural"):
        st.session_state.pagina = "Mural"
        st.rerun()

with col5:
    if st.button("Ajuda", use_container_width=True, 
                 key="btn_ajuda"):
        st.session_state.pagina = "Ajuda"
        st.rerun()

with col_tutor:
    if eh_tutor and st.button("Nova Atividade", use_container_width=True, 
                              key="btn_nova_atividade"):
        st.session_state.mostra_painel_tutor = not st.session_state.mostra_painel_tutor
        st.rerun()

with col_profile:
    st.markdown(f"""
    <div style="padding: 8px; text-align: center; border: 1.5px solid #1a4263; 
                border-radius: 20px; background: white; color: #1a4263; 
                font-weight: 700; font-size: 0.85rem;">
        Olá, {usuario.nome}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────
# ROTEAMENTO
# ──────────────────────────────────────────
if st.session_state.pagina == "Calendario":
    calendario.renderizar()
elif st.session_state.pagina == "Atividades":
    atividades.renderizar()
else:
    st.info("Página em desenvolvimento...")
