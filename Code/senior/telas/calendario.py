import streamlit as st
import calendar
from models.atividade import AtividadePresencial, AtividadeRemota
from models.usuario import Tutor, Senior
from services.atividade_service import (
    listar_atividades, criar_atividade,
    inscrever_senior, get_usuario_atual, deletar_atividade
)

# ══════════════════════════════════════════
# LÓGICA INTERNA DO MODAL
# ══════════════════════════════════════════
def conteudo_modal(atividade_id):
    usuario = get_usuario_atual()
    eh_senior = isinstance(usuario, Senior)
    eh_tutor = isinstance(usuario, Tutor)
    
    atividade = next((a for a in listar_atividades() if a.id == atividade_id), None)
    if not atividade:
        st.error("Atividade não encontrada.")
        return

    st.markdown(f"**Data:** {atividade.data}")
    st.markdown(f"**Horário:** {atividade.horario}")
    st.markdown(f"**Local:** {atividade.local}")
    tutor_nome = atividade.tutor.nome if atividade.tutor else "Não definido"
    st.markdown(f"**Tutor:** {tutor_nome}")
    
    if atividade.descricao:
        st.markdown(f"**Descrição:** {atividade.descricao}")
        
    vagas_restantes = atividade.vagas - len(atividade.inscritos)
    st.markdown(f"**Vagas disponíveis:** {vagas_restantes}")
    
    st.divider()

    if eh_senior:
        ja_inscrito = any(a.id == atividade.id for a in usuario.atividades_inscritas)
        if ja_inscrito:
            st.info("✅ Você já está inscrito nesta atividade.")
        else:
            if st.button("✅ Quero Participar", use_container_width=True):
                resultado = inscrever_senior(usuario.id, atividade.id)
                if resultado["sucesso"]:
                    st.session_state.flash_msg = resultado["mensagem"]
                else:
                    st.session_state.flash_msg_error = resultado["mensagem"]
                st.rerun()
                
    if eh_tutor:
        st.warning("Deseja deletar esta atividade? Isso removerá as inscrições de todos os alunos.")
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("Sim, Deletar", use_container_width=True, key="btn_sim_del"):
                if deletar_atividade(atividade.id):
                    st.session_state.flash_msg = f"Atividade '{atividade.titulo}' deletada com sucesso!"
                else:
                    st.session_state.flash_msg_error = "Erro ao deletar atividade."
                st.rerun()
        with col_nao:
            if st.button("Cancelar", use_container_width=True, key="btn_nao_del"):
                st.rerun()

dialog_decorator = getattr(st, "dialog", getattr(st, "experimental_dialog", None))

if dialog_decorator:
    @dialog_decorator("📌 Detalhes da Atividade")
    def modal_detalhes(atividade_id):
        conteudo_modal(atividade_id)
else:
    def modal_detalhes(atividade_id):
        with st.expander("📌 Detalhes da Atividade", expanded=True):
            conteudo_modal(atividade_id)

