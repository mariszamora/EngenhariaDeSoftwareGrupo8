# pages/pageatividades.py - AGORA SO CHAMA O SERVICE
# pages/pageatividades.py - INICIO CORRIGIDO
import streamlit as st
import streamlit.components.v1 as components
from models.usuario import Senior
from services.atividade_service import get_usuario_atual, listar_atividades_do_senior

def renderizar():
    """Renderiza a pagina de atividades do senior"""
    
    usuario = get_usuario_atual()
    
    if usuario is None:
        st.warning("Por favor, faca login para acessar as atividades.")
        return
    
    if not isinstance(usuario, Senior):
        st.warning("Esta pagina e apenas para Seniores.")
        return
    
    # <-- CHAMA O SERVICE PARA LISTAR
    atividades_inscrito = listar_atividades_do_senior(usuario.id)
    
    st.title("Minhas Atividades")
    st.caption(f"Voce esta inscrito em {len(atividades_inscrito)} atividades")
    
    if not atividades_inscrito:
        st.info("Voce ainda nao se inscreveu em nenhuma atividade. Va ao Calendario para se inscrever!")
        return
    
    # ==========================================
    # CONSTRUI OS CARDS DE ATIVIDADES
    # ==========================================
    cards_html = ""
    
    for atividade in atividades_inscrito:
        if atividade.tipo() == "Remota":
            icone = "💻"
            cor_fundo = "#aa9393"
        else:
            icone = "📍"
            cor_fundo = "#8a7a7a"
        
        nome_tutor = atividade.tutor.nome if atividade.tutor else "Nao definido"
        
        cards_html += f"""
        <div class="card" style="background-color: {cor_fundo};">
            <div class="video-thumbnail">
                <div class="play-button">
                    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                </div>
                <div class="tipo-badge">{icone} {atividade.tipo()}</div>
            </div>
            <div class="card-content">
                <h2 class="card-title">{atividade.titulo}</h2>
                <div class="tutor-info">
                    <div class="avatar-placeholder">👤</div>
                    <span>Tutor(a) {nome_tutor}</span>
                </div>
                <div class="post-time">
                    <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
                    Data: {atividade.data} as {atividade.horario}
                </div>
                <div class="post-time">
                    📍 {atividade.local}
                </div>
            </div>
        </div>
        """
    
    html_completo = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Atividades - Comunidade 65+</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}

            body {{
                background-color: #d2e1eb;
                color: #3e3330;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                padding-bottom: 40px;
            }}

            header {{
                width: 100%;
                background-color: #bcd0e0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}

            .logo-area {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .logo-placeholder {{
                width: 45px;
                height: 45px;
                background: linear-gradient(45deg, #f39c12, #9b59b6);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 20px;
            }}

            nav {{
                display: flex;
                align-items: center;
                gap: 30px;
            }}

            nav a {{
                text-decoration: none;
                color: #2c5270;
                font-weight: 600;
                font-size: 16px;
                transition: color 0.2s;
                cursor: pointer;
            }}

            nav a:hover {{
                color: #1a3347;
            }}

            nav a.active {{
                background-color: #215c84;
                color: white;
                padding: 8px 18px;
                border-radius: 20px;
            }}

            .user-menu {{
                border: 1.5px solid #2c5270;
                padding: 8px 18px;
                border-radius: 20px;
                color: #2c5270;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 5px;
            }}

            main {{
                width: 100%;
                max-width: 850px;
                margin-top: 30px;
                padding: 0 20px;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}

            .card {{
                border-radius: 15px;
                padding: 20px;
                display: flex;
                gap: 25px;
                align-items: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}

            .video-thumbnail {{
                width: 240px;
                height: 140px;
                background-color: #7d6b6b;
                border-radius: 8px;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                flex-shrink: 0;
            }}

            .video-thumbnail::before {{
                content: "🎬";
                color: rgba(255,255,255,0.6);
                font-size: 40px;
            }}

            .play-button {{
                position: absolute;
                width: 50px;
                height: 50px;
                border: 2px solid #ffffff;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(0, 0, 0, 0.2);
            }}

            .play-button svg {{
                fill: white;
                width: 20px;
                height: 20px;
                margin-left: 3px;
            }}
            
            .tipo-badge {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.6);
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }}

            .card-content {{
                display: flex;
                flex-direction: column;
                gap: 12px;
                color: #362521;
                flex: 1;
            }}

            .card-title {{
                font-size: 24px;
                font-weight: 700;
                font-family: 'Georgia', serif;
                color: white;
            }}

            .tutor-info {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 15px;
                font-weight: 600;
                color: #f0e8e6;
            }}

            .avatar-placeholder {{
                width: 35px;
                height: 35px;
                background-color: #554444;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
            }}

            .post-time {{
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                font-weight: 600;
                opacity: 0.9;
                color: #f0e8e6;
            }}

            .post-time svg {{
                width: 18px;
                height: 18px;
                fill: #f0e8e6;
            }}

            .btn-load-more {{
                background-color: #aa9393;
                color: #362521;
                border: none;
                padding: 12px 35px;
                border-radius: 20px;
                font-size: 16px;
                font-weight: 700;
                cursor: pointer;
                align-self: center;
                margin-top: 15px;
                transition: background-color 0.2s;
            }}

            .btn-load-more:hover {{
                background-color: #968080;
            }}

            @media (max-width: 768px) {{
                header {{
                    flex-direction: column;
                    gap: 15px;
                    padding: 15px 20px;
                }}
                nav {{
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 10px;
                }}
                .card {{
                    flex-direction: column;
                    text-align: center;
                }}
                .video-thumbnail {{
                    width: 100%;
                    height: 180px;
                }}
                .card-title {{
                    font-size: 20px;
                }}
                .tutor-info {{
                    justify-content: center;
                }}
                .post-time {{
                    justify-content: center;
                }}
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="logo-area">
                <div class="logo-placeholder">65+</div>
            </div>
            <nav>
                <a href="?pagina=Calendario">Calendario</a>
                <a href="?pagina=Mural">Mural Avisos</a>
                <a href="?pagina=Atividades" class="active">Atividades</a>
                <a href="?pagina=Ajuda">Ajuda</a>
                <div class="user-menu">
                    Ola, {usuario.nome}
                    <svg width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L5 5L9 1" stroke="#2c5270" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </nav>
        </header>

        <main>
            {cards_html}
            <button class="btn-load-more" onclick="alert('Carregando mais atividades...')">Carregar mais</button>
        </main>
    </body>
    </html>
    """
    
    components.html(html_completo, height=800, scrolling=True)