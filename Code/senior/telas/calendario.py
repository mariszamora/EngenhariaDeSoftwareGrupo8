# telas/calendario.py
import streamlit as st
import streamlit.components.v1 as components
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Tutor, Senior
from services.atividade_service import (
    listar_atividades, criar_atividade,
    inscrever_senior, get_usuario_atual
)
import calendar
import json


def _atividades_por_dia() -> dict:
    result = {}
    for a in listar_atividades():
        result.setdefault(a.data, []).append(a)
    return result


def _grid_html(dias: list, por_dia: dict) -> str:
    html = ""
    for dia in dias:
        lista = por_dia.get(dia, [])
        if lista:
            a = lista[0]
            cor_btn = "blue-btn" if a.tipo() == "Remota" else ""
            local_curto = a.local if len(a.local) <= 14 else a.local[:12] + "…"
            mais = f"<div class='mais'>+{len(lista)-1} mais</div>" if len(lista) > 1 else ""
            # json.dumps garante escape correto mesmo com apóstrofos no título
            args = ", ".join([
                str(a.id),
                json.dumps(a.titulo),
                json.dumps(dia),
                json.dumps(a.horario),
                json.dumps(a.local),
                json.dumps(a.descricao),
            ])
            html += f"""
            <button class="day-cell" onclick="abrirModal(event,{args})">
                <div class="day-number">{dia}</div>
                <div class="event-card">
                    <div class="event-title">{a.titulo}</div>
                    <div class="event-info">🕐 {a.horario}</div>
                    <div class="event-info">📍 {local_curto}</div>
                    {mais}
                    <div class="btn-details {cor_btn}">Saiba mais</div>
                </div>
            </button>"""
        else:
            html += f"""
            <button class="day-cell empty" onclick="abrirModalVazio(event,'{dia}')">
                <div class="day-number">{dia}</div>
            </button>"""
    return html


