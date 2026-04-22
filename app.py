import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# 1. CONFIGURAÇÕES E IDENTIDADE VISUAL
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_OURO = "#FFD700"
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO (Otimização de Contraste e Cards)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* CORREÇÃO DE CONTRASTE: Selectbox com fundo branco e texto preto para legibilidade máxima */
    div[data-baseweb="select"] > div {{ background-color: #FFFFFF !important; border-radius: 8px !important; }}
    div[data-baseweb="select"] span {{ color: #000000 !important; font-weight: 600 !important; }}
    div[data-baseweb="popover"] ul {{ background-color: #FFFFFF !important; }}
    div[data-baseweb="popover"] li {{ color: #000000 !important; background-color: #FFFFFF !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #FFFFFF !important; }}

    /* Cards com profundidade e hover */
    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.5); }}

    /* Botões Padrão Vale */
    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 45px; font-weight: 700; text-transform: uppercase;
        margin: 0 auto; display: block; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 25px {COR_VERDE}; color: #0E1117 !important; }}

    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; }}
    .mes-titulo {{ color: {COR_VERDE}; border-bottom: 2px solid #333; padding-bottom: 8px; margin-top: 35px; text-transform: uppercase; }}
    .header-container {{ text-align: center; padding: 40px 0; border-bottom: 1px solid #333; margin-bottom: 30px; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA UNIFICADO
def fetch_radar_data(termo, local="", d_inicio=None, d_fim=None):
    query = f"{termo} {local}".strip()
    if d_inicio: query += f" after:{d_inicio.strftime('%Y-%m-%d')}"
    if d_fim: query += f" before:{d_fim.strftime('%Y-%m-%d')}"
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)

# 4. HEADER CENTRAL
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
        <h1 style="font-weight:700; margin-top:15px;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; letter-spacing: 2px; font-size:1.1rem;">VALE DOS IPÊS • LAVRAS/MG</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# --- ABA 1: NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: tema_n = st.selectbox("Tema:", ["Todos", "Geral", "Economia", "Inovação", "UFLA", "Rankings"], key="n_tema")
    with c2: d_ini_n = st.date_input("De:", value=date.today() - timedelta(days=7), key="n_ini")
    with c3: d_fim_n = st.date_input("Até:", value=date.today(), key="n_fim")
    
    if st.button("BUSCAR NOTÍCIAS", key="btn_not"):
        mapa = {
            "Todos": "Lavras MG (inovação OR economia OR UFLA OR prefeitura)",
            "Geral": "Lavras MG", "Economia": "Lavras MG economia", "Inovação": "Lavras MG tecnologia", 
            "UFLA": "UFLA Lavras", "Rankings": "Lavras MG ranking"
        }
        res = fetch_radar_data(mapa[tema_n], "", d_ini_n, d_fim_n)
        if res:
            for n in res[:15]:
                dt = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
                st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3 style="margin:10px 0; font-size:1.15rem;">{n.title}</h3><p style="color:#888; font-size:0.8rem;">📅 {dt}</p><a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700;">LER AGORA →</a></div>', unsafe_allow_html=True)
        else: st.info("Sem notícias no período.")

# --- ABA 2: EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    c_e1, c_e2 = st.columns([2, 2])
    with c_e1: loc_e = st.selectbox("Onde buscamos eventos?", ["Todos", "Lavras", "Minas Gerais", "Brasil"], key="e_loc")
    with c_e2: d_ini_e = st.date_input("A partir de:", value=date.today() - timedelta(days=30), key="e_ini")
    
    if st.button("MAPEAR EVENTOS", key="btn_eve"):
        loc_q = "Lavras MG" if loc_e == "Lavras" else ("" if loc_e == "Todos" else loc_e)
        res = fetch_radar_data('("evento" OR "meetup" OR "congresso") (tecnologia OR inovação)', loc_q, d_ini_e)
        for e in res[:15]:
            dt = datetime(*e.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_LARANJA};"><span class="badge" style="background:{COR_LARANJA}33; color:{COR_LARANJA};">Evento</span><h3 style="margin:10px 0; font-size:1.15rem;">{e.title}</h3><p style="color:#888; font-size:0.8rem;">📅 Divulgado em: {dt}</p><a href="{e.link}" target="_blank" style="color:{COR_LARANJA}; text-decoration:none; font-weight:700;">VER DETALHES →</a></div>', unsafe_allow_html=True)

# --- ABA 3: OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: perfil_op = st.selectbox("Para quem?", ["Todos", "Startups", "Empresas Consolidadas", "Estudantes", "Empreendedores"], key="o_per")
    with c2: d_ini_o = st.date_input("Publicado após:", value=date(2026, 1, 1), key="o_ini")
    with c3: abr_op = st.selectbox("Região:", ["Todos", "Lavras e Região", "Minas Gerais", "Brasil"], key="o_abr")
    
    if st.button("BUSCAR OPORTUNIDADES", key="btn_op"):
        mapa_o = {
            "Todos": '("edital" OR "vaga" OR "chamada") (inovação OR tecnologia)',
            "Startups": '("edital" OR "inscrições") (startup OR aceleração)',
            "Empresas Consolidadas": '"inovação aberta" OR "desafio corporativo"',
            "Estudantes": '"vaga estágio" OR hackathon OR trainee',
            "Empreendedores": '"oportunidade" OR "crédito inovação" OR sebrae'
        }
        loc_q = "" if abr_op == "Todos" else abr_op
        res = fetch_radar_data(mapa_o[perfil_op], loc_q, d_ini_o)
        for o in res[:15]:
            dt = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><span class="badge" style="background:{COR_VERDE}33; color:{COR_VERDE};">Oportunidade</span><h3 style="margin:10px 0; font-size:1.15rem;">{o.title}</h3><p style="color:#888; font-size:0.8rem;">📅 Postado em: {dt}</p><a href="{o.link}" target="_blank" style="color:{COR_VERDE}; text-decoration:none; font-weight:700;">ACESSAR EDITAL →</a></div>', unsafe_allow_html=True)

# --- ABA 4: PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    c_p1, c_p2 = st.columns([3, 1])
    with c_p1: cat_p = st.selectbox("Filtrar Categoria:", ["Todos", "Startups", "Cidades Inteligentes", "Acadêmico"], key="p_cat")
    if st.button("BUSCAR PRÊMIOS", key="btn_pre"):
        mapa_p = {
            "Todos": '("vencedores" OR "ranking" OR "prêmio") (inovação OR tecnologia)',
            "Startups": '("vencedores" OR "finalistas") startup',
            "Cidades Inteligentes": '"smart city" OR "cidade inteligente"',
            "Acadêmico": '"pesquisador" OR "tese inovadora" OR ufla'
        }
        res = fetch_radar_data(mapa_p[cat_p], "Brasil", date(2025, 1, 1))
        for p in res[:12]:
            dt = datetime(*p.published_parsed[:6]).strftime('%d/%m/%Y')
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><span class="badge" style="background:{COR_OURO}33; color:{COR_OURO};">Premiação</span><h3 style="margin:10px 0; font-size:1.15rem;">{p.title}</h3><p style="color:#888; font-size:0.8rem;">📅 Divulgado em: {dt}</p><a href="{p.link}" target="_blank" style="color:{COR_OURO}; text-decoration:none; font-weight:700;">VER RESULTADO →</a></div>', unsafe_allow_html=True)

# --- ABA 5: CALENDÁRIO ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    reg_c = st.selectbox("Região do Cronograma:", ["Brasil", "Lavras", "Minas Gerais"], key="c_reg")
    if st.button("GERAR CALENDÁRIO 2026"):
        res = fetch_radar_data('("data" OR "até dia" OR "cerimônia" OR "inscrições")', reg_c, date(2026, 1, 1), date(2026, 12, 31))
        if res:
            st.markdown("<h1 style='text-align:center;'>2026</h1>", unsafe_allow_html=True)
            agenda = collections.defaultdict(list)
            meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            for item in res: agenda[item.published_parsed.tm_mon].append(item)
            for i in range(1, 13):
                if i in agenda:
                    st.markdown(f"<h2 class='mes-titulo'>{meses[i]}</h2>", unsafe_allow_html=True)
                    for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                        st.markdown(f'<div style="padding:12px 0; border-bottom:1px solid #222; display:flex; align-items:center;"><span style="color:{COR_LARANJA}; font-weight:800; margin-right:15px; min-width:30px;">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title}</div>', unsafe_allow_html=True)

# --- ABA 6: DIAGNÓSTICO ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Privacidade LGPD - Censo Semestral"):
        aceito = st.checkbox("Li e aceito os termos de tratamento de dados estratégicos.")
    if aceito:
        with st.form("form_diag"):
            st.text_input("Nome da Startup")
            st.selectbox("Vertical", ["AgriTech", "HealthTech", "FinTech", "Outro"])
            if st.form_submit_button("ENVIAR DIAGNÓSTICO"): st.success("Enviado com sucesso!"); st.balloons()

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA 2026</p>", unsafe_allow_html=True)