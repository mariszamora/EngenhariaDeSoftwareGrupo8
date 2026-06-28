# pages/calendario.py - DO ZERO
import streamlit as st
import streamlit.components.v1 as components
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Tutor, Senior
from services.atividade_service import (
    listar_atividades,
    criar_atividade,
    inscrever_senior,
    get_usuario_atual
)
from datetime import datetime
import calendar


def obter_atividades_por_dia():
    atividades = {}
    for atividade in listar_atividades():
        data = atividade.data
        if data not in atividades:
            atividades[data] = []
        atividades[data].append(atividade)
    return atividades

def get_mes_atual():
    if "mes_atual" not in st.session_state:
        agora = datetime.now()
        st.session_state.mes_atual = agora.month
        st.session_state.ano_atual = agora.year
    return st.session_state.mes_atual, st.session_state.ano_atual




class CalendarioHTMLBuilder:
    def __init__(self, dias_calendario, atividades_por_dia, mes, ano, usuario):
        self.dias_calendario = dias_calendario
        self.atividades_por_dia = atividades_por_dia
        self.mes = mes
        self.ano = ano
        self.usuario = usuario
    
    def construir_grid_items(self) -> str:
        html_items = ""
        
        for dia in self.dias_calendario:
            lista = self.atividades_por_dia.get(dia, [])
            
            if lista:
                atividade = lista[0]
                
                if atividade.tipo() == "Remota":
                    classe_botao = "btn-details blue-btn"
                else:
                    classe_botao = "btn-details"
                
                local_exibicao = atividade.local if len(atividade.local) <= 14 else atividade.local[:12] + "..."
                
                mais_atividades = ""
                if len(lista) > 1:
                    mais_atividades = f"<div style='font-size:0.7rem;color:#888;margin-top:2px;'>+{len(lista)-1} mais</div>"
                
                html_items += f"""
                <button class="day-cell" data-day="{dia}">
                    <div class="day-number">{dia}</div>
                    <div class="event-card">
                        <div class="event-title">{atividade.titulo}</div>
                        <div class="event-info"> {atividade.horario}</div>
                        <div class="event-info"> {local_exibicao}</div>
                        {mais_atividades}
                        <div class="{classe_botao}" onclick="abrirModal(event, '{atividade.titulo}', '{dia}', '{atividade.horario}', '{atividade.local}', {atividade.id})">Saiba mais</div>
                    </div>
                </button>
                """
            else:
                html_items += f"""
                <button class="day-cell empty" data-day="{dia}">
                    <div class="day-number">{dia}</div>
                </button>
                """
        
        return html_items

    def renderizar_template_completo(self, html_grid_items: str):
        meses = ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", 
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        nome_mes = meses[self.mes - 1]

        codigo_interface = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                body {{ background-color: #f3f1f2; color: #333; display: flex; flex-direction: column; }}
                .navbar {{ background-color: #bcd0e3; padding: 15px 40px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .nav-left {{ display: flex; align-items: center; gap: 20px; }}
                .logo {{ width: 45px; height: 45px; background: linear-gradient(45deg, #f39c12, #9b59b6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold; }}
                .nav-links {{ display: flex; gap: 15px; }}
                .nav-item {{ text-decoration: none; color: #1a4263; font-weight: 600; font-size: 1.1rem; padding: 8px 15px; border-radius: 25px; }}
                .nav-item.active {{ background-color: #1a4263; color: white; }}
                .profile-menu {{ border: 2px solid #1a4263; padding: 8px 18px; border-radius: 20px; font-size: 1rem; color: #1a4263; background: none; cursor: pointer; font-weight: bold; }}
                .desktop-container {{ flex: 1; padding: 10px 0px; display: flex; justify-content: center; }}
                .app-container {{ width: 100%; background-color: white; border: 4px solid #7d4ba7; border-radius: 12px; overflow: hidden; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
                .calendar-header {{ background-color: #a78b8b; color: #3b2323; display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; }}
                .calendar-header h2 {{ font-size: 2.2rem; font-weight: bold; }}
                .arrow-btn {{ background: none; border: none; font-size: 2rem; color: #3b2323; cursor: pointer; padding: 0 15px; }}
                .calendar-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; padding: 20px; }}
                .weekday {{ text-align: center; font-weight: bold; color: #725353; font-size: 1.1rem; padding: 10px 0; border-bottom: 2px solid #e9e6e7; }}
                .day-cell {{ background-color: #e9e6e7; min-height: 160px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; padding: 8px; border: 2px solid transparent; cursor: pointer; text-align: left; width: 100%; transition: all 0.2s ease-in-out; }}
                .day-cell:hover {{ border-color: #7d4ba7; background-color: #e2dedf; transform: translateY(-2px); }}
                .day-cell.empty {{ cursor: default; }}
                .day-cell.empty:hover {{ transform: none; border-color: transparent; background-color: #e9e6e7; }}
                .day-number {{ background-color: white; width: 100%; text-align: center; font-size: 0.95rem; font-weight: bold; color: #333; padding: 4px 0; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 8px; }}
                .event-card {{ background-color: white; width: 100%; border-radius: 6px; padding: 8px; box-shadow: 0 3px 6px rgba(0,0,0,0.08); display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }}
                .event-title {{ font-size: 1rem; font-weight: bold; color: #4a3636; line-height: 1.2; margin-bottom: 4px; }}
                .event-info {{ font-size: 0.85rem; color: #555; display: flex; align-items: center; gap: 4px; margin-bottom: 2px; }}
                .btn-details {{ background-color: #a78b8b; color: white; border: none; border-radius: 20px; font-size: 0.85rem; padding: 6px 0; width: 100%; margin-top: 6px; font-weight: bold; text-align: center; cursor: pointer; }}
                .btn-details.blue-btn {{ background-color: #a0bcd3; color: #1a4263; }}
                .modal-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; z-index: 1000; }}
                .modal-overlay.active {{ opacity: 1; pointer-events: auto; }}
                .modal-content {{ background-color: white; padding: 35px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 3px solid #7d4ba7; text-align: center; }}
                .modal-title {{ font-size: 1.8rem; color: #1a4263; margin-bottom: 15px; }}
                .modal-text {{ font-size: 1.2rem; margin-bottom: 10px; color: #444; }}
                .modal-actions {{ margin-top: 25px; display: flex; gap: 15px; justify-content: center; }}
                .btn-modal {{ padding: 12px 25px; font-size: 1.1rem; font-weight: bold; border-radius: 25px; cursor: pointer; border: none; min-height: 48px; }}
                .btn-participar {{ background-color: #27ae60; color: white; }}
                .btn-fechar {{ background-color: #e74c3c; color: white; }}
                @media (max-width: 768px) {{
                    .calendar-grid {{ gap: 4px; padding: 10px; }}
                    .day-cell {{ min-height: 100px; padding: 4px; }}
                    .event-title {{ font-size: 0.85rem; }}
                    .calendar-header h2 {{ font-size: 1.5rem; }}
                    .navbar {{ padding: 10px 15px; flex-wrap: wrap; }}
                    .nav-links {{ gap: 5px; }}
                    .nav-item {{ font-size: 0.9rem; padding: 5px 10px; }}
                }}
            </style>
        </head>
        <body>
            <header class="navbar">
                <div class="nav-left"><div class="logo">65+</div>
                    <nav class="nav-links">
                        <a href="?pagina=Calendario" class="nav-item active">Calendario</a>
                        <a href="?pagina=Atividades" class="nav-item">Atividades</a>
                        <a href="#" class="nav-item">Mural Avisos</a>
                        <a href="#" class="nav-item">Ajuda</a>
                    </nav>
                </div>
                <button class="profile-menu">Ola, Senior</button>
            </header>
            <main class="desktop-container">
                <div class="app-container">
                    <div class="calendar-header" style="justify-content: center;">
                        <h2>{nome_mes} {self.ano}</h2>
                    </div>
                    <div class="calendar-grid">
                        <div class="weekday">Domingo</div>
                        <div class="weekday">Segunda</div>
                        <div class="weekday">Terca</div>
                        <div class="weekday">Quarta</div>
                        <div class="weekday">Quinta</div>
                        <div class="weekday">Sexta</div>
                        <div class="weekday">Sabado</div>
                        {html_grid_items}
                    </div>
                </div>
            </main>
            <div class="modal-overlay" id="modalOverlay">
                <div class="modal-content">
                    <h3 class="modal-title" id="modalTitle">Detalhes</h3>
                    <p class="modal-text" id="modalDate"></p>
                    <p class="modal-text" id="modalTime"></p>
                    <p class="modal-text" id="modalLocal"></p>
                    <div class="modal-actions" id="modalActions"></div>
                </div>
            </div>
            <script>
                const overlay = document.getElementById('modalOverlay');
                const mTitle = document.getElementById('modalTitle');
                const mDate = document.getElementById('modalDate');
                const mTime = document.getElementById('modalTime');
                const mLocal = document.getElementById('modalLocal');
                const mActions = document.getElementById('modalActions');
                let currentActivityId = null;

                function abrirModal(e, title, day, time, local, activityId) {{
                    e.stopPropagation();
                    currentActivityId = activityId;
                    mTitle.innerText = title;
                    mDate.innerText = ` Dia: ${{day}}`;
                    mTime.innerText = ` Horario: ${{time}}`;
                    mLocal.innerText = ` Local: ${{local}}`;
                    
                    mActions.innerHTML = `
                        <button class="btn-modal btn-fechar" onclick="fecharModal()">Voltar</button>
                    `;
                    overlay.classList.add('active');
                }}

                document.querySelectorAll('.day-cell.empty').forEach(cell => {{
                    cell.addEventListener('click', () => {{
                        const day = cell.getAttribute('data-day');
                        mTitle.innerText = "Nenhuma atividade";
                        mDate.innerText = `Dia: ${{day}}`;
                        mTime.innerText = "Nao ha atividades agendadas para este dia.";
                        mLocal.innerText = "";
                        mActions.innerHTML = `<button class="btn-modal btn-fechar" onclick="fecharModal()">Voltar</button>`;
                        overlay.classList.add('active');
                    }});
                }});

                function fecharModal() {{ overlay.classList.remove('active'); }}

                overlay.addEventListener('click', (e) => {{ if(e.target === overlay) fecharModal(); }});
            </script>
        </body>
        </html>
        """
        components.html(codigo_interface, height=980, scrolling=True)


# ==========================================
# FUNCAO PRINCIPAL - RENDERIZAR
# ==========================================

def renderizar():
    """Renderiza a pagina do calendario"""
    
    usuario = get_usuario_atual()
    
    if usuario is None:
        st.warning("Por favor, faca login para acessar o calendario.")
        return

    st.title("Calendario de Atividades")
    
    mes, ano = get_mes_atual()

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("◀ Mes anterior", use_container_width=True):
            if mes == 1:
                st.session_state.mes_atual = 12
                st.session_state.ano_atual -= 1
            else:
                st.session_state.mes_atual -= 1
            st.rerun()
    
    with col2:
        meses = ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", 
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        st.markdown(f"<h2 style='text-align: center;'>{meses[mes-1]} {ano}</h2>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Proximo mes ▶", use_container_width=True):
            if mes == 12:
                st.session_state.mes_atual = 1
                st.session_state.ano_atual += 1
            else:
                st.session_state.mes_atual += 1
            st.rerun()
    

    if isinstance(usuario, Tutor):
        st.divider()
        st.subheader(" Painel do Tutor")
        
        with st.expander("➕ Criar nova atividade", expanded=False):
            with st.form("form_nova_atividade", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    titulo = st.text_input("Titulo da atividade*", placeholder="Ex: Aula de Yoga")
                    data = st.text_input("Data (DD/MM)*", placeholder="Ex: 15/06")
                    horario = st.text_input("Horario*", placeholder="Ex: 14:30")
                
                with col2:
                    tipo = st.radio("Tipo*", ["Presencial", "Remota"], horizontal=True)
                    
                    if tipo == "Presencial":
                        local = st.text_input("Endereco*", placeholder="Ex: Rua das Flores, 123")
                    else:
                        local = st.text_input("Link da aula*", placeholder="Ex: https://meet.google.com/...")
                    
                    vagas = st.number_input("Numero de vagas", min_value=1, max_value=100, value=30)
                
                descricao = st.text_area("Descricao (opcional)", placeholder="Descreva a atividade...")
                
                if st.form_submit_button(" Salvar Atividade", use_container_width=True):
                    if titulo and data and horario and local:
                        try:
                            if tipo == "Remota":
                                nova_atividade = AtividadeRemota(
                                    id=0,
                                    titulo=titulo,
                                    descricao=descricao,
                                    data=data,
                                    horario=horario,
                                    tutor=usuario,
                                    local=local,
                                    vagas=vagas,
                                    link=local
                                )
                            else:
                                nova_atividade = AtividadePresencial(
                                    id=0,
                                    titulo=titulo,
                                    descricao=descricao,
                                    data=data,
                                    horario=horario,
                                    tutor=usuario,
                                    local=local,
                                    vagas=vagas,
                                    endereco=local
                                )
                            
                            criar_atividade(nova_atividade)
                            st.success("Atividade criada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao criar atividade: {str(e)}")
                    else:
                        st.warning("Preencha todos os campos com *")
    
    # ==========================================
    # CRIA O CALENDARIO
    # ==========================================
    _, num_dias = calendar.monthrange(ano, mes)
    DIAS_DO_CALENDARIO = [f"{dia:02d}/{mes:02d}" for dia in range(1, num_dias + 1)]
    
    atividades_por_dia = obter_atividades_por_dia()
    
    view_calendario = CalendarioHTMLBuilder(
        DIAS_DO_CALENDARIO, 
        atividades_por_dia, 
        mes, 
        ano,
        usuario
    )
    
    grid_gerado = view_calendario.construir_grid_items()
    view_calendario.renderizar_template_completo(grid_gerado)

    if isinstance(usuario, Senior):
        st.divider()
        st.subheader("✍️ Inscrever-se em uma atividade")

        todas = listar_atividades()
        if not todas:
            st.info("Nenhuma atividade disponivel no momento.")
        else:
            opcoes = {
                f"{a.titulo} — {a.data} as {a.horario} ({a.local})": a.id
                for a in todas
            }
            escolha = st.selectbox("Escolha a atividade:", list(opcoes.keys()))

            if st.button("Quero participar", use_container_width=True):
                resultado = inscrever_senior(usuario.id, opcoes[escolha])
                if resultado["sucesso"]:
                    st.success(resultado["mensagem"])
                else:
                    st.warning(resultado["mensagem"])