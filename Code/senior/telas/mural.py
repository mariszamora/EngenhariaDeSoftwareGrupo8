import streamlit as st
from models.usuario import Tutor
from services.atividade_service import (
    get_usuario_atual,
    listar_avisos,
    criar_aviso,
    remover_aviso
)


def renderizar():
    """Renderiza o mural de avisos da comunidade"""

    usuario = get_usuario_atual()

    if usuario is None:
        st.warning("Por favor, faca login para acessar o mural.")
        return

    st.title("📢 Mural de Avisos")
    st.caption("Fique por dentro das novidades da comunidade")

    if isinstance(usuario, Tutor):
        with st.expander("➕ Publicar novo aviso", expanded=False):
            with st.form("form_novo_aviso", clear_on_submit=True):
                titulo = st.text_input("Titulo*", placeholder="Ex: Mudanca de horario")
                mensagem = st.text_area("Mensagem*", placeholder="Escreva o aviso aqui...")

                if st.form_submit_button("Publicar aviso", use_container_width=True):
                    if titulo and mensagem:
                        criar_aviso(titulo, mensagem, usuario.nome)
                        st.success("Aviso publicado com sucesso!")
                        st.rerun()
                    else:
                        st.warning("Preencha o titulo e a mensagem.")

    st.divider()

    avisos = listar_avisos()

    if not avisos:
        st.info("Nenhum aviso publicado ainda.")
        return

    for aviso in avisos:
        with st.container(border=True):
            st.subheader(aviso.titulo)
            st.write(aviso.mensagem)
            st.caption(f"Publicado por {aviso.autor} em {aviso.data}")

            if isinstance(usuario, Tutor):
                if st.button("🗑️ Remover", key=f"remover_aviso_{aviso.id}"):
                    remover_aviso(aviso.id)
                    st.rerun()
