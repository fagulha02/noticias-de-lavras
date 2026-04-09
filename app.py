import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. IDENTIDADE VISUAL OFICIAL (Manual Vale dos Ipês)
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_CINZA_ESCURO = "#636466"
COR_FUNDO = "#F8F9FA"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO PARA ELEGÂNCIA
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: {COR_FUNDO}; }}
    
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_CINZA_ESCURO}; }}

    /* Cards Elegantes */
    .card {{
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        transition: transform 0.2s ease;
    }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}

    /* Tags e Labels */
    .tag {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 10px;
        display: block;
    }}

    /* Estilização de Botões Streamlit para seguir o manual */
    div.stButton > button {{
        background-color: {COR_CINZA_ESCURO};
        color: white;
        border-radius: 8px;
        padding: 10px 25px;
        border: none;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: {COR_VERDE};
        color: white;
    }}

    /* Header Styling */
    .header-container {{
        text-align: center;
        padding: 40px 0;
        background: white;
        border-radius: 0 0 30px 30px;
        margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA ROBUSTO (Sem erros de URL)
def buscar_dados(termo, local=""):
    query = f"{termo} {local}".strip()
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 4. HEADER (CENTRALIZADO E ELEGANTE)
with st.container():
    st.markdown(f"""
        <div class="header-container">
            <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180" style="margin-bottom:15px;">
            <h1 style="color:{COR_CINZA_ESCURO}; font-weight:700; font-size: 2.2rem; margin:0;">Radar de Inteligência</h1>
            <p style="color:{COR_VERDE}; font-weight:400; font-size: 1.1rem; margin-top:5px;">Co-criando um polo para o desenvolvimento</p>
        </div>
    """, unsafe_allow_html=True)

# 5. ABAS PRINCIPAIS
tab_noticias, tab_eventos = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS"])

# --- ABA DE NOTÍCIAS ---
with tab_noticias:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topico_noticia = st.selectbox("Sobre o que quer se informar hoje?", 
                                    ["Geral", "Economia e Negócios", "Educação e UFLA", "Tecnologia", "Saúde"], 
                                    key="sel_not")
    with col2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        btn_not = st.button("ATUALIZAR RADAR")

    if btn_not:
        termos_map = {
            "Geral": "Lavras MG",
            "Economia e Negócios": "investimento startup Lavras",
            "Educação e UFLA": "UFLA pesquisa Lavras",
            "Tecnologia": "inovação tecnologia Lavras",
            "Saúde": "saúde hospital Lavras"
        }
        
        with st.spinner("🔍 Analisando fontes de dados..."):
            noticias = buscar_dados(termos_map[topico_noticia])
            if noticias:
                noticias_ord = sorted(noticias, key=lambda x: x.published_parsed, reverse=True)
                for n in noticias_ord[:12]:
                    data = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y')
                    st.markdown(f"""
                        <div class="card" style="border-top: 4px solid {COR_AZUL};">
                            <span class="tag" style="color:{COR_AZUL};">{topico_noticia}</span>
                            <h3 style="font-size:1.2rem; margin:10px 0; font-weight:600;">{n.title}</h3>
                            <p style="font-size:0.8rem; color:#999;">📅 {data} • Fonte: Google News</p>
                            <a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700; font-size:0.9rem;">LER NOTÍCIA COMPLETA →</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma novidade recente encontrada.")

# --- ABA DE EVENTOS ---
with tab_eventos:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    
    with c1:
        local_ev = st.selectbox("Abrangência Regional", ["Lavras", "Minas Gerais", "Brasil", "Mundial"], key="loc_ev")
    with c2:
        tema_ev = st.selectbox("Tipo de Evento", ["Todos os temas", "Tecnologia", "Empreendedorismo", "Cultura"], key="tem_ev")
    with c3:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        btn_ev = st.button("BUSCAR EVENTOS")

    if btn_ev:
        with st.spinner("📅 Mapeando agenda..."):
            termo_final = f"eventos {tema_ev if tema_ev != 'Todos os temas' else ''}"
            eventos = buscar_dados(termo_final, local_ev)
            
            if eventos:
                eventos_ord = sorted(eventos, key=lambda x: x.published_parsed, reverse=True)
                for e in eventos_ord[:12]:
                    data_e = datetime(*e.published_parsed[:6]).strftime('%d/%m/%Y')
                    st.markdown(f"""
                        <div class="card" style="border-top: 4px solid {COR_LARANJA};">
                            <span class="tag" style="color:{COR_LARANJA};">{tema_ev}</span>
                            <h3 style="font-size:1.2rem; margin:10px 0; font-weight:600;">{e.title}</h3>
                            <p style="font-size:0.8rem; color:#999;">📆 Publicado em: {data_e}</p>
                            <a href="{e.link}" target="_blank" 
                               style="display:inline-block; margin-top:10px; padding:8px 20px; background:{COR_LARANJA}; color:white; border-radius:6px; text-decoration:none; font-size:0.8rem; font-weight:600;">
                               VER DETALHES DO EVENTO
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum evento mapeado para estes filtros no momento.")

# 6. RODAPÉ
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(f"<p style='text-align:center; color:#999; font-size:0.8rem;'>© 2026 Vale dos Ipês Lavras. Sistema de Inteligência Governamental e Ecossistema.</p>", unsafe_allow_html=True)