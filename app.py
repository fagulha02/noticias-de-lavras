# Query: app.py
# ContextLines: 1

import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# 1. Configurações de Identidade Visual (Baseado no Manual)
COR_VERDE = "#92BC4E"   # [cite: 27]
COR_LARANJA = "#EB6923" # [cite: 26]
COR_AZUL = "#00ADEF"    # [cite: 25]
COR_CINZA = "#636466"   # [cite: 28]

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# CSS Customizado
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* Força o fundo da página como claro para combinar com o manual */
    .stApp {{
        background-color: #f5f7f9;
    }}

    /* Fonte principal e cor do texto base (Cinza do manual) */
    html, body, [class*="css"] {{ 
        font-family: 'Montserrat', sans-serif; 
        color: #636466 !important; 
    }}

    /* Estilização do Título do Header */
    .main-header h1 {{
        color: #636466 !important;
        font-weight: 700;
    }}

    .main-header p {{
        color: #92BC4E !important;
        font-weight: bold;
    }}

    /* Cards de Notícias */
    .card {{
        background-color: white !important;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00ADEF; /* Azul do manual */
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    /* Força a cor dos títulos das notícias dentro dos cards */
    .card h4 {{
        color: #636466 !important;
        margin-bottom: 10px;
    }}

    .tag {{
        color: #EB6923 !important; /* Laranja do manual */
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Lógica de Pesquisa (Motor de Busca Gratuito)
def buscar_noticias(termo):
    url = f"https://news.google.com/rss/search?q={termo}+Lavras+MG&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 3. Interface - Cabeçalho
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo_vale.png", width=150)
    except:
        st.subheader("🌳 Vale dos Ipês")

with col2:
    st.markdown(f"""
        <div class="main-header">
            <h1 style='margin:0;'>Radar de Inteligência Lavras</h1>
            <p style='margin:0; color:{COR_VERDE}; font-weight:bold;'>Co-criando um polo para o desenvolvimento</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Barra Lateral e Filtros
st.sidebar.header("Filtros de Pesquisa")
categoria = st.sidebar.selectbox("Tópico", ["Tudo", "Economia", "Educação", "Saúde", "Rankings"])

termos_busca = {
    "Tudo": "",
    "Economia": "investimento+startup+negocios",
    "Educação": "UFLA+pesquisa+escola",
    "Saúde": "hospital+saude+prefeitura",
    "Rankings": "ranking+melhores+felicidade"
}

if st.sidebar.button("Atualizar Radar"):
    with st.spinner("Buscando informações em tempo real..."):
        noticias = buscar_noticias(termos_busca[categoria])
        
        if not noticias:
            st.warning("Nenhuma notícia nova encontrada para este filtro.")
        else:
            # 1. Organiza da mais nova para a mais velha
            noticias_ordenadas = sorted(
                noticias, 
                key=lambda x: x.published_parsed, 
                reverse=True
            )

            # 2. Loop para exibir os cards organizados
            for entry in noticias_ordenadas[:15]: 
                # Converte para data do Brasil (Dia/Mês/Ano)
                dt = datetime(*entry.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
                
                st.markdown(f"""
                    <div class="card">
                        <span class="tag">{categoria}</span>
                        <h4 style="color: {COR_CINZA} !important;">{entry.title}</h4>
                        <p style="font-size: 0.85rem; color: #888;">Publicado em: {dt}</p>
                        <a href="{entry.link}" target="_blank" class="btn-link" 
                           style="color:{COR_AZUL}; text-decoration:none; font-weight:bold;">
                           Acessar Notícia Completa →
                        </a>
                    </div>
                """, unsafe_allow_html=True)

# 5. Rodapé Informativo (Fora do bloco de repetição)
st.divider()
st.caption("Ferramenta desenvolvida para o ecossistema Vale dos Ipês - Lavras/MG")
