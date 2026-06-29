# telas/mural.py
import streamlit as st
import json
import os
from models.usuario import Tutor
from services.atividade_service import get_usuario_atual

ARQUIVO_AVISOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "avisos.json"
)


def carregar_avisos():
    if "avisos" not in st.session_state:
        if os.path.exists(ARQUIVO_AVISOS):
            with open(ARQUIVO_AVISOS, "r", encoding="utf-8") as f:
                st.session_state.avisos = json.load(f)
        else:
            st.session_state.avisos = [
                {
                    "id": 1,
                    "titulo": "Bem-vindos!",
                    "data": "01/06/2026",
                    "conteudo": "A Comunidade 65+ está no ar!",
                },
                {
                    "id": 2,
                    "titulo": "Novo curso de Dança",
                    "data": "15/06/2026",
                    "conteudo": "Aulas de dança todas as terças e quintas, 10h.",
                },
            ]
            _salvar_avisos()


def _salvar_avisos():
    os.makedirs(os.path.dirname(ARQUIVO_AVISOS), exist_ok=True)
    with open(ARQUIVO_AVISOS, "w", encoding="utf-8") as f:
        json.dump(st.session_state.avisos, f, ensure_ascii=False, indent=2)


def renderizar():
    usuario = get_usuario_atual()
    if not usuario:
        st.warning("Faça login para acessar o mural.")
        return

    carregar_avisos()
    eh_tutor = isinstance(usuario, Tutor)

    st.markdown(
        """
    <style>
        .aviso-card {
            background: white;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-left: 6px solid #7d4ba7;
        }
        .aviso-titulo {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a4263;
            margin-bottom: 6px;
        }
        .aviso-data {
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 10px;
        }
        .aviso-conteudo {
            font-size: 1rem;
            color: #333;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='color:#1a4263;'>📢 Mural de Avisos</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#4a5c6c;'>Fique por dentro das novidades da comunidade!</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Formulário para tutor (se o estado mostrar_painel_aviso estiver ativo)
    if eh_tutor and st.session_state.get("mostra_painel_aviso", False):
        st.markdown('<div id="ancora-novo-aviso"></div>', unsafe_allow_html=True)
        import streamlit.components.v1 as components

        components.html(
            "<script>window.parent.document.getElementById('ancora-novo-aviso').scrollIntoView({behavior:'smooth'});</script>",
            height=0,
        )
        with st.expander("➕ Criar novo aviso", expanded=True):
            with st.form("form_novo_aviso", clear_on_submit=True):
                titulo = st.text_input("Título do aviso*")
                conteudo = st.text_area("Conteúdo*", height=100)
                c_salvar, c_cancelar = st.columns(2)
                with c_salvar:
                    salvar = st.form_submit_button("Publicar", use_container_width=True)
                with c_cancelar:
                    cancelar = st.form_submit_button(
                        "Cancelar", use_container_width=True
                    )
                if cancelar:
                    st.session_state.mostra_painel_aviso = False
                    st.rerun()
                if salvar:
                    if not titulo or not conteudo:
                        st.error("Preencha todos os campos.")
                    else:
                        from datetime import datetime

                        data_atual = datetime.now().strftime("%d/%m/%Y")
                        novo = {
                            "id": len(st.session_state.avisos) + 1,
                            "titulo": titulo,
                            "data": data_atual,
                            "conteudo": conteudo,
                        }
                        st.session_state.avisos.append(novo)
                        _salvar_avisos()
                        st.session_state.mostra_painel_aviso = False
                        st.success("Aviso publicado com sucesso!")
                        st.rerun()
        st.divider()

    # Exibe avisos
    if not st.session_state.avisos:
        st.info("Nenhum aviso disponível.")
        return

    for aviso in st.session_state.avisos:
        col_aviso, col_acao = st.columns([6, 1])
        with col_aviso:
            st.markdown(
                f"""
                <div class="aviso-card">
                    <div class="aviso-titulo">{aviso["titulo"]}</div>
                    <div class="aviso-data">📅 {aviso["data"]}</div>
                    <div class="aviso-conteudo">{aviso["conteudo"]}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with col_acao:
            if eh_tutor:
                if st.button("🗑️", key=f"remover_{aviso['id']}", help="Remover aviso"):
                    st.session_state.avisos = [
                        a for a in st.session_state.avisos if a["id"] != aviso["id"]
                    ]
                    _salvar_avisos()
                    st.rerun()
