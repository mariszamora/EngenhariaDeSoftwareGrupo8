import streamlit as st


def tela_tutor(usuario):

    st.title("Área do Tutor")

    st.write(usuario.nome)

    st.info("Cadastro de atividades virá na Parte 2.")

    if st.button("Sair"):

        st.session_state.clear()

        st.rerun()