import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# 1. IDENTIDADE VISUAL & CONFIGURAÇÕES
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_OURO = "#FFD700"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_MENU = "#161B22"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS DE ALTO CONTRASTE (Blindado)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* MENU DROPDOWN: Correção de Contraste Absoluto */
    div[data-baseweb="select"] > div {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid #333 !important; }}
    div[data-baseweb="select"] span {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid {COR_VERDE} !important; }}
    div[data-baseweb="popover"] li {{ color: #FFFFFF !important; background-color: {COR_FUNDO_MENU} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}

    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}

    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; text-transform: uppercase;
        margin: 0 auto; display: block; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 20px {COR_VERDE}; color: #0E1117 !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA (Teste de Resiliência aplicado)
def fetch_radar_data(termo, local="", dias=30):
    d_fim = date.today()
    d_ini = d_fim - timedelta(days=dias)
    query = f"{termo} {local} after:{d_ini.strftime('%Y-%m-%d')}"
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)

# 4. HEADER
st.markdown(f"""
    <div style="text-align:center; padding: 40px 0; border-bottom: 1px solid #333;">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
        <h1 style="font-weight:700; margin-top:15px;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; letter-spacing: 2px;">VALE DOS IPÊS • HUB DE OPORTUNIDADES</p>
    </div>
""", unsafe_allow_html=True)

# Inicialização do estado para persistência (O "segredo" para não sumir os dados)
if 'resultados' not in st.session_state:
    st.session_state.resultados = {}

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# --- NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1: tema_n = st.selectbox("Escolha o Tema:", ["Todos", "Geral", "Economia", "Inovação", "UFLA"], key="sel_not")
    with c2: st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True); btn_n = st.button("BUSCAR NOTÍCIAS", key="btn_n")
    if btn_n:
        mapa = {"Todos": "Lavras MG (inovação OR economia OR UFLA)", "Geral": "Lavras MG", "Economia": "Lavras MG economia", "Inovação": "Lavras MG tecnologia", "UFLA": "UFLA Lavras"}
        st.session_state.resultados['noticias'] = fetch_radar_data(mapa[tema_n], "", dias=7)
    
    if 'noticias' in st.session_state.resultados:
        for n in st.session_state.resultados['noticias'][:10]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><h3>{n.title}</h3><a href="{n.link}" target="_blank">Ler mais →</a></div>', unsafe_allow_html=True)

# --- EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    loc_e = st.selectbox("Região dos Eventos:", ["Todos", "Lavras", "Minas Gerais", "Brasil"], key="sel_eve")
    btn_e = st.button("MAPEAR EVENTOS", key="btn_e")
    if btn_e:
        st.session_state.resultados['eventos'] = fetch_radar_data('("evento" OR "meetup" OR "congresso") (tecnologia OR inovação)', "" if loc_e=="Todos" else loc_e, dias=60)
    
    if 'eventos' in st.session_state.resultados:
        for e in st.session_state.resultados['eventos'][:10]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_LARANJA};"><h3>{e.title}</h3><a href="{e.link}" target="_blank">Ver detalhes →</a></div>', unsafe_allow_html=True)

# --- OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    perf_o = st.selectbox("Perfil:", ["Todos", "Startups", "Empresas", "Estudantes"], key="sel_op")
    btn_o = st.button("BUSCAR OPORTUNIDADES", key="btn_o")
    if btn_o:
        mapa_o = {"Todos": '("edital" OR "vaga") (inovação OR tecnologia)', "Startups": 'edital startup aceleração', "Empresas": '"inovação aberta" OR desafio', "Estudantes": 'estágio tecnologia hackathon'}
        st.session_state.resultados['oportunidades'] = fetch_radar_data(mapa_o[perf_o], "Brasil", dias=45)
    
    if 'oportunidades' in st.session_state.resultados:
        for o in st.session_state.resultados['oportunidades'][:10]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><h3>{o.title}</h3><a href="{o.link}" target="_blank">Acessar →</a></div>', unsafe_allow_html=True)

# --- PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_p = st.button("BUSCAR PRÊMIOS", key="btn_p")
    if btn_p:
        st.session_state.resultados['premios'] = fetch_radar_data('("vencedores" OR "ranking" OR "prêmio") (inovação OR tecnologia)', "Brasil", dias=120)
    
    if 'premios' in st.session_state.resultados:
        for p in st.session_state.resultados['premios'][:10]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><h3>{p.title}</h3><a href="{p.link}" target="_blank">Resultado →</a></div>', unsafe_allow_html=True)

# --- CALENDÁRIO ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_c = st.button("GERAR CALENDÁRIO 2026", key="btn_c")
    if btn_c:
        st.session_state.resultados['calendario'] = fetch_radar_data('("data" OR "acontece dia" OR "inscrições")', "Brasil", dias=150)
    
    if 'calendario' in st.session_state.resultados:
        st.markdown("<h1 style='text-align:center;'>2026</h1>", unsafe_allow_html=True)
        agenda = collections.defaultdict(list)
        meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        for item in st.session_state.resultados['calendario']:
            agenda[item.published_parsed.tm_mon].append(item)
        for i in range(1, 13):
            if i in agenda:
                st.markdown(f"<h3 style='color:{COR_VERDE}; border-bottom:1px solid #333; margin-top:20px;'>{meses[i]}</h3>", unsafe_allow_html=True)
                for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                    st.markdown(f'<div style="padding:8px 0; border-bottom:1px solid #222;"><span style="color:{COR_LARANJA}; font-weight:800; margin-right:15px;">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title}</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA 2026</p>", unsafe_allow_html=True)