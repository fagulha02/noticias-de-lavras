import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# Configuração visual de Software Desktop
st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide")

# CSS para esconder elementos de "site" e focar no "App"
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #333; }
    .card-local { background: #1E2129; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL INTERATIVO ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png", width=150)
    st.title("Painel de Controle")
    regiao = st.selectbox("Região de Busca:", ["Lavras", "Sul de Minas", "Minas Gerais", "Brasil"])
    dias = st.slider("Histórico (dias):", 7, 180, 30)
    st.markdown("---")
    st.info("Versão Desktop Pro 2026")

# MOTOR DE BUSCA
def fetch_data(termo, extra="", geo="Lavras", d=30):
    mapa_geo = {"Lavras": 'Lavras MG', "Sul de Minas": 'Varginha OR "Sul de Minas"', "Minas Gerais": 'MG', "Brasil": 'Brasil'}
    q = f"({termo}) ({mapa_geo[geo]}) {extra} after:{(date.today() - timedelta(days=d)).strftime('%Y-%m-%d')}"
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    return feedparser.parse(url).entries

# INTERFACE PRINCIPAL
st.title("🌳 Radar de Inteligência")
tabs = st.tabs(["📰 Notícias", "💡 Oportunidades", "🗓️ Calendário"])

with tabs[0]:
    txt = st.text_input("Filtrar notícia por palavra:", key="n_txt")
    if st.button("BUSCAR NOTÍCIAS"):
        res = fetch_data("inovação OR economia", txt, regiao, dias)
        for n in res[:15]:
            st.markdown(f'<div class="card-local"><b>{n.title}</b><br><a href="{n.link}">Abrir link</a></div>', unsafe_allow_html=True)

with tabs[1]:
    txt_o = st.text_input("Filtrar oportunidade por palavra:", key="o_txt")
    if st.button("BUSCAR EDITAIS"):
        res = fetch_data("edital OR vaga OR fomento", txt_o, regiao, dias)
        for o in res[:15]:
            st.markdown(f'<div class="card-local" style="border-left: 5px solid #92BC4E;"><b>{o.title}</b><br><a href="{o.link}">Acessar</a></div>', unsafe_allow_html=True)