import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. IDENTIDADE VISUAL (Adaptada para Dark Mode)
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS CUSTOMIZADO (MODO ESCURO ELEGANTE)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    /* Fundo Geral */
    .stApp {{ background-color: #0E1117; }}
    
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}

    /* Cards Dark Mode */
    .card {{
        background: {COR_FUNDO_CARD};
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: scale(1.01); }}

    /* Centralização e Estilo dos Botões */
    .stButton {{
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }}
    
    div.stButton > button {{
        background-color: transparent;
        color: white;
        border: 2px solid {COR_VERDE};
        border-radius: 30px;
        padding: 12px 40px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s;
    }}
    
    div.stButton > button:hover {{
        background-color: {COR_VERDE};
        box-shadow: 0 0 15px {COR_VERDE};
        color: #0E1117;
    }}

    /* Estilo Especial para o Botão de Eventos */
    .btn-eventos div.stButton > button {{
        border-color: {COR_LARANJA};
    }}
    .btn-eventos div.stButton > button:hover {{
        background-color: {COR_LARANJA};
        box-shadow: 0 0 15px {COR_LARANJA};
    }}

    /* Header e Logo */
    .header-container {{
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(180deg, #161B22 0%, #0E1117 100%);
        border-bottom: 1px solid #333;
        margin-bottom: 30px;
    }}
    
    .logo-img {{
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA
def buscar_dados(termo, local=""):
    query = f"{termo} {local}".strip()
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 4. HEADER CENTRALIZADO
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="220" class="logo-img">
        <h1 style="font-weight:700; font-size: 2.5rem; margin:0; letter-spacing:-1px;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; font-weight:400; font-size: 1.2rem; opacity:0.9;">VALE DOS IPÊS • LAVRAS/MG</p>
    </div>
""", unsafe_allow_html=True)

# 5. ABAS
tab_noticias, tab_eventos = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS"])

with tab_noticias:
    st.markdown("<br>", unsafe_allow_html=True)
    # Filtro centralizado
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        topico_noticia = st.selectbox("Selecione o Tópico", 
                                    ["Geral", "Economia e Negócios", "Educação e UFLA", "Inovação", "Saúde"])
        btn_not = st.button("ATUALIZAR RADAR")

    if btn_not:
        termos_map = {
            "Geral": "Lavras MG",
            "Economia e Negócios": "investimento startup Lavras",
            "Educação e UFLA": "UFLA pesquisa Lavras",
            "Inovação": "inovação tecnologia Lavras",
            "Saúde": "saúde hospital Lavras"
        }
        with st.spinner("Sincronizando dados..."):
            noticias = buscar_dados(termos_map[topico_noticia])
            for n in noticias[:12]:
                data = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""
                    <div class="card" style="border-left: 4px solid {COR_AZUL};">
                        <small style="color:{COR_AZUL}; font-weight:700;">{topico_noticia.upper()}</small>
                        <h3 style="margin:10px 0; font-size:1.3rem;">{n.title}</h3>
                        <p style="color:#888; font-size:0.9rem;">📅 {data}</p>
                        <a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700;">VER NOTÍCIA →</a>
                    </div>
                """, unsafe_allow_html=True)

with tab_eventos:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid_ev, _ = st.columns([1, 2, 1])
    with col_mid_ev:
        local_ev = st.selectbox("Abrangência", ["Lavras", "Minas Gerais", "Brasil", "Mundial"])
        tema_ev = st.selectbox("Tema", ["Todos os temas", "Tecnologia", "Empreendedorismo", "Cultura"])
        st.markdown('<div class="btn-eventos">', unsafe_allow_html=True)
        btn_ev = st.button("BUSCAR AGENDA")
        st.markdown('</div>', unsafe_allow_html=True)

    if btn_ev:
        with st.spinner("Mapeando eventos..."):
            termo_final = f"eventos {tema_ev if tema_ev != 'Todos os temas' else ''}"
            eventos = buscar_dados(termo_final, local_ev)
            for e in eventos[:12]:
                data_e = datetime(*e.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""
                    <div class="card" style="border-left: 4px solid {COR_LARANJA};">
                        <small style="color:{COR_LARANJA}; font-weight:700;">{tema_ev.upper()}</small>
                        <h3 style="margin:10px 0; font-size:1.3rem;">{e.title}</h3>
                        <p style="color:#888; font-size:0.9rem;">📅 {data_e}</p>
                        <a href="{e.link}" target="_blank" 
                           style="display:inline-block; margin-top:10px; padding:10px 25px; background:{COR_LARANJA}; color:white; border-radius:30px; text-decoration:none; font-size:0.8rem; font-weight:700;">
                           VER DETALHES
                        </a>
                    </div>
                """, unsafe_allow_html=True)

# 6. RODAPÉ
st.markdown("<br><br><p style='text-align:center; opacity:0.5; font-size:0.8rem;'>© 2026 VALE DOS IPÊS • SISTEMA DE INTELIGÊNCIA</p>", unsafe_allow_html=True)