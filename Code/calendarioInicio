import streamlit as st
import streamlit.components.v1 as components
from abc import ABC, abstractmethod
from typing import Dict, Optional

st.set_page_config(layout="wide", page_title="Comunidade 65+ - Calendário")


class Atividade(ABC):
    """Classe base que representa a entidade Atividade do sistema."""
    def __init__(self, titulo: str, horario: str, local: str, estilo: str = ""):
        self.titulo = titulo
        self.horario = horario
        self.local = local
        self.estilo = estilo

    @abstractmethod
    def obter_classe_estilo(self) -> str:
        """Retorna a classe CSS correspondente para acessibilidade e design."""
        pass


class AtividadePresencial(Atividade):
    """Representa atividades em locais físicos (Ex: Pilates no Parque)."""
    def obter_classe_estilo(self) -> str:
        return "btn-details"


class AtividadeRemota(Atividade):
    """Representa rodas de conversa ou aulas online ao vivo (RF05)."""
    def obter_classe_estilo(self) -> str:
        return "btn-details blue-btn"

#mricroserviços

class AtividadeRepository:
    """Gerencia o estado e persistência em memória das atividades (st.session_state)."""
    
    @staticmethod
    def inicializar_banco_dados():
        """Garante a persistência inicial simulando os dados da Desk Research."""
        if "atividades" not in st.session_state:
            st.session_state.atividades = {
                "01/06": AtividadeRemota("Roda de Conversa", "13h30", "Sala Comunitária Virtual"),
                "04/06": AtividadePresencial("Aula Pilates", "13h30", "Parque Central"),
                "08/06": AtividadeRemota("Aula Yoga", "07h30", "Plataforma Online (Ao vivo)"),
                "18/06": AtividadePresencial("Aula Pilates", "13h30", "Parque Central"),
                "02/07": AtividadePresencial("Aula Pilates", "13h30", "Parque Central")
            }
        if "mostrar_formulario" not in st.session_state:
            st.session_state.mostrar_formulario = False

    def listar_todas(self) -> Dict[str, Atividade]:
        return st.session_state.atividades

    def buscar_por_dia(self, dia: str) -> Optional[Atividade]:
        return st.session_state.atividades.get(dia)

    def salvar(self, dia: str, atividade: Atividade):
        st.session_state.atividades[dia] = atividade


# ==============================================================================
# vizualização

class CalendarioHTMLBuilder:
    """Responsável por isolar toda a montagem de strings HTML e CSS injetados."""
    
    def __init__(self, dias_calendario: list, repositorio: AtividadeRepository):
        self.dias_calendario = dias_calendario
        self.repositorio = repositorio

    def construir_grid_items(self) -> str:
        html_items = ""
        for dia in self.dias_calendario:
            atividade = self.repositorio.buscar_por_dia(dia)
            
            if atividade:
                classe_botao = atividade.obter_classe_estilo()
                # RNF01 - Evita que quebras de layout confundam usuários 65+
                local_exibicao = atividade.local if len(atividade.local) <= 14 else atividade.local[:12] + "..."
                
                html_items += f"""
                <button class="day-cell">
                    <div class="day-number">{dia}</div>
                    <div class="event-card">
                        <div class="event-title">{atividade.titulo}</div>
                        <div class="event-info"> {atividade.horario}</div>
                        <div class="event-info"> {local_exibicao}</div>
                        <div class="{classe_botao}" onclick="abrirModal(event, '{atividade.titulo}', '{dia}', '{atividade.horario}', '{atividade.local}')">Saiba mais →</div>
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
        """String contendo toda a estrutura de estilos e scripts injetados."""
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
                .day-number {{ background-color: white; width: 100%; text-align: center; font-size: 0.95rem; font-weight: bold; color: #333; padding: 4px 0; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 8px; }}
                .event-card {{ background-color: white; width: 100%; border-radius: 6px; padding: 8px; box-shadow: 0 3px 6px rgba(0,0,0,0.08); display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }}
                .event-title {{ font-size: 1rem; font-weight: bold; color: #4a3636; line-height: 1.2; margin-bottom: 4px; }}
                .event-info {{ font-size: 0.85rem; color: #555; display: flex; align-items: center; gap: 4px; margin-bottom: 2px; }}
                .btn-details {{ background-color: #a78b8b; color: white; border: none; border-radius: 20px; font-size: 0.85rem; padding: 6px 0; width: 100%; margin-top: 6px; font-weight: bold; text-align: center; }}
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
            </style>
        </head>
        <body>
            <header class="navbar">
                <div class="nav-left"><div class="logo"></div>
                    <nav class="nav-links">
                        <a href="#" class="nav-item active">Calendário</a>
                        <a href="#" class="nav-item">Mural Avisos</a>
                        <a href="#" class="nav-item">Atividades</a>
                        <a href="#" class="nav-item">Ajuda</a>
                    </nav>
                </div>
                <button class="profile-menu">Olá, Sênior ∨</button>
            </header>
            <main class="desktop-container">
                <div class="app-container">
                    <div class="calendar-header">
                        <button class="arrow-btn" aria-label="Mês anterior">&lt;</button>
                        <h2>Junho</h2>
                        <button class="arrow-btn" aria-label="Próximo mês">&gt;</button>
                    </div>
                    <div class="calendar-grid">
                        <div class="weekday">Domingo</div><div class="weekday">Segunda</div><div class="weekday">Terça</div>
                        <div class="weekday">Quarta</div><div class="weekday">Quinta</div><div class="weekday">Sexta</div>
                        <div class="weekday">Sábado</div>
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

                function abrirModal(e, title, day, time, local) {{
                    e.stopPropagation();
                    mTitle.innerText = title;
                    mDate.innerText = ` Dia: ${{day}}`;
                    mTime.innerText = ` Horário: ${{time}}`;
                    mLocal.innerText = ` Local: ${{local}}`;
                    mActions.innerHTML = `
                        <button class="btn-modal btn-participar" onclick="confirmarInscricao()">Quero Participar</button>
                        <button class="btn-modal btn-fechar" onclick="fecharModal()">Voltar</button>
                    `;
                    overlay.classList.add('active');
                }}

                document.querySelectorAll('.day-cell.empty').forEach(cell => {{
                    cell.addEventListener('click', () => {{
                        const day = cell.getAttribute('data-day');
                        mTitle.innerText = "Nenhuma atividade";
                        mDate.innerText = `Dia: ${{day}}`;
                        mTime.innerText = "Não hay atividades agendadas para este dia.";
                        mLocal.innerText = "";
                        mActions.innerHTML = `<button class="btn-modal btn-fechar" onclick="fecharModal()">Voltar</button>`;
                        overlay.classList.add('active');
                    }});
                }});

                function fecharModal() {{ overlay.classList.remove('active'); }}
                function confirmarInscricao() {{ alert("Inscrição realizada com sucesso!"); fecharModal(); }}
                overlay.addEventListener('click', (e) => {{ if(e.target === overlay) fecharModal(); }});
            </script>
        </body>
        </html>
        """
        components.html(codigo_interface, height=980, scrolling=True)


