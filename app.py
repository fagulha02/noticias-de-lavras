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

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO (Contraste de Menus e Design Dark)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* CORREÇÃO DE CONTRASTE NOS MENUS */
    div[data-baseweb="select"] > div {{ background-color: #FFFFFF !important; }}
    div[data-baseweb="select"] span {{ color: #000000 !important; font-weight: 600; }}
    div[data-baseweb="popover"] ul {{ background-color: #FFFFFF !important; }}
    div[data-baseweb="popover"] li {{ color: #000000 !important; background-color: #FFFFFF !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #FFFFFF !important; }}

    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}

    div.stButton > button {{
        background-color: transparent; color: white; border: 3px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; text-transform: uppercase;
        margin: 0 auto; display: block; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; box-shadow: 0 0 20px {COR_VERDE}; color: #0E1117 !important; }}

    .header-container {{ text-align: center; padding: 50px 0; border-bottom: 1px solid #333; }}
    .mes-titulo {{ color: {COR_VERDE}; border-bottom: 2px solid #333; padding-bottom: 8px; margin-top: 40px; text-transform: uppercase; font-weight: 700; }}
    .dia-destaque {{ color: {COR_LARANJA}; font-weight: 800; margin-right: 15px; font-size: 1.1rem; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA COM FILTRO TEMPORAL
def buscar_dados(termo, local="", d_inicio=None, d_fim=None):
    query = f"{termo} {local}".strip()
    if d_inicio: query += f" after:{d_inicio.strftime('%Y-%m-%d')}"
    if d_fim: query += f" before:{d_fim.strftime('%Y-%m-%d')}"
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    return feedparser.parse(url).entries

# 4. HEADER
st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
        <h1 style="font-weight:700; margin:10px 0;">Radar de Inteligência</h1>
        <p style="color:{COR_VERDE}; letter-spacing: 2px;">VALE DOS IPÊS • HUB DE OPORTUNIDADES E FUTURO</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# --- ABA 1: NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    c_n1, c_n2 = st.columns([3, 1])
    with c_n1:
        tema_n = st.selectbox("Escolha o tema:", ["Todos", "Geral", "Economia", "Inovação", "UFLA", "Rankings"], key="n_sel")
    with c_n2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        btn_n = st.button("ATUALIZAR NOTÍCIAS", key="btn_n")
    
    if btn_n:
        mapa_n = {
            "Todos": "Lavras MG (inovação OR economia OR UFLA OR ranking)",
            "Geral": "Lavras MG", "Economia": "Lavras MG economia investimentos",
            "Inovação": "Lavras MG inovação tecnologia", "UFLA": "UFLA Lavras", "Rankings": "Lavras MG ranking melhor cidade"
        }
        res_n = buscar_dados(mapa_n[tema_n], "", date.today() - timedelta(days=7))
        for n in sorted(res_n, key=lambda x: x.published_parsed, reverse=True)[:12]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><h4>{n.title}</h4><a href="{n.link}" target="_blank">Ler Notícia →</a></div>', unsafe_allow_html=True)

# --- ABA 2: EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    c_e1, c_e2 = st.columns([3, 1])
    with c_e1:
        loc_e = st.selectbox("Abrangência:", ["Todos", "Lavras", "Minas Gerais", "Brasil", "Mundo"], key="e_sel")
    if st.button("BUSCAR EVENTOS", key="btn_e"):
        loc_q = "" if loc_e == "Todos" else loc_e
        res_e = buscar_dados("eventos tecnologia inovação", loc_q, date.today() - timedelta(days=30))
        for e in sorted(res_e, key=lambda x: x.published_parsed, reverse=True)[:12]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_LARANJA};"><h4>{e.title}</h4><a href="{e.link}" target="_blank">Ver Detalhes →</a></div>', unsafe_allow_html=True)

# --- ABA 3: OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1: perfil_op = st.selectbox("Perfil:", ["Todos", "Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes"])
    with c2: abr_op = st.selectbox("Abrangência", ["Todos", "Lavras e Região", "Minas Gerais", "Brasil"], key="op_abr")
    with c3: data_op = st.date_input("Intervalo:", value=(date(2026, 1, 1), date.today()))

    if st.button("MAPEAR OPORTUNIDADES", key="btn_op"):
        mapa_op = {
            "Todos": '("inscrições abertas" OR edital OR "vaga" OR "chamada") (startup OR inovação OR tecnologia)',
            "Empresas Consolidadas": '(chamada "inovação aberta" OR "open innovation")',
            "Startups": '("inscrições abertas" OR edital) (startup OR aceleração)',
            "Empreendedores": '("oportunidade de negócio" OR "edital sebrae")',
            "Estudantes": '("vaga estágio" OR hackathon OR trainee)'
        }
        loc_q = "" if abr_op == "Todos" else abr_op
        res_o = buscar_dados(mapa_op[perfil_op], loc_q, data_op[0], data_op[1] if len(data_op)>1 else date.today())
        for o in sorted(res_o, key=lambda x: x.published_parsed, reverse=True)[:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><h4>{o.title}</h4><a href="{o.link}" target="_blank">Acessar Edital →</a></div>', unsafe_allow_html=True)

# --- ABA 4: PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    c_p1, c_p2 = st.columns([3, 1])
    with c_p1: cat_p = st.selectbox("Categoria:", ["Todos", "Startups", "Cidades Inteligentes", "Design", "Acadêmica"])
    if st.button("BUSCAR PRÊMIOS", key="btn_p"):
        mapa_p = {
            "Todos": '("vencedores" OR "finalistas" OR "ranking" OR "prêmio") (inovação OR tecnologia)',
            "Startups": '("vencedores" OR "ranking") startup',
            "Cidades Inteligentes": '"prêmio cidade inteligente" OR "smart city"',
            "Design": '"prêmio de design" OR "criatividade"',
            "Acadêmica": '"prêmio pesquisador" OR "tese inovadora"'
        }
        res_p = buscar_dados(mapa_p[cat_p], "Brasil", date(2025,1,1))
        for p in sorted(res_p, key=lambda x: x.published_parsed, reverse=True)[:12]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><h4>{p.title}</h4><a href="{p.link}" target="_blank">Ver Resultado →</a></div>', unsafe_allow_html=True)

# --- ABA 5: CALENDÁRIO ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GERAR CALENDÁRIO 2026"):
        res_cal = buscar_dados('("data do evento" OR "inscrições até" OR "cerimônia")', "Brasil", date(2026,1,1), date(2026,12,31))
        if res_cal:
            st.markdown("<h1 style='text-align:center;'>2026</h1>", unsafe_allow_html=True)
            agenda = collections.defaultdict(list)
            meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            for item in res_cal: agenda[item.published_parsed.tm_mon].append(item)
            for i in range(1, 13):
                if i in agenda:
                    st.markdown(f"<h2 class='mes-titulo'>{meses[i]}</h2>", unsafe_allow_html=True)
                    for ev in sorted(agenda[i], key=lambda x: x.published_parsed.tm_mday):
                        st.markdown(f'<div style="padding:10px 0; border-bottom:1px solid #222;"><span class="dia-destaque">{str(ev.published_parsed.tm_mday).zfill(2)}</span> {ev.title[:120]}...</div>', unsafe_allow_html=True)

# --- ABA 6: DIAGNÓSTICO ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Privacidade LGPD"): aceito = st.checkbox("Li e aceito os termos.")
    if aceito:
        with st.form("diag"):
            st.text_input("Nome da Startup")
            if st.form_submit_button("ENVIAR"): st.success("Enviado com sucesso!"); st.balloons()

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA 2026</p>", unsafe_allow_html=True)