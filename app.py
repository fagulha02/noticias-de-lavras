import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# 1. IDENTIDADE VISUAL
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_OURO = "#FFD700"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"
COR_FUNDO_MENU = "#161B22"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS DE ALTO CONTRASTE (Análise: UI/UX Otimizada)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* FIX: Visibilidade dos Menus Dropdown */
    div[data-baseweb="select"] > div {{
        background-color: {COR_FUNDO_MENU} !important;
        border: 1px solid #333 !important;
    }}
    div[data-baseweb="select"] span {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid {COR_VERDE} !important; }}
    div[data-baseweb="popover"] li {{ color: #FFFFFF !important; background-color: {COR_FUNDO_MENU} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}

    /* Cards Estilizados */
    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}

    /* Botões */
    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; text-transform: uppercase;
        margin: 0 auto; display: block; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 20px {COR_VERDE}; color: #0E1117 !important; }}

    .header-container {{ text-align: center; padding: 40px 0; border-bottom: 1px solid #333; }}
    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA (Análise: Lógica de Filtro Temporal)
def fetch_radar_data(termo, local="", d_inicio=None, d_fim=None):
    query = f"{termo} {local}".strip()
    if d_inicio: query += f" after:{d_inicio.strftime('%Y-%m-%d')}"
    if d_fim: query += f" before:{d_fim.strftime('%Y-%m-%d')}"
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    # Retorna ordenado por data (mais recente primeiro)
    return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)

# 4. HEADER
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
        <h1 style="font-weight:700; margin-top:15px;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; letter-spacing: 2px;">VALE DOS IPÊS • HUB DE OPORTUNIDADES</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# --- ABA NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: tema_n = st.selectbox("Tema:", ["Todos", "Geral", "Economia", "Inovação", "UFLA"], key="n_tema")
    with c2: d_ini_n = st.date_input("De:", value=date.today() - timedelta(days=7), key="n_ini")
    with c3: d_fim_n = st.date_input("Até:", value=date.today(), key="n_fim")
    if st.button("BUSCAR NOTÍCIAS"):
        mapa = {"Todos": "Lavras MG (inovação OR economia OR UFLA)", "Geral": "Lavras MG", "Economia": "Lavras MG economia", "Inovação": "Lavras MG tecnologia", "UFLA": "UFLA Lavras"}
        res = fetch_radar_data(mapa[tema_n], "", d_ini_n, d_fim_n)
        for n in res[:12]:
            dt = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3>{n.title}</h3><p style="color:#888; font-size:0.8rem;">📅 {dt}</p><a href="{n.link}" target="_blank">Ler mais →</a></div>', unsafe_allow_html=True)

# --- ABA OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1: perfil_op = st.selectbox("Para quem?", ["Todos", "Startups", "Empresas Consolidadas", "Estudantes", "Empreendedores"], key="o_per")
    with c2: abr_op = st.selectbox("Região:", ["Todos", "Lavras e Região", "Minas Gerais", "Brasil"], key="o_abr")
    with c3: d_ini_o = st.date_input("Publicado após:", value=date(2026, 1, 1), key="o_ini")
    if st.button("BUSCAR OPORTUNIDADES"):
        mapa_o = {"Todos": '("edital" OR "vaga") (inovação OR tecnologia)', "Startups": '("edital" OR "inscrições") (startup OR aceleração)', "Empresas Consolidadas": '"inovação aberta" OR "desafio"', "Estudantes": '"vaga estágio" OR hackathon', "Empreendedores": '"oportunidade" OR sebrae'}
        res = fetch_radar_data(mapa_o[perfil_op], "" if abr_op == "Todos" else abr_op, d_ini_o)
        for o in res[:15]:
            dt = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><span class="badge" style="background:{COR_VERDE}33; color:{COR_VERDE};">Oportunidade</span><h3>{o.title}</h3><p style="color:#888; font-size:0.8rem;">📅 {dt}</p><a href="{o.link}" target="_blank">Acessar →</a></div>', unsafe_allow_html=True)

# --- ABA CALENDÁRIO ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GERAR CALENDÁRIO 2026"):
        res = fetch_radar_data('("data" OR "até dia" OR "inscrições")', "Brasil", date(2026, 1, 1), date(2026, 12, 31))
        if res:
            st.markdown("<h1 style='text-align:center; color:#FFF;'>2026</h1>", unsafe_allow_html=True)
            agenda = collections.defaultdict(list)
            meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            for item in res: agenda[item.published_parsed.tm_mon].append(item)
            for i in range(1, 13):
                if i in agenda:
                    st.markdown(f"<h3 style='color:{COR_VERDE}; border-bottom:1px solid #333; margin-top:20px;'>{meses[i]}</h3>", unsafe_allow_html=True)
                    for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                        st.markdown(f'<div style="padding:10px 0; border-bottom:1px solid #222;"><span style="color:{COR_LARANJA}; font-weight:800; margin-right:15px;">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title[:150]}...</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA 2026</p>", unsafe_allow_html=True)