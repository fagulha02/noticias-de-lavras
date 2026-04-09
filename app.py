import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# 1. Configurações de Identidade Visual (Baseado no Manual)
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_CINZA = "#636466"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# CSS Customizado
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    .stApp {{ background-color: #f5f7f9; }}
    html, body, [class*="css"] {{ font-family: 'Montserrat', sans-serif; color: #636466 !important; }}
    .card {{
        background-color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .tag {{ font-weight: bold; font-size: 0.9rem; }}
    </style>
""", unsafe_allow_html=True)

# 2. Lógica de Pesquisa
def buscar_noticias(termo, local="Lavras MG"):
    # Se o local for Mundial, removemos a trava de localização
    loc_query = "" if local == "Mundial" else f"+{local}"
    url = f"https://news.google.com/rss/search?q={termo}{loc_query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 3. Cabeçalho
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo_vale.png", width=150)
    except:
        st.subheader("🌳 Vale dos Ipês")

with col2:
    st.markdown(f"""
        <div style="padding-top:10px;">
            <h1 style='margin:0; color:{COR_CINZA};'>Radar de Inteligência</h1>
            <p style='margin:0; color:{COR_VERDE}; font-weight:bold;'>Co-criando um polo para o desenvolvimento</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Interface por Abas
tab1, tab2 = st.tabs(["📰 Notícias de Lavras", "📅 Agenda de Eventos"])

with tab1:
    st.sidebar.header("Filtros de Notícias")
    categoria = st.sidebar.selectbox("Tópico", ["Tudo", "Economia", "Educação", "Saúde", "Rankings"])
    
    termos_noticias = {
        "Tudo": "",
        "Economia": "investimento+startup+negocios",
        "Educação": "UFLA+pesquisa+escola",
        "Saúde": "hospital+saude+prefeitura",
        "Rankings": "ranking+melhores+felicidade"
    }

    if st.sidebar.button("Atualizar Notícias"):
        with st.spinner("Buscando notícias..."):
            noticias = buscar_noticias(termos_noticias[categoria])
            if not noticias:
                st.warning("Nenhuma notícia encontrada.")
            else:
                noticias_ord = sorted(noticias, key=lambda x: x.published_parsed, reverse=True)
                for entry in noticias_ord[:15]:
                    dt = datetime(*entry.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
                    st.markdown(f"""
                        <div class="card" style="border-left: 5px solid {COR_AZUL};">
                            <span class="tag" style="color:{COR_AZUL};">{categoria}</span>
                            <h4 style="margin: 10px 0;">{entry.title}</h4>
                            <p style="font-size: 0.85rem; color: #888;">Publicado em: {dt}</p>
                            <a href="{entry.link}" target="_blank" style="color:{COR_AZUL}; font-weight:bold; text-decoration:none;">Ver Notícia Completa →</a>
                        </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"<h3 style='color:{COR_LARANJA};'>Busca de Eventos e Meetups</h3>", unsafe_allow_html=True)
    
    col_loc, col_tema = st.columns(2)
    with col_loc:
        local_ev = st.selectbox("Abrangência", ["Lavras", "Minas Gerais", "Brasil", "Mundial"])
    with col_tema:
        tema_ev = st.selectbox("Tema", ["Todos os eventos", "Inovação", "Tecnologia", "Agronegócio", "Cultura"])

    if st.button("🔍 Pesquisar Eventos"):
        with st.spinner("Buscando agenda..."):
            query_ev = f"eventos {tema_ev if tema_ev != 'Todos os eventos' else ''}"
            eventos = buscar_noticias(query_ev, local_ev)
            
            if not eventos:
                st.info("Nenhum evento recente encontrado para estes filtros.")
            else:
                eventos_ord = sorted(eventos, key=lambda x: x.published_parsed, reverse=True)
                for ev in eventos_ord[:12]:
                    dt_ev = datetime(*ev.published_parsed[:6]).strftime('%d/%m/%Y')
                    st.markdown(f"""
                        <div class="card" style="border-left: 5px solid {COR_LARANJA};">
                            <span class="tag" style="color:{COR_LARANJA};">{tema_ev}</span>
                            <h4 style="margin: 10px 0;">{ev.title}</h4>
                            <p style="font-size: 0.85rem; color: #888;">📅 Divulgado em: {dt_ev}</p>
                            <a href="{ev.link}" target="_blank" 
                               style="background-color:{COR_LARANJA}; color:white; padding:8px 15px; border-radius:5px; text-decoration:none; display:inline-block; font-size:14px; font-weight:bold;">
                               Ver Detalhes do Evento
                            </a>
                        </div>
                    """, unsafe_allow_html=True)

st.divider()
st.caption("Ferramenta desenvolvida para o ecossistema Vale dos Ipês - Lavras/MG")