# ====================================================================================

# Definição estática dos dias mapeados na iteração do grid
DIAS_DO_CALENDARIO = [
    "31/05", "01/06", "02/06", "03/06", "04/06", "05/06", "06/06", "07/06", "08/06", "09/06", "10/06",
    "11/06", "12/06", "13/06", "14/06", "15/06", "16/06", "17/06", "18/06", "19/06", "20/06", "21/06",
    "22/06", "23/06", "24/06", "25/06", "26/06", "27/06", "28/06", "29/06", "30/06", "01/07", "02/07",
    "03/07", "04/07"
]

# Estilização explícita do Streamlit nativo para botões de controle
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 24px !important;
            background-color: #7d4ba7 !important;
            color: white !important;
            border: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            transition: transform 0.2s !important;
        }
        .stButton > button:hover {
            transform: scale(1.1) !important;
            background-color: #663d8b !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializa o repositório fictício de dados
AtividadeRepository.inicializar_banco_dados()
repo = AtividadeRepository()

# Área de Cabeçalho Superior - Interações e Ações do Tutor
col1, col2 = st.columns([1, 11])
with col1:
    if st.button("＋", help="Adicionar novo evento"):
        st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario

# Exibição Condicional do Formulário de Criação (Padrão MVC/Service)
if st.session_state.mostrar_formulario:
    with st.form("novo_evento_direto", clear_on_submit=True):
        st.markdown("### Novo Evento (Painel do Tutor)")
        c1, c2, c3, c4 = st.columns([2, 4, 2, 4])
        
        with c1:
            dia_sel = st.selectbox("Dia:", DIAS_DO_CALENDARIO)
        with c2:
            tit = st.text_input("Atividade:", placeholder="Ex: Oficina de Pintura")
        with c3:
            hr = st.text_input("Horário:", placeholder="Ex: 14h00")
        with c4:
            loc = st.text_input("Local / Link:", placeholder="Ex: Sala Comunitária ou Link Zoom")
            
        tipo_cadastro = st.radio("Ambiente:", ["Presencial", "Remota ao Vivo"], horizontal=True)
        
        if st.form_submit_button("Salvar Evento"):
            if tit and hr and loc:
                # Polimorfismo na criação das instâncias
                nova_ativ = AtividadeRemota(tit, hr, loc) if tipo_cadastro == "Remota ao Vivo" else AtividadePresencial(tit, hr, loc)
                repo.salvar(dia_sel, nova_ativ)
                st.session_state.mostrar_formulario = False
                st.rerun()
            else:
                st.error("Preencha todos os campos!")

# Instanciação da View e exibição final do Calendário
view_calendario = CalendarioHTMLBuilder(DIAS_DO_CALENDARIO, repo)
grid_gerado = view_calendario.construir_grid_items()
view_calendario.renderizar_template_completo(grid_gerado)
