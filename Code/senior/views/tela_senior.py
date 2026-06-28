import streamlit as st


def tela_senior(usuario):

    st.title("Área do Sênior")

    st.write(usuario.nome)

    st.info("Calendário virá na Parte 2.")

    if st.button("Sair"):

        st.session_state.clear()

        st.rerun()