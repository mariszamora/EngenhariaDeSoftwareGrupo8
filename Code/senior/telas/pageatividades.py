# telas/pageatividades.py
import streamlit as st
from models.usuario import Senior
from services.atividade_service import (
    get_usuario_atual, listar_atividades_do_senior, cancelar_inscricao
)

def renderizar():
    usuario = get_usuario_atual()
    if not usuario:
        st.warning("Faça login para acessar.")
        return
    if not isinstance(usuario, Senior):
        st.warning("Esta página é apenas para Seniores.")
        return

    atividades = listar_atividades_do_senior(usuario.id)

    st.markdown("""
    <style>
        .page-header { margin-bottom: 20px; }
        .page-header h1 { font-size: 2rem; color: #1a4263; font-family: 'Georgia', serif; margin-bottom: 6px; }
        .page-header p { color: #4a5c6c; font-size: 1rem; font-weight: 500; }
        .thumb-box {
            height: 100px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
        }
        .card-body h3 {
            margin: 0;
            color: #1a4263;
            font-size: 1.2rem;
        }
        .card-body p {
            margin: 2px 0;
            color: #555;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="page-header">
            <h1>Minhas Atividades</h1>
            <p>Você está inscrito em {len(atividades)} atividade(s)</p>
        </div>
    """, unsafe_allow_html=True)

    if not atividades:
        st.info("Nenhuma atividade disponível.")
        return

    for atividade in atividades:
        # Envelopa cada atividade em um contêiner separado
        with st.container(border=True):
            icone = "💻 Remota" if atividade.tipo() == "Remota" else "📍 Presencial"
            cor = "#aa9393" if atividade.tipo() == "Remota" else "#8a7a7a"
            tutor_nm = atividade.tutor.nome if atividade.tutor else "Não definido"

            col_thumb, col_info, col_actions = st.columns([1.5, 3, 1.5], vertical_alignment="center")

            with col_thumb:
                st.markdown(f"""
                    <div class="thumb-box" style="background:{cor};">
                        🎬 {icone}
                    </div>
                """, unsafe_allow_html=True)

            with col_info:
                st.markdown(f"""
                    <div class="card-body">
                        <h3>{atividade.titulo}</h3>
                        <p>👤 <b>Tutor(a):</b> {tutor_nm}</p>
                        <p>🕐 {atividade.data} às {atividade.horario}</p>
                        <p>📍 {atividade.local}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_actions:
                with st.popover("Cancelar inscrição", use_container_width=True):
                    st.warning(f"Cancelar inscrição em '{atividade.titulo}'?")
                    col_sim, col_nao = st.columns(2)
                    with col_sim:
                        if st.button("Sim", key=f"cancel_sim_{atividade.id}", use_container_width=True):
                            resultado = cancelar_inscricao(usuario.id, atividade.id)
                            if resultado["sucesso"]:
                                st.session_state.flash_msg = resultado["mensagem"]
                            else:
                                st.session_state.flash_msg_error = resultado["mensagem"]
                            st.rerun()
                    with col_nao:
                        if st.button("Não", key=f"cancel_nao_{atividade.id}", use_container_width=True):
                            st.rerun()