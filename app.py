import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. IDENTIDADE VISUAL (Dark Mode Premium - Vale dos Ipês)
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO (Elegância e Contraste)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}

    /* Correção de Contraste nos Menus */
    div[data-baseweb="select"] > div {{ background-color: #161B22 !important; color: white !important; }}
    div[data-baseweb="select"] span {{ color: white !important; }}
    div[data-baseweb="popover"] ul {{ background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li {{ color: white !important; background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}

    /* Cards Estilizados com Gradiente Sutil */
    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }}

    /* Botões Customizados */
    div.stButton > button {{
        background-color: transparent;
        color: white;
        border: 3px solid {COR_VERDE} !important;
        border-radius: 50px;
        padding: 10px 40px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.4s;
        display: block;
        margin: 0 auto;
    }}
    
    div.stButton > button:hover {{
        background-color: {COR_VERDE} !important;
        box-shadow: 0 0 20px {COR_VERDE};
        color: #0E1117 !important;
    }}

    .header-container {{ text-align: center; padding: 60px 0; background: linear-gradient(180deg, #161B22 0%, #0E1117 100%); border-bottom: 1px solid #333; }}
    .logo-img {{ filter: drop-shadow(0 0 15px rgba(255,255,255,0.2)); margin-bottom: 20px; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA AVANÇADO
def buscar_dados(termo, local="", periodo="1m"):
    query = f"{termo} {local}".strip()
    query_encoded = urllib.parse.quote(query)
    # Parâmetro 'when' garante a atualidade das oportunidades
    url = f"https://news.google.com/rss/search?q={query_encoded}+when:{periodo}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries

# 4. HEADER
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="220" class="logo-img">
        <h1 style="font-weight:700; font-size: 2.6rem; margin:0;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; font-weight:400; font-size: 1.2rem; letter-spacing: 2px;">VALE DOS IPÊS • LAVRAS/MG</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🚀 DIAGNÓSTICO"])

# --- ABA 1: NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        topico_n = st.selectbox("Tópico de Notícia", ["Geral", "Economia", "Inovação", "UFLA & Educação", "Saúde", "Rankings"])
        btn_n = st.button("ATUALIZAR NOTÍCIAS", key="btn_n")
    
    if btn_n:
        mapa_n = {"Geral": "Lavras MG", "Economia": "investimento startup Lavras", "Inovação": "tecnologia inovação Lavras", "UFLA & Educação": "UFLA educação Lavras", "Saúde": "saúde hospital Lavras", "Rankings": "ranking melhores cidades Lavras MG"}
        with st.spinner("Buscando fatos recentes..."):
            noticias = buscar_dados(mapa_n[topico_n], periodo="7d")
            res_n = sorted(noticias, key=lambda x: x.published_parsed, reverse=True)
            for n in res_n[:12]:
                dt = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
                st.markdown(f"""<div class="card" style="border-left: 5px solid {COR_AZUL};"><small style="color:{COR_AZUL}; font-weight:700;">{topico_n.upper()}</small><h3 style="margin:10px 0; font-size:1.2rem;">{n.title}</h3><p style="color:#888; font-size:0.85rem;">📅 {dt}</p><a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700;">LER MAIS →</a></div>""", unsafe_allow_html=True)

# --- ABA 2: EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid_e, _ = st.columns([1, 2, 1])
    with col_mid_e:
        loc_e = st.selectbox("Abrangência Regional", ["Lavras", "Minas Gerais", "Brasil", "Mundo"])
        btn_e = st.button("BUSCAR EVENTOS", key="btn_e")
    
    if btn_e:
        with st.spinner("Mapeando agenda..."):
            eventos = buscar_dados("eventos tecnologia inovação", loc_e, "1m")
            res_e = sorted(eventos, key=lambda x: x.published_parsed, reverse=True)
            for e in res_e[:10]:
                dt_e = datetime(*e.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""<div class="card" style="border-left: 5px solid {COR_LARANJA};"><small style="color:{COR_LARANJA}; font-weight:700;">{loc_e.upper()}</small><h3 style="margin:10px 0; font-size:1.2rem;">{e.title}</h3><p style="color:#888; font-size:0.85rem;">📅 Divulgado em: {dt_e}</p><a href="{e.link}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 25px; background:{COR_LARANJA}; color:white; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:700;">VER DETALHES</a></div>""", unsafe_allow_html=True)

# --- ABA 3: OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: perfil = st.selectbox("Para quem busca?", ["Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes"])
    with c2: abr = st.selectbox("Abrangência", ["Lavras e Região", "Minas Gerais", "Brasil", "Mundo"], key="abr_op")
    with c3: tempo = st.selectbox("Publicado há:", ["7 dias", "30 dias", "90 dias"])

    if st.button("MAPEAR OPORTUNIDADES ATIVAS"):
        mapa_t = {
            "Empresas Consolidadas": '(chamada "inovação aberta" OR "open innovation" OR "desafio de inovação")',
            "Startups": '("inscrições abertas" OR edital) (startup OR aceleração OR aporte OR "investimento anjo")',
            "Empreendedores": '("oportunidade de negócio" OR "edital sebrae" OR "crédito inovação")',
            "Estudantes": '("vaga estágio" OR hackathon OR "bolsa pesquisa" OR "vaga tecnologia")'
        }
        loc_q = {"Lavras e Região": "Lavras MG", "Minas Gerais": "Minas Gerais", "Brasil": "Brasil", "Mundo": ""}[abr]
        tmp_q = {"7 dias": "7d", "30 dias": "1m", "90 dias": "3m"}[tempo]

        with st.spinner("Filtrando editais e vagas..."):
            ops = buscar_dados(mapa_t[perfil], loc_q, tmp_q)
            res_o = sorted(ops, key=lambda x: x.published_parsed, reverse=True)
            for o in res_o[:15]:
                dt_o = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""
                    <div class="card" style="border-left: 5px solid {COR_VERDE};">
                        <div style="display:flex; justify-content:space-between;"><small style="color:{COR_VERDE}; font-weight:700;">{perfil.upper()}</small><span style="background:{COR_VERDE}22; color:{COR_VERDE}; padding:2px 8px; border-radius:5px; font-size:0.7rem; font-weight:bold;">ATIVO</span></div>
                        <h3 style="margin:10px 0; font-size:1.2rem;">{o.title}</h3>
                        <p style="color:#888; font-size:0.85rem;">📅 Detectado em: {dt_o}</p>
                        <a href="{o.link}" target="_blank" style="display:inline-block; padding:10px 30px; background:{COR_VERDE}; color:#0E1117; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:700;">ACESSAR OPORTUNIDADE</a>
                    </div>
                """, unsafe_allow_html=True)

# --- ABA 4: DIAGNÓSTICO (LGPD) ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;'><h2 style='color:{COR_VERDE};'>Censo Semestral de Inovação</h2><p>Diagnóstico de Startups — Vale dos Ipês</p></div>", unsafe_allow_html=True)
    with st.expander("🔒 Consentimento & Privacidade (LGPD)", expanded=True):
        c1 = st.checkbox("Autorizo o tratamento de dados empresariais para políticas públicas.")
        c2 = st.checkbox("Autorizo o tratamento de dados pessoais dos sócios para contato.")
        c3 = st.checkbox("Estou ciente do uso de dados anonimizados em relatórios.")
    
    if c1 and c2 and c3:
        with st.form("form_diag"):
            n_st = st.text_input("Nome da Startup *")
            socio_e = st.text_input("E-mail de contato *")
            vert = st.selectbox("Vertical", ["AgriTech", "HealthTech", "FinTech", "EdTech", "Outro"])
            if st.form_submit_button("ENVIAR DIAGNÓSTICO") and n_st:
                st.success("✔ Diagnóstico enviado com sucesso!"); st.balloons()
    else: st.info("⚠ Aceite os termos de privacidade para liberar o formulário.")

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA CRONOLÓGICA</p>", unsafe_allow_html=True)