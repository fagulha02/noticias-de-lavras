import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, timedelta

# 1. IDENTIDADE VISUAL
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS (Com correção de contraste e design dark)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    div[data-baseweb="select"] > div {{ background-color: #161B22 !important; color: white !important; }}
    div[data-baseweb="select"] span {{ color: white !important; }}
    div[data-baseweb="popover"] ul {{ background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li {{ color: white !important; background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}
    .card {{ background: {COR_FUNDO_CARD}; padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s; }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}
    div.stButton > button {{ background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important; border-radius: 50px; padding: 10px 40px; font-weight: 700; text-transform: uppercase; transition: 0.4s; display: block; margin: 0 auto; }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 20px {COR_VERDE}; color: #0E1117 !important; }}
    .header-container {{ text-align: center; padding: 40px 0; background: linear-gradient(180deg, #161B22 0%, #0E1117 100%); border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA AVANÇADO
def buscar_dados(termo, local="", periodo="1m"):
    # periodo: 1d (últimas 24h), 7d (última semana), 1m (último mês)
    query = f"{termo} {local}".strip()
    query_encoded = urllib.parse.quote(query)
    # Adicionando o parâmetro 'when' para garantir oportunidades recentes
    url = f"https://news.google.com/rss/search?q={query_encoded}+when:{periodo}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
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

# --- ABA OPORTUNIDADES (REFORÇADA) ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        perfil = st.selectbox("Para quem busca?", 
                            ["Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes", "Todas"])
    with c2:
        abrangencia = st.selectbox("Onde?", ["Lavras e Região", "Minas Gerais", "Brasil", "Mundo"])
    with c3:
        tempo = st.selectbox("Publicado há:", ["7 dias", "30 dias", "90 dias"])

    btn_op = st.button("BUSCAR OPORTUNIDADES ATIVAS")

    if btn_op:
        # Dicionário de termos ultra-específicos para evitar "lixo" antigo
        mapa_termos = {
            "Empresas Consolidadas": '(chamada "inovação aberta" OR "open innovation" OR "desafio de inovação" OR "edital finep")',
            "Startups": '("inscrições abertas" OR edital OR chamamento) (startup OR aceleração OR aporte OR "investimento anjo")',
            "Empreendedores": '("oportunidade de negócio" OR "edital sebrae" OR "franquia inovadora" OR "crédito inovação")',
            "Estudantes": '("vaga estágio" OR "trainee inovação" OR hackathon OR "bolsa pesquisa" OR "vaga tecnologia")',
            "Todas": '("inscrições abertas" OR "edital aberto" OR "oportunidade" OR "vaga") (inovação OR startup OR tecnologia)'
        }
        
        mapa_loc = {
            "Lavras e Região": "Lavras Sul de Minas",
            "Minas Gerais": "Minas Gerais",
            "Brasil": "Brasil",
            "Mundo": ""
        }
        
        mapa_tempo = {"7 dias": "7d", "30 dias": "1m", "90 dias": "3m"}

        with st.spinner("Filtrando oportunidades recentes e editais ativos..."):
            resultados = buscar_dados(mapa_termos[perfil], mapa_loc[abrangencia], mapa_tempo[tempo])
            
            if not resultados:
                st.info("Nenhuma oportunidade ativa encontrada para este período. Tente aumentar o filtro de tempo.")
            else:
                # Ordenação cronológica garantida
                res_ord = sorted(resultados, key=lambda x: x.published_parsed, reverse=True)
                
                for r in res_ord[:20]:
                    data_pub = datetime(*r.published_parsed[:6]).strftime('%d/%m/%Y')
                    
                    # Interface do Card de Oportunidade
                    st.markdown(f"""
                        <div class="card" style="border-left: 5px solid {COR_VERDE};">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <span style="color:{COR_VERDE}; font-weight:700; font-size:0.8rem;">DISPONÍVEL EM: {abrangencia.upper()}</span>
                                <span style="background:{COR_VERDE}33; color:{COR_VERDE}; padding:2px 8px; border-radius:5px; font-size:0.7rem; font-weight:bold;">ATIVO</span>
                            </div>
                            <h3 style="margin:10px 0; font-size:1.2rem; line-height:1.4;">{r.title}</h3>
                            <p style="color:#888; font-size:0.85rem; margin-bottom:15px;">
                                📅 Postado em: {data_pub} <br>
                                📍 Local: {abrangencia}
                            </p>
                            <a href="{r.link}" target="_blank" 
                               style="display:inline-block; padding:10px 25px; background:{COR_VERDE}; color:#0E1117; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:700;">
                               ACESSAR EDITAL / VAGA
                            </a>
                        </div>
                    """, unsafe_allow_html=True)

# As outras abas (Notícias, Eventos, Diagnóstico) devem seguir o mesmo padrão visual.