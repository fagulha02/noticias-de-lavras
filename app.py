import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# 1. CONFIGURAÇÕES E IDENTIDADE
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_OURO = "#FFD700"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_MENU = "#161B22"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS DE ALTO CONTRASTE (UI Blindada)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    div[data-baseweb="select"] > div {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid #333 !important; }}
    div[data-baseweb="select"] span {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid {COR_VERDE} !important; }}
    div[data-baseweb="popover"] li {{ color: #FFFFFF !important; background-color: {COR_FUNDO_MENU} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}

    .card {{ 
        background: linear-gradient(145deg, #1E2129, #161B22); 
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; 
        transition: 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}
    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }}
    
    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; width: 100%; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; box-shadow: 0 0 20px {COR_VERDE}; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA OTIMIZADO (Analista: Mais flexibilidade na query)
def fetch_radar_data(termo_base, extra_v="", regiao="Lavras", d_ini=None, d_fim=None):
    try:
        mapa_geo = {
            "Lavras": 'Lavras MG OR "Lavras/MG"',
            "Sul de Minas": '"Sul de Minas" OR Varginha OR "Pouso Alegre" OR Itajubá',
            "Minas Gerais": '"Minas Gerais" OR MG',
            "Brasil": "Brasil"
        }
        geo_query = mapa_geo.get(regiao, "Lavras MG")
        
        # Montagem flexível: Prioriza a localização e soma o termo e a palavra-chave
        query = f"{geo_query} {termo_base} {extra_v}".strip()
        
        d_ini = d_ini if d_ini else date.today() - timedelta(days=30)
        d_fim = d_fim if d_fim else date.today()
        
        query += f" after:{d_ini.strftime('%Y-%m-%d')} before:{d_fim.strftime('%Y-%m-%d')}"
        query_encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        feed = feedparser.parse(url)
        return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
    except:
        return []

# 4. HEADER
st.markdown(f"""<div style="text-align:center; padding: 30px 0;">
    <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
    <h1 style="margin-top:15px; font-size: 2.5rem;">Radar de Inteligência</h1>
    <p style="color:{COR_VERDE}; letter-spacing: 3px; font-weight: 400;">VALE DOS IPÊS • HUB DE OPORTUNIDADES</p>
</div>""", unsafe_allow_html=True)

if 'db' not in st.session_state: st.session_state.db = {}

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# Função Auxiliar (Redundância Removida)
def render_filtros_com_geo(key_prefix, default_days=30):
    c_geo, c_ex, c_d1, c_d2, c_btn = st.columns([1.2, 1.5, 1, 1, 1])
    with c_geo: reg = st.selectbox("Região:", ["Lavras", "Sul de Minas", "Minas Gerais", "Brasil"], key=f"geo_{key_prefix}")
    with c_ex: extra = st.text_input("🔍 Palavra-chave:", key=f"ex_{key_prefix}", placeholder="Ex: Café, IA...")
    with c_d1: ini = st.date_input("De:", value=date.today() - timedelta(days=default_days), key=f"ini_{key_prefix}")
    with c_d2: fim = st.date_input("Até:", value=date.today(), key=f"fim_{key_prefix}")
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    return reg, extra, ini, fim, c_btn

# --- ABA NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    tema = st.selectbox("Tópico:", ["Todos", "Economia", "Inovação", "UFLA"], key="n_tema")
    reg, extra, d_i, d_f, c_btn = render_filtros_com_geo("not", 7)
    if c_btn.button("BUSCAR NOTÍCIAS", key="btn_not"):
        mapa = {"Todos": "inovação OR tecnologia OR economia", "Economia": "economia OR mercado", "Inovação": "inovação OR startups", "UFLA": "UFLA"}
        st.session_state.db['n'] = fetch_radar_data(mapa[tema], extra, reg, d_i, d_f)
    if 'n' in st.session_state.db:
        for item in st.session_state.db['n'][:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Ler mais →</a></div>', unsafe_allow_html=True)

# --- ABA EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    reg, extra, d_i, d_f, c_btn = render_filtros_com_geo("eve", 60)
    if c_btn.button("MAPEAR EVENTOS", key="btn_eve"):
        st.session_state.db['e'] = fetch_radar_data('evento OR meetup OR congresso', extra, reg, d_i, d_f)
    if 'e' in st.session_state.db:
        for item in st.session_state.db['e'][:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_LARANJA};"><span class="badge" style="background:{COR_LARANJA}33; color:{COR_LARANJA};">Evento</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Ver detalhes →</a></div>', unsafe_allow_html=True)

# --- ABA OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    perfil = st.selectbox("Para quem:", ["Todos", "Startups", "Empresas", "Estudantes"], key="o_perf")
    reg, extra, d_i, d_f, c_btn = render_filtros_com_geo("opt", 45)
    if c_btn.button("BUSCAR OPORTUNIDADES", key="btn_opt"):
        mapa = {"Todos": 'edital OR vaga OR chamada', "Startups": 'edital startup aceleração', "Empresas": '"inovação aberta" OR desafio', "Estudantes": 'estágio tecnologia'}
        st.session_state.db['o'] = fetch_radar_data(mapa[perfil], extra, reg, d_i, d_f)
    if 'o' in st.session_state.db:
        for item in st.session_state.db['o'][:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><span class="badge" style="background:{COR_VERDE}33; color:{COR_VERDE};">Oportunidade</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Acessar →</a></div>', unsafe_allow_html=True)

# --- ABA PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    reg, extra, d_i, d_f, c_btn = render_filtros_com_geo("pre", 120)
    if c_btn.button("BUSCAR PREMIAÇÕES", key="btn_pre"):
        st.session_state.db['p'] = fetch_radar_data('vencedores OR ranking OR prêmio', extra, reg, d_i, d_f)
    if 'p' in st.session_state.db:
        for item in st.session_state.db['p'][:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><span class="badge" style="background:{COR_OURO}33; color:{COR_OURO};">Premiação</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Resultado →</a></div>', unsafe_allow_html=True)

# --- ABA CALENDÁRIO ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    reg, extra, d_i, d_f, c_btn = render_filtros_com_geo("cal", 180)
    if c_btn.button("GERAR CALENDÁRIO", key="btn_cal"):
        st.session_state.db['c'] = fetch_radar_data('data OR "acontece dia" OR inscrições', extra, reg, d_i, d_f)
    if 'c' in st.session_state.db:
        meses_n = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        agenda = collections.defaultdict(list)
        for item in st.session_state.db['c']: agenda[item.published_parsed.tm_mon].append(item)
        for i in range(1, 13):
            if i in agenda:
                st.markdown(f"<h3 style='color:{COR_VERDE}; border-bottom:1px solid #333; margin-top:20px;'>{meses_n[i]}</h3>", unsafe_allow_html=True)
                for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                    st.markdown(f'<div style="padding:10px 0; border-bottom:1px solid #222;"><span style="color:{COR_LARANJA}; font-weight:800; margin-right:15px;">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title}</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • 2026</p>", unsafe_allow_html=True)