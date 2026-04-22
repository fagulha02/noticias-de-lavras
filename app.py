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

# 2. CSS DE ALTO CONTRASTE & UI (Análise de UX concluída)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* FIX: Dropdowns de Alto Contraste */
    div[data-baseweb="select"] > div {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid #333 !important; }}
    div[data-baseweb="select"] span {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {COR_FUNDO_MENU} !important; border: 1px solid {COR_VERDE} !important; }}
    div[data-baseweb="popover"] li {{ color: #FFFFFF !important; background-color: {COR_FUNDO_MENU} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}

    /* Cards e Badges */
    .card {{ 
        background: linear-gradient(145deg, #1E2129, #161B22); 
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; 
        transition: 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }}
    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }}
    
    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; width: 100%; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; box-shadow: 0 0 20px {COR_VERDE}; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA AVANÇADO (Analista: Robustez garantida)
def fetch_radar_data(termo_base, extra_v="", d_ini=None, d_fim=None):
    with st.spinner("Sincronizando dados estratégica..."):
        query = f"{termo_base} {extra_v}".strip()
        # Fallback para datas nulas
        d_ini = d_ini if d_ini else date.today() - timedelta(days=30)
        d_fim = d_fim if d_fim else date.today()
        
        query += f" after:{d_ini.strftime('%Y-%m-%d')} before:{d_fim.strftime('%Y-%m-%d')}"
        query_encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        feed = feedparser.parse(url)
        return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)

# 4. HEADER
st.markdown(f"""<div style="text-align:center; padding: 30px 0;">
    <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180" style="filter: drop-shadow(0 0 10px rgba(255,255,255,0.1));">
    <h1 style="margin-top:15px; font-size: 2.5rem;">Radar de Inteligência</h1>
    <p style="color:{COR_VERDE}; letter-spacing: 3px; font-weight: 400;">VALE DOS IPÊS • PESQUISA AVANÇADA</p>
</div>""", unsafe_allow_html=True)

if 'db' not in st.session_state: st.session_state.db = {}

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

def render_filtros(key_prefix, default_days=30):
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1: extra = st.text_input("🔍 Palavra-chave extra:", key=f"ex_{key_prefix}", placeholder="Ex: IA, Agronegócio, Sustentabilidade...")
    with c2: ini = st.date_input("De:", value=date.today() - timedelta(days=default_days), key=f"ini_{key_prefix}")
    with c3: fim = st.date_input("Até:", value=date.today(), key=f"fim_{key_prefix}")
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    return extra, ini, fim, c4

