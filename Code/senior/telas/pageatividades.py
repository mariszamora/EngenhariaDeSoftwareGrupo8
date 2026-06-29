# telas/pageatividades.py
import streamlit as st
from models.usuario import Senior
from services.atividade_service import (
    get_usuario_atual, listar_atividades_do_senior, cancelar_inscricao
)


def renderizar():
    usuario = get_usuario_atual()

    if usuario is None:
        st.warning("Por favor, faça login para acessar as atividades.")
        return
    if not isinstance(usuario, Senior):
        st.warning("Esta página é apenas para Seniores.")
        return

    atividades = listar_atividades_do_senior(usuario.id)

    st.markdown("""
    <style>
      *{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',Tahoma,sans-serif;}
      .page-header{margin-bottom:20px;}
      .page-header h1{font-size:2rem;color:#1a4263;font-family:'Georgia',serif;margin-bottom:6px;}
      .page-header p{color:#4a5c6c;font-size:1rem;font-weight:500;}
      .card{border-radius:14px;padding:18px;display:grid;grid-template-columns:200px auto;gap:20px;align-items:center;
            box-shadow:0 4px 12px rgba(0,0,0,.08);margin-bottom:18px;background:#ffffff;}
      .thumb{height:140px;border-radius:14px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;}
      .thumb::before{content:'🎬';color:rgba(255,255,255,.55);font-size:36px;}
      .badge{position:absolute;top:12px;right:12px;background:rgba(0,0,0,.6);color:white;
             padding:5px 10px;border-radius:12px;font-size:.78rem;font-weight:600;}
      .card-body{display:flex;flex-direction:column;gap:12px;}
      .card-title{font-size:1.35rem;font-weight:700;font-family:'Georgia',serif;color:#1a4263;margin-bottom:6px;}
      .tutor-row{display:flex;align-items:center;gap:10px;font-size:.95rem;font-weight:700;color:#4c4c4c;}
      .avatar{width:30px;height:30px;background:#554444;border-radius:50%;display:flex;
              align-items:center;justify-content:center;font-size:16px;color:white;}
      .info-row{font-size:.95rem;font-weight:600;color:#555;}
      .btn-cancelar{background:#c0392b;color:white;border:none;padding:10px 18px;border-radius:16px;
                    font-size:.95rem;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;}
      .btn-cancelar:hover{background:#a93226;}
      @media(max-width:760px){.card{grid-template-columns:1fr;}.thumb{width:100%;height:160px;}}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
      <div class="page-header">
        <h1>Minhas Atividades</h1>
        <p>Você está inscrito em {len(atividades)} atividade(s)</p>
      </div>
    """, unsafe_allow_html=True)

    if not atividades:
        st.info("Nenhuma atividade disponível no momento.")
        return

    for atividade in atividades:
        icone = "💻" if atividade.tipo() == "Remota" else "📍"
        cor = "#aa9393" if atividade.tipo() == "Remota" else "#8a7a7a"
        tutor_nm = atividade.tutor.nome if atividade.tutor else "Não definido"

        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                st.markdown(f"""
                  <div style='border-radius:14px;height:140px;background:{cor};display:flex;
                              align-items:center;justify-content:center;position:relative;'>
                    <div style='position:absolute;top:12px;right:12px;background:rgba(0,0,0,.6);color:white;
                                padding:5px 10px;border-radius:12px;font-size:.78rem;font-weight:600;'>
                        {icone} {atividade.tipo()}
                    </div>
                    <span style='font-size:36px;opacity:.55;'>🎬</span>
                  </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                  <div style='display:flex;flex-direction:column;gap:10px;'>
                    <div style='font-size:1.35rem;font-weight:700;color:#1a4263;'>{atividade.titulo}</div>
                    <div style='display:flex;align-items:center;gap:10px;font-size:.95rem;font-weight:700;color:#4c4c4c;'>
                      <div style='width:30px;height:30px;border-radius:50%;background:#554444;color:white;display:flex;
                                  align-items:center;justify-content:center;font-size:16px;'>👤</div>
                      Tutor(a) {tutor_nm}
                    </div>
                    <div style='font-size:.95rem;font-weight:600;color:#555;'>🕐 {atividade.data} às {atividade.horario}</div>
                    <div style='font-size:.95rem;font-weight:600;color:#555;'>📍 {atividade.local}</div>
                  </div>
                """, unsafe_allow_html=True)

        if st.button("Cancelar inscrição", key=f"cancelar_{atividade.id}", use_container_width=True):
            resultado = cancelar_inscricao(usuario.id, atividade.id)
            if resultado["sucesso"]:
                st.success(resultado["mensagem"])
            else:
                st.warning(resultado["mensagem"])
            st.rerun()
