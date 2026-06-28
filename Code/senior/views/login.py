import streamlit as st

from services.auth_service import login


def tela_login():

    st.title("Comunidade 65+")

    email = st.text_input("Email")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        usuario = login(email,senha)

        if usuario:

            st.session_state.usuario = usuario

            st.rerun()

        else:

            st.error("Login inválido")