# --- ABA NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    tema = st.selectbox("Escolha o Tema Base:", ["Todos", "Geral", "Economia", "Inovação", "UFLA"], key="n_tema")
    extra, d_i, d_f, c_btn = render_filtros("not", 7)
    if c_btn.button("BUSCAR", key="btn_not"):
        mapa = {"Todos": "Lavras MG (inovação OR economia OR tecnologia)", "Geral": "Lavras MG", "Economia": "Lavras MG economia", "Inovação": "Lavras MG tecnologia", "UFLA": "UFLA Lavras"}
        st.session_state.db['n'] = fetch_radar_data(mapa[tema], extra, d_i, d_f)
    if 'n' in st.session_state.db:
        for item in st.session_state.db['n'][:15]:
            dt = datetime(*item.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3>{item.title}</h3><p style="color:#888; font-size:0.85rem;">📅 {dt}</p><a href="{item.link}" target="_blank" style="color:{COR_AZUL}; font-weight:700; text-decoration:none;">LER NOTÍCIA COMPLETA →</a></div>', unsafe_allow_html=True)

# --- ABA EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    regiao = st.selectbox("Abrangência Regional:", ["Todos", "Lavras", "Minas Gerais", "Brasil"], key="e_reg")
    extra, d_i, d_f, c_btn = render_filtros("eve", 60)
    if c_btn.button("MAPEAR", key="btn_eve"):
        base = '("evento" OR "meetup" OR "congresso" OR "workshop") (tecnologia OR inovação OR startup)'
        st.session_state.db['e'] = fetch_radar_data(base, f"{'' if regiao=='Todos' else regiao} {extra}", d_i, d_f)
    if 'e' in st.session_state.db:
        for item in st.session_state.db['e'][:15]:
            dt = datetime(*item.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_LARANJA};"><span class="badge" style="background:{COR_LARANJA}33; color:{COR_LARANJA};">Evento</span><h3>{item.title}</h3><p style="color:#888; font-size:0.85rem;">📅 {dt}</p><a href="{item.link}" target="_blank" style="color:{COR_LARANJA}; font-weight:700; text-decoration:none;">VER DETALHES DO EVENTO →</a></div>', unsafe_allow_html=True)

# --- ABA OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    perfil = st.selectbox("Filtrar por Perfil:", ["Todos", "Startups", "Empresas", "Estudantes"], key="o_perf")
    extra, d_i, d_f, c_btn = render_filtros("opt", 45)
    if c_btn.button("BUSCAR OPORTUNIDADES", key="btn_opt"):
        mapa = {"Todos": '("edital" OR "vaga" OR "chamada") (inovação OR tecnologia)', "Startups": 'edital startup aceleração', "Empresas": '"inovação aberta" OR desafio corporativo', "Estudantes": 'estágio tecnologia OR hackathon'}
        st.session_state.db['o'] = fetch_radar_data(mapa[perfil], extra, d_i, d_f)
    if 'o' in st.session_state.db:
        for item in st.session_state.db['o'][:15]:
            dt = datetime(*item.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><span class="badge" style="background:{COR_VERDE}33; color:{COR_VERDE};">Oportunidade</span><h3>{item.title}</h3><p style="color:#888; font-size:0.85rem;">📅 Postado em: {dt}</p><a href="{item.link}" target="_blank" style="color:{COR_VERDE}; font-weight:700; text-decoration:none;">ACESSAR EDITAL →</a></div>', unsafe_allow_html=True)

# --- ABA PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    extra, d_i, d_f, c_btn = render_filtros("pre", 120)
    if c_btn.button("BUSCAR PREMIAÇÕES", key="btn_pre"):
        st.session_state.db['p'] = fetch_radar_data('("vencedores" OR "ranking" OR "prêmio") (inovação OR tecnologia OR criatividade)', extra, d_i, d_f)
    if 'p' in st.session_state.db:
        for item in st.session_state.db['p'][:15]:
            dt = datetime(*item.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><span class="badge" style="background:{COR_OURO}33; color:{COR_OURO};">Premiação</span><h3>{item.title}</h3><p style="color:#888; font-size:0.85rem;">📅 Resultados em: {dt}</p><a href="{item.link}" target="_blank" style="color:{COR_OURO}; font-weight:700; text-decoration:none;">VER RESULTADOS →</a></div>', unsafe_allow_html=True)

# --- ABA CALENDÁRIO ---
with tabs[4]:s
    st.markdown("<br>", unsafe_allow_html=True)
    extra, d_i, d_f, c_btn = render_filtros("cal", 180)
    if c_btn.button("GERAR CRONOGRAMA", key="btn_cal"):
        st.session_state.db['c'] = fetch_radar_data('("data" OR "acontece dia" OR "inscrições até")', extra, d_i, d_f)
    if 'c' in st.session_state.db:
        st.markdown("<h2 style='text-align:center;'>🗓️ Agenda 2026</h2>", unsafe_allow_html=True)
        meses_n = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        agenda = collections.defaultdict(list)
        for item in st.session_state.db['c']: agenda[item.published_parsed.tm_mon].append(item)
        for i in range(1, 13):
            if i in agenda:
                st.markdown(f"<h3 style='color:{COR_VERDE}; border-bottom:2px solid #333; margin-top:30px;'>{meses_n[i]}</h3>", unsafe_allow_html=True)
                for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                    st.markdown(f'<div style="padding:10px 0; border-bottom:1px solid #222; display:flex; align-items:center;"><span style="color:{COR_LARANJA}; font-weight:800; margin-right:20px; font-size:1.2rem;">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title}</div>', unsafe_allow_html=True)

# --- DIAGNÓSTICO ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("diagnostico_final"):
        st.markdown(f"<h3 style='color:{COR_VERDE};'>Censo Semestral de Inovação</h3>", unsafe_allow_html=True)
        st.text_input("Nome da Startup/Iniciativa")
        st.text_area("Resumo da Proposta")
        st.form_submit_button("Enviar para o Vale")

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA CRONOLÓGICA 2026</p>", unsafe_allow_html=True)