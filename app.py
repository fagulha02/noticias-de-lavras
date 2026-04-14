import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date

# 1. IDENTIDADE VISUAL
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO (Design Dark e Ajuste de Componentes)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}

    /* Títulos das Abas */
    button[data-baseweb="tab"] {{ font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }}

    /* Selectboxes e Calendário */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"] ul {{ background-color: #161B22 !important; }}
    div[data-baseweb="select"] span {{ color: white !important; }}
    
    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}

    div.stButton > button {{
        background-color: transparent;
        color: white;
        border: 3px solid {COR_VERDE} !important;
        border-radius: 50px;
        padding: 10px 40px;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0 auto;
        display: block;
        transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 20px {COR_VERDE}; color: #0E1117 !important; }}

    .header-container {{ text-align: center; padding: 50px 0; background: linear-gradient(180deg, #161B22 0%, #0E1117 100%); border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA OTIMIZADO
def buscar_dados_com_periodo(termo, local="", d_inicio=None, d_fim=None):
    query = f"{termo} {local}".strip()
    if d_inicio: query += f" after:{d_inicio.strftime('%Y-%m-%d')}"
    if d_fim: query += f" before:{d_fim.strftime('%Y-%m-%d')}"
    
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 4. HEADER
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180" style="filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));">
        <h1 style="font-weight:700; font-size: 2.3rem; margin:10px 0;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; font-weight:400; letter-spacing: 2px;">VALE DOS IPÊS • HUB DE OPORTUNIDADES</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🚀 DIAGNÓSTICO"])

# --- ABA OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    
    with c1:
        perfil = st.selectbox("Busco oportunidades para:", ["Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes"])
    with c2:
        abr = st.selectbox("Abrangência", ["Lavras e Região", "Minas Gerais", "Brasil", "Mundo"], key="abr_op")
    with c3:
        datas_sel = st.date_input("Intervalo de Publicação:", value=(date(2026, 1, 1), date.today()))

    if st.button("MAPEAR OPORTUNIDADES NO PERÍODO"):
        mapa_t = {
            "Empresas Consolidadas": '(chamada "inovação aberta" OR "open innovation" OR "desafio de inovação" OR "edital finep")',
            "Startups": '("inscrições abertas" OR edital OR chamamento) (startup OR aceleração OR aporte OR "investimento anjo")',
            "Empreendedores": '("oportunidade de negócio" OR "edital sebrae" OR "franquia inovadora" OR "crédito inovação")',
            "Estudantes": '("vaga estágio" OR "trainee inovação" OR hackathon OR "bolsa pesquisa" OR "vaga tecnologia")'
        }
        loc_q = {"Lavras e Região": "Lavras MG", "Minas Gerais": "Minas Gerais", "Brasil": "Brasil", "Mundo": ""}[abr]
        
        # Correção do Bug de Seleção Única de Data
        d_i = datas_sel[0] if isinstance(datas_sel, tuple) and len(datas_sel) >= 1 else datas_sel
        d_f = datas_sel[1] if isinstance(datas_sel, tuple) and len(datas_sel) >= 2 else date.today()

        with st.spinner("Escaneando inteligência de mercado..."):
            ops = buscar_dados_com_periodo(mapa_t[perfil], loc_q, d_i, d_f)
            if not ops:
                st.info("Nenhuma oportunidade ativa neste período. Tente ampliar as datas.")
            else:
                for o in sorted(ops, key=lambda x: x.published_parsed, reverse=True)[:20]:
                    dt_o = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
                    st.markdown(f"""
                        <div class="card" style="border-left: 5px solid {COR_VERDE};">
                            <div style="display:flex; justify-content:space-between;"><small style="color:{COR_VERDE}; font-weight:700;">{perfil.upper()}</small><span style="background:{COR_VERDE}33; color:{COR_VERDE}; padding:2px 8px; border-radius:5px; font-size:0.7rem; font-weight:bold;">ATIVO</span></div>
                            <h3 style="margin:10px 0; font-size:1.1rem;">{o.title}</h3>
                            <p style="color:#888; font-size:0.8rem;">📅 Detectado em: {dt_o} • 📍 {abr}</p>
                            <a href="{o.link}" target="_blank" style="color:{COR_VERDE}; text-decoration:none; font-weight:700; font-size:0.8rem;">ACESSAR DETALHES →</a>
                        </div>
                    """, unsafe_allow_html=True)

# --- OUTRAS ABAS (Revisadas) ---
with tabs[0]: # Notícias
    st.markdown("<br>", unsafe_allow_html=True)
    c_n, c_b = st.columns([3, 1])
    with c_n: t_n = st.selectbox("Tema", ["Geral", "Economia", "Inovação", "UFLA", "Rankings"])
    with c_b: 
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("ATUALIZAR NOTÍCIAS"):
            noticias = buscar_dados_com_periodo(f"{t_n} Lavras MG", "", date(2026, 1, 1), date.today())
            for n in sorted(noticias, key=lambda x: x.published_parsed, reverse=True)[:10]:
                st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><h4>{n.title}</h4><a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700;">Ler mais →</a></div>', unsafe_allow_html=True)

with tabs[3]: # Diagnóstico
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;'><h2 style='color:{COR_VERDE};'>Censo Semestral de Inovação</h2></div>", unsafe_allow_html=True)
    with st.expander("Privacidade LGPD"): aceito = st.checkbox("Li e aceito os termos.")
    if aceito:
        with st.form("diag"):
            st.text_input("Nome da Startup")
            if st.form_submit_button("ENVIAR"): st.success("Enviado com sucesso!"); st.balloons()

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA CRONOLÓGICA</p>", unsafe_allow_html=True)