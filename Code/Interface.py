import streamlit as st
from authController import realizar_login
from Usuario import Senior, Tutor

st.set_page_config(page_title="Comunidade 65+", layout="centered")


def renderizar_tela_login():
    """Desenha apenas o formulário de acesso."""
    st.markdown(
        "<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True
    )

    with st.form("form_login"):
        email = st.text_input("Seu E-mail:")
        senha = st.text_input("Sua Senha:", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            # 1. Chama a lógica isolada no outro arquivo
            resultado = realizar_login(email, senha)

            if resultado["sucesso"]:
                # 2. Salva O OBJETO no estado do Streamlit
                st.session_state["usuario_logado"] = resultado["usuario"]
                st.rerun()  # Recarrega a página
            else:
                st.error(resultado["erro"])


def renderizar_sistema_principal():
    """Desenha a plataforma baseada na CLASSE do usuário logado."""
    # Recuperamos o objeto salvo
    usuario = st.session_state["usuario_logado"]

    st.success(f"Bem-vindo(a), {usuario.nome_completo}!")

    # Aplica lógica de design universal se a preferência estiver ativa
    if usuario.alto_contraste:
        st.info("💡 Modo de Alto Contraste ativado via preferências.")

    st.write("---")

    # POLIMORFISMO VISUAL: A tela muda dependendo da classe instanciada
    if isinstance(usuario, Senior):
        st.subheader("🗓️ Seu Calendário de Atividades")
        st.write("Aqui apareceriam as atividades do sênior...")

        # Botão usando atributo exclusivo da classe Senior
        if st.button("🚨 Botão de Ajuda"):
            st.warning(f"Notificando emergência para: {usuario.contato_emergencia}")

    elif isinstance(usuario, Tutor):
        st.subheader("⚙️ Painel de Gerenciamento")
        st.write(f"Especialidade registrada: **{usuario.especialidade}**")

        # Botões exclusivos para a visão do Tutor
        st.button("＋ Nova Atividade")
        st.button("📋 Lista de Presença")

    st.write("---")
    if st.button("Sair da conta"):
        st.session_state.clear()
        st.rerun()


# ==========================================
# Maestro (Ponto de Entrada do Arquivo)
# ==========================================
if "usuario_logado" not in st.session_state:
    renderizar_tela_login()
else:
    renderizar_sistema_principal()