# ══════════════════════════════════════════
# RENDERIZAÇÃO PRINCIPAL DO CALENDÁRIO
# ══════════════════════════════════════════
def renderizar():
    usuario = get_usuario_atual()
    if not usuario:
        st.warning("Faça login para acessar o calendário.")
        return

    if "flash_msg" in st.session_state:
        st.success(st.session_state.flash_msg)
        del st.session_state.flash_msg
    if "flash_msg_error" in st.session_state:
        st.warning(st.session_state.flash_msg_error)
        del st.session_state.flash_msg_error

    # --- CSS CORRIGIDO PARA A GRADE E BOTÕES ---
    st.markdown("""
    <style>
        /* Ajuste das colunas para remover espaços laterais em excesso */
        div[data-testid="column"] {
            padding: 0 4px !important;
        }
        /* Estilo base dos blocos do calendário */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white !important;
            border-radius: 8px !important;
            padding: 8px !important;
            border: 2px solid #e9e6e7 !important;
        }
        /* Efeito visual ao passar o mouse no dia */
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #7d4ba7 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.06) !important;
        }
        /* Esconde barra de rolagem se houver muito texto */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            overflow: hidden !important; 
        }
        /* Regra de ALTA ESPECIFICIDADE para o botão 'Saiba mais' vencer o css global do app.py */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] button {
            min-height: 32px !important;
            height: 32px !important;
            padding: 0 10px !important;
            font-size: 0.8rem !important;
            background-color: #f4f6f9 !important;
            color: #1a4263 !important;
            border: 1px solid #d0d7de !important;
            border-radius: 6px !important;
            margin-top: 10px !important; /* Espaço limpo e sem sobreposição */
            width: 100% !important;
            box-shadow: none !important;
            line-height: 1 !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] button:hover {
            background-color: #a0bcd3 !important;
            border-color: #1a4263 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    mes = st.session_state.mes_atual
    ano = st.session_state.ano_atual
    nomes_mes = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    nome_mes = nomes_mes[mes-1]

    eh_senior = isinstance(usuario, Senior)
    eh_tutor = isinstance(usuario, Tutor)

    # 1. Navegação de Meses
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_left:
        if st.button("◀", use_container_width=True):
            if mes == 1:
                st.session_state.mes_atual = 12
                st.session_state.ano_atual = ano - 1
            else:
                st.session_state.mes_atual -= 1
            st.rerun()
    with col_center:
        st.markdown(f"<div style='text-align:center; font-size:1.4rem; font-weight:700; color:#1a4263; padding:10px 0;'>{nome_mes} {ano}</div>", unsafe_allow_html=True)
    with col_right:
        if st.button("▶", use_container_width=True):
            if mes == 12:
                st.session_state.mes_atual = 1
                st.session_state.ano_atual = ano + 1
            else:
                st.session_state.mes_atual += 1
            st.rerun()

    # Espaçador para afastar os dias da semana dos botões de navegação
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # 2. Dados do Mês
    atividades_por_dia = {}
    for a in listar_atividades():
        try:
            d, m = a.data.split("/") 
            if int(m) == mes:
                atividades_por_dia.setdefault(int(d), []).append(a)
        except:
            pass

    cal = calendar.Calendar(firstweekday=6) # 6 = Domingo
    semanas = cal.monthdayscalendar(ano, mes)

    # 3. Cabeçalho dos dias da semana
    dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    cols_header = st.columns(7)
    for i, col in enumerate(cols_header):
        with col:
            st.markdown(f"""
            <div style='
                text-align:center; 
                font-weight:700; 
                color:#725353; 
                font-size:0.95rem; 
                background-color:#e9e6e7; 
                padding:8px 0; 
                border-radius:6px;
                border-bottom: 3px solid #d5d1d2;
                margin-bottom: 10px;
            '>{dias_semana[i]}</div>
            """, unsafe_allow_html=True)

    # 4. Grade do Calendário (Com altura ampliada para 230px para acomodar tudo com sobra)
    for semana in semanas:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            with cols[i]:
                if dia != 0:
                    with st.container(height=230, border=True):
                        st.markdown(f"<div style='text-align:right; font-weight:700; color:#333; font-size:0.9rem; margin-bottom:4px;'>{dia}</div>", unsafe_allow_html=True)
                        
                        lista = atividades_por_dia.get(dia, [])
                        if lista:
                            a = lista[0]
                            cor = "🔵" if a.tipo() == "Remota" else "📍"
                            
                            st.markdown(f"""
                            <div style='background:#f4f6f9; padding:8px; border-radius:6px; border-left:4px solid #7d4ba7; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                                <div style='font-size:0.75rem; font-weight:bold; color:#1a4263; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{a.titulo}</div>
                                <div style='font-size:0.7rem; color:#555; margin-top:4px;'>{cor} {a.horario}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if len(lista) > 1:
                                st.markdown(f"<div style='font-size:0.65rem; color:#888; text-align:center; padding-top:4px;'>+{len(lista)-1} mais</div>", unsafe_allow_html=True)
                            
                            if st.button("Saiba mais", key=f"mod_{mes}_{dia}_{a.id}", use_container_width=True):
                                modal_detalhes(a.id)
                else:
                    with st.container(height=230, border=True):
                        st.markdown("<div style='text-align:center; color:#ccc; margin-top:60px; font-size:1.5rem;'>-</div>", unsafe_allow_html=True)

    # Painel de criação de atividade (Tutor)
    if eh_tutor and st.session_state.mostra_painel_tutor:
        st.divider()
        with st.form("form_criar_atividade", clear_on_submit=True):
            st.markdown("**➕ Nova Atividade**")
            c1, c2 = st.columns(2)
            with c1:
                titulo = st.text_input("Título*")
                data = st.text_input("Data (DD/MM)*", placeholder="Ex: 15/06")
                tipo = st.radio("Tipo*", ["Presencial", "Remota"], horizontal=True)
            with c2:
                horario = st.text_input("Horário*", placeholder="Ex: 14:30")
                vagas = st.number_input("Vagas", value=30, min_value=1, max_value=200)
                local = st.text_input("Endereço / Link*")
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
                    st.error("Preencha todos os campos obrigatórios.")
                else:
                    if tipo == "Remota":
                        nova = AtividadeRemota(id=0, titulo=titulo, descricao=descricao, data=data,
                                               horario=horario, tutor=usuario, local=local,
                                               vagas=int(vagas), link=local)
                    else:
                        nova = AtividadePresencial(id=0, titulo=titulo, descricao=descricao, data=data,
                                                   horario=horario, tutor=usuario, local=local,
                                                   vagas=int(vagas), endereco=local)
                    criar_atividade(nova)
                    st.session_state.mostra_painel_tutor = False
                    st.session_state.flash_msg = f"Atividade '{titulo}' criada com sucesso!"
                    st.rerun()

    # Formulário de inscrição rápida (Sênior)
    if eh_senior:
        st.divider()
        todas = listar_atividades()
        if todas:
            with st.form("form_inscrever", clear_on_submit=True):
                st.markdown("**✍️ Inscrever-se em uma atividade**")
                escolha = st.selectbox("Escolha a atividade:", todas,
                                       format_func=lambda a: f"{a.titulo} — {a.data} às {a.horario} ({a.local})")
                if st.form_submit_button("✅ Quero Participar", use_container_width=True):
                    resultado = inscrever_senior(usuario.id, escolha.id)
                    if resultado["sucesso"]:
                        st.session_state.flash_msg = resultado["mensagem"]
                    else:
                        st.session_state.flash_msg_error = resultado["mensagem"]
                    st.rerun()
        else:
            st.info("Nenhuma atividade disponível.")