def renderizar():
    usuario = get_usuario_atual()
    if usuario is None:
        st.warning("Por favor, faça login para acessar o calendário.")
        return

    mes = st.session_state.mes_atual
    ano = st.session_state.ano_atual
    nomes_mes = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    nome_mes = nomes_mes[mes - 1]

    _, num_dias = calendar.monthrange(ano, mes)
    dias = [f"{d:02d}/{mes:02d}" for d in range(1, num_dias + 1)]
    grid = _grid_html(dias, _atividades_por_dia())

    eh_senior = isinstance(usuario, Senior)
    eh_tutor  = isinstance(usuario, Tutor)

    params = st.query_params
    if "inscrever" in params and eh_senior:
        resultado = inscrever_senior(usuario.id, int(params["inscrever"]))
        params.clear()
        if resultado["sucesso"]:
            st.success(resultado["mensagem"])
        else:
            st.warning(resultado["mensagem"])
        st.rerun()

    codigo_interface = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',Tahoma,sans-serif;}}
  html,body{{background:transparent;}}

  /* ── Cabeçalho do mês ── */
  .cal-header{{background:#a78b8b;color:#3b2323;display:flex;justify-content:space-between;
    align-items:center;padding:14px 24px;border-radius:10px 10px 0 0;}}
  .cal-header h2{{font-size:1.8rem;font-weight:bold;}}
  .arrow-btn{{background:none;border:none;font-size:2rem;color:#3b2323;cursor:pointer;padding:0 10px;line-height:1;}}
  .arrow-btn:hover{{color:#000;}}

  /* ── Grid ── */
  .cal-box{{background:white;border:3px solid #7d4ba7;border-top:none;border-radius:0 0 10px 10px;overflow:hidden;}}
  .calendar-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;padding:12px;}}
  .weekday{{text-align:center;font-weight:700;color:#725353;font-size:.95rem;padding:6px 0;border-bottom:2px solid #e9e6e7;}}
  .day-cell{{background:#e9e6e7;min-height:130px;border-radius:7px;display:flex;flex-direction:column;
    padding:5px;border:2px solid transparent;cursor:pointer;text-align:left;width:100%;transition:all .15s;}}
  .day-cell:hover{{border-color:#7d4ba7;background:#e2dedf;transform:translateY(-2px);}}
  .day-cell.empty{{cursor:default;}}
  .day-cell.empty:hover{{transform:none;border-color:transparent;background:#e9e6e7;}}
  .day-number{{background:white;width:100%;text-align:center;font-size:.85rem;font-weight:700;color:#333;
    padding:2px 0;border-radius:4px;box-shadow:0 1px 2px rgba(0,0,0,.1);margin-bottom:5px;}}
  .event-card{{background:white;width:100%;border-radius:5px;padding:5px;box-shadow:0 2px 5px rgba(0,0,0,.07);
    display:flex;flex-direction:column;flex-grow:1;}}
  .event-title{{font-size:.85rem;font-weight:700;color:#4a3636;line-height:1.2;margin-bottom:2px;}}
  .event-info{{font-size:.75rem;color:#555;margin-bottom:2px;}}
  .mais{{font-size:.7rem;color:#888;margin-top:2px;}}
  .btn-details{{background:#a78b8b;color:white;border:none;border-radius:13px;font-size:.75rem;
    padding:4px 0;width:100%;margin-top:4px;font-weight:700;cursor:pointer;
    display:flex;align-items:center;justify-content:center;text-align:center;}}
  .btn-details.blue-btn{{background:#a0bcd3;color:#1a4263;}}

  /* ── Modal ── */
  .modal-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);
    display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;
    transition:opacity .2s;z-index:500;}}
  .modal-overlay.active{{opacity:1;pointer-events:auto;}}
  .modal-content{{background:white;padding:28px;border-radius:12px;width:90%;max-width:440px;
    box-shadow:0 10px 30px rgba(0,0,0,.3);border:3px solid #7d4ba7;text-align:center;}}
  .modal-title{{font-size:1.5rem;color:#1a4263;margin-bottom:12px;font-weight:700;}}
  .modal-text{{font-size:1rem;margin-bottom:7px;color:#444;}}
  .modal-actions{{margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap;}}
  .btn-modal{{padding:10px 20px;font-size:.95rem;font-weight:700;border-radius:20px;
    cursor:pointer;border:none;min-height:44px;}}
  .btn-participar{{background:#27ae60;color:white;}}
  .btn-participar:hover{{background:#219a52;}}
  .btn-fechar{{background:#e74c3c;color:white;}}
  .btn-fechar:hover{{background:#c0392b;}}

  @media(max-width:700px){{
    .calendar-grid{{gap:3px;padding:8px;}}
    .day-cell{{min-height:80px;padding:3px;}}
    .cal-header h2{{font-size:1.3rem;}}
  }}
</style>
</head>
<body>
  <div style="padding:12px 16px;">
    <div class="cal-box">
      <div class="calendar-grid">
        <div class="weekday">Dom</div><div class="weekday">Seg</div>
        <div class="weekday">Ter</div><div class="weekday">Qua</div>
        <div class="weekday">Qui</div><div class="weekday">Sex</div>
        <div class="weekday">Sáb</div>
        {grid}
      </div>
    </div>
  </div>

  <div class="modal-overlay" id="modalOverlay">
    <div class="modal-content">
      <h3 class="modal-title" id="mTitle"></h3>
      <p  class="modal-text"  id="mDate"></p>
      <p  class="modal-text"  id="mTime"></p>
      <p  class="modal-text"  id="mLocal"></p>
      <p  class="modal-text"  id="mDesc" style="font-size:.9rem;color:#666;"></p>
      <div class="modal-actions" id="mActions"></div>
    </div>
  </div>

<script>
  const ehSenior = {'true' if eh_senior else 'false'};
  const overlay = document.getElementById('modalOverlay');
  let _currentId = null;

  function abrirModal(e, id, titulo, data, horario, local, descricao) {{
    e.stopPropagation();
    _currentId = id;
    document.getElementById('mTitle').innerText = titulo;
    document.getElementById('mDate').innerText  = '📅 ' + data;
    document.getElementById('mTime').innerText  = '🕐 ' + horario;
    document.getElementById('mLocal').innerText = '📍 ' + local;
    document.getElementById('mDesc').innerText  = descricao || '';
    const btns = document.getElementById('mActions');
    if (ehSenior) {{
      btns.innerHTML =
        `<button class="btn-modal btn-participar" onclick="confirmarInscricao(${{id}})">✅ Quero Participar</button>
         <button class="btn-modal btn-fechar"    onclick="fecharModal()">Voltar</button>`;
    }} else {{
      btns.innerHTML = `<button class="btn-modal btn-fechar" onclick="fecharModal()">Fechar</button>`;
    }}
    overlay.classList.add('active');
  }}

  function abrirModalVazio(e, dia) {{
    e.stopPropagation();
    _currentId = null;
    document.getElementById('mTitle').innerText = 'Nenhuma atividade';
    document.getElementById('mDate').innerText  = '📅 ' + dia;
    document.getElementById('mTime').innerText  = 'Não há atividades neste dia.';
    document.getElementById('mLocal').innerText = '';
    document.getElementById('mDesc').innerText  = '';
    document.getElementById('mActions').innerHTML =
      `<button class="btn-modal btn-fechar" onclick="fecharModal()">Fechar</button>`;
    overlay.classList.add('active');
  }}

  function fecharModal() {{ overlay.classList.remove('active'); }}
  overlay.addEventListener('click', e => {{ if (e.target === overlay) fecharModal(); }});

  function confirmarInscricao(id) {{
    fecharModal();
    var base = window.parent.location.href.split('?')[0];
    window.parent.location.href = base + '?inscrever=' + id;
  }}
</script>
</body>
</html>"""

    header_left, header_center, header_right = st.columns([1, 3, 1])
    with header_left:
        if st.button("◀", use_container_width=True, key="btn_mes_anterior"):
            if mes == 1:
                st.session_state.mes_atual = 12
                st.session_state.ano_atual = ano - 1
            else:
                st.session_state.mes_atual -= 1
            st.rerun()

    with header_center:
        st.markdown(
            f"""
            <div style='text-align:center; font-size:1.4rem; font-weight:700; color:#3b2323; padding: 10px 0;'>
              {nome_mes} {ano}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_right:
        if st.button("▶", use_container_width=True, key="btn_mes_proximo"):
            if mes == 12:
                st.session_state.mes_atual = 1
                st.session_state.ano_atual = ano + 1
            else:
                st.session_state.mes_atual += 1
            st.rerun()

    # ── Renderiza o calendário HTML ──
    components.html(codigo_interface, height=720, scrolling=False)

    # ── Processa inscrição (sem query_params, via query param de inscrição) ──
    if eh_senior and "inscricao_id" in st.session_state:
        id_atividade = st.session_state.inscricao_id
        resultado = inscrever_senior(usuario.id, id_atividade)
        del st.session_state.inscricao_id
        if resultado["sucesso"]:
            st.success(resultado["mensagem"])
        else:
            st.warning(resultado["mensagem"])
        st.rerun()

    # ── Formulário de criação (Tutor) ──
    if eh_tutor and st.session_state.mostra_painel_tutor:
        st.divider()
        with st.form("form_criar_atividade", clear_on_submit=True):
            st.markdown("**➕ Nova Atividade**")
            c1, c2 = st.columns(2)
            with c1:
                titulo  = st.text_input("Título*")
                data    = st.text_input("Data (DD/MM)*", placeholder="Ex: 15/06")
                tipo    = st.radio("Tipo*", ["Presencial", "Remota"], horizontal=True)
            with c2:
                horario = st.text_input("Horário*", placeholder="Ex: 14:30")
                vagas   = st.number_input("Vagas", value=30, min_value=1, max_value=200)
                local   = st.text_input("Endereço / Link*")
            descricao = st.text_area("Descrição", height=60)

            c_salvar, c_cancelar = st.columns(2)
            with c_salvar:
                salvar = st.form_submit_button("💾 Salvar", use_container_width=True)
            with c_cancelar:
                cancelar = st.form_submit_button("✖ Cancelar", use_container_width=True)

            if cancelar:
                st.session_state.mostra_painel_tutor = False
                st.rerun()

            if salvar:
                if not all([titulo, data, horario, local]):
                    st.error("Preencha todos os campos obrigatórios (*)")
                else:
                    if tipo == "Remota":
                        nova = AtividadeRemota(
                            id=0, titulo=titulo, descricao=descricao, data=data,
                            horario=horario, tutor=usuario, local=local,
                            vagas=int(vagas), link=local
                        )
                    else:
                        nova = AtividadePresencial(
                            id=0, titulo=titulo, descricao=descricao, data=data,
                            horario=horario, tutor=usuario, local=local,
                            vagas=int(vagas), endereco=local
                        )
                    criar_atividade(nova)
                    st.session_state.mostra_painel_tutor = False
                    st.success(f"Atividade '{titulo}' criada com sucesso!")
                    st.rerun()

    # ── Formulário de inscrição (Sênior) ──
    if eh_senior:
        st.divider()
        todas = listar_atividades()
        if todas:
            with st.form("form_inscrever", clear_on_submit=True):
                st.markdown("**✍️ Inscrever-se em uma atividade**")
                escolha = st.selectbox(
                    "Escolha a atividade:",
                    todas,
                    format_func=lambda a: f"{a.titulo} — {a.data} às {a.horario} ({a.local})"
                )
                if st.form_submit_button("✅ Quero Participar", use_container_width=True):
                    resultado = inscrever_senior(usuario.id, escolha.id)
                    if resultado["sucesso"]:
                        st.success(resultado["mensagem"])
                        st.rerun()
                    else:
                        st.warning(resultado["mensagem"])
        else:
            st.info("Nenhuma atividade disponível no momento.")
