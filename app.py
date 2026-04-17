import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date
import collections

# 1. IDENTIDADE VISUAL (Dark Mode Premium - Vale dos Ipês)
COR_VERDE = "#92BC4E"
COR_LARANJA = "#EB6923"
COR_AZUL = "#00ADEF"
COR_OURO = "#FFD700" 
COR_TEXTO = "#E0E0E0"
COR_FUNDO_CARD = "#1E2129"

st.set_page_config(page_title="Radar Vale dos Ipês", layout="wide", page_icon="🌳")

# 2. CSS AVANÇADO (Design, Calendário e Contraste)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}

    /* Títulos das Abas */
    button[data-baseweb="tab"] {{ font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }}

    /* Estilização de Menus (Selectbox) */
    div[data-baseweb="select"] > div {{ background-color: #161B22 !important; color: white !important; }}
    div[data-baseweb="select"] span {{ color: white !important; }}
    div[data-baseweb="popover"] ul {{ background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li {{ color: white !important; background-color: #161B22 !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; }}
    
    /* Estilo Calendário */
    .mes-titulo {{ color: {COR_VERDE}; border-bottom: 2px solid #333; padding-bottom: 8px; margin-top: 40px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }}
    .evento-item {{ padding: 12px 0; border-bottom: 1px solid #222; font-size: 1rem; display: flex; align-items: center; }}
    .dia-destaque {{ color: {COR_LARANJA}; font-weight: 800; margin-right: 20px; font-size: 1.2rem; min-width: 35px; border-right: 2px solid #333; padding-right: 10px; }}
    .tag-cal {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; margin-left: 10px; font-weight: 600; text-transform: uppercase; }}

    .card {{
        background: linear-gradient(145deg, #1E2129, #161B22);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }}

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
def buscar_dados(termo, local="", d_inicio=None, d_fim=None):
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
        <p style="color:{COR_VERDE}; font-weight:400; letter-spacing: 2px;">VALE DOS IPÊS • LAVRAS/MG</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

# --- ABA 1: NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ATUALIZAR NOTÍCIAS DO DIA"):
        with st.spinner("Buscando fatos..."):
            noticias = buscar_dados("Lavras MG inovação", "", date.today())
            if noticias:
                for n in noticias[:10]:
                    st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><h4>{n.title}</h4><a href="{n.link}" target="_blank" style="color:{COR_AZUL}; font-weight:700; text-decoration:none;">LER NOTÍCIA →</a></div>', unsafe_allow_html=True)
            else:
                st.info("Nenhuma notícia de última hora encontrada.")

# --- ABA 2: EVENTOS ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Consulte a aba de Calendário para ver a agenda completa do ano.")

# --- ABA 3: OPORTUNIDADES ---
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1: perfil_op = st.selectbox("Busco oportunidades para:", ["Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes"])
    with c2: abr_op = st.selectbox("Abrangência", ["Lavras e Região", "Minas Gerais", "Brasil", "Mundo"], key="abr_op")
    with c3: data_op = st.date_input("Intervalo de Inscrição:", value=(date(2026, 1, 1), date.today()), key="data_op")

    if st.button("MAPEAR OPORTUNIDADES", key="btn_op"):
        mapa_op = {
            "Empresas Consolidadas": '(chamada "inovação aberta" OR "open innovation" OR "desafio")',
            "Startups": '("inscrições abertas" OR edital) (startup OR aceleração OR aporte)',
            "Empreendedores": '("oportunidade de negócio" OR "edital sebrae" OR "crédito inovação")',
            "Estudantes": '("vaga estágio" OR hackathon OR "bolsa pesquisa" OR trainee)'
        }
        loc_op = {"Lavras e Região": "Lavras MG", "Minas Gerais": "Minas Gerais", "Brasil": "Brasil", "Mundo": ""}[abr_op]
        d_i = data_op[0] if len(data_op) >= 1 else date(2026,1,1)
        d_f = data_op[1] if len(data_op) >= 2 else date.today()
        
        with st.spinner("Escaneando editais..."):
            res = buscar_dados(mapa_op[perfil_op], loc_op, d_i, d_f)
            for o in sorted(res, key=lambda x: x.published_parsed, reverse=True)[:15]:
                dt = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f'<div class="card" style="border-left: 5px solid {COR_VERDE};"><small style="color:{COR_VERDE}; font-weight:700;">OPORTUNIDADE ATIVA</small><h3 style="margin:10px 0; font-size:1.1rem;">{o.title}</h3><p style="color:#888; font-size:0.8rem;">📅 Detectado em: {dt}</p><a href="{o.link}" target="_blank" style="color:{COR_VERDE}; text-decoration:none; font-weight:700;">VER DETALHES →</a></div>', unsafe_allow_html=True)

# --- ABA 4: PREMIAÇÕES ---
with tabs[3]:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("BUSCAR RECONHECIMENTOS"):
        with st.spinner("Mapeando conquistas..."):
            premios = buscar_dados('("vencedores" OR "finalistas" OR "ranking") (startup OR inovação)', "Brasil", date(2025,1,1))
            for p in sorted(premios, key=lambda x: x.published_parsed, reverse=True)[:10]:
                st.markdown(f'<div class="card" style="border-left: 5px solid {COR_OURO};"><small style="color:{COR_OURO}; font-weight:700;">🏆 PREMIAÇÃO</small><h4>{p.title}</h4><a href="{p.link}" target="_blank" style="color:{COR_OURO}; text-decoration:none; font-weight:700;">VER RESULTADOS →</a></div>', unsafe_allow_html=True)

# --- ABA 5: CALENDÁRIO (IMPLEMENTAÇÃO COMPLETA) ---
with tabs[4]:
    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        tipos_cal = st.multiselect("Filtrar categorias da agenda:", ["Eventos", "Editais", "Premiações"], default=["Eventos", "Editais"])
    with col_c2:
        reg_cal = st.selectbox("Região do Calendário:", ["Lavras e Região", "Minas Gerais", "Brasil", "Mundo"])

    if st.button("GERAR CRONOGRAMA 2026"):
        termos_cal = []
        if "Eventos" in tipos_cal: termos_cal.append('("data do evento" OR "acontece dia" OR meetup)')
        if "Editais" in tipos_cal: termos_cal.append('("inscrições até" OR "prazo final" OR "abertura")')
        if "Premiações" in tipos_cal: termos_cal.append('("cerimônia" OR "vencedores" OR "entrega")')
        
        query_cal = " OR ".join(termos_cal)
        loc_cal = {"Lavras e Região": "Lavras MG", "Minas Gerais": "Minas Gerais", "Brasil": "Brasil", "Mundo": ""}[reg_cal]
        
        with st.spinner("Construindo linha do tempo estratégica..."):
            res_cal = buscar_dados(query_cal, loc_cal, date(2026, 1, 1), date(2026, 12, 31))
            
            if not res_cal:
                st.warning("Ainda não detectamos marcos cronológicos específicos para esses filtros.")
            else:
                st.markdown("<h1 style='text-align:center; color:#FFF;'>📅 2026</h1>", unsafe_allow_html=True)
                meses_lista = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                agenda_mensal = collections.defaultdict(list)
                
                for item in res_cal:
                    mes_idx = item.published_parsed.tm_mon
                    agenda_mensal[mes_idx].append(item)
                
                # Exibição do Calendário
                for i in range(1, 13):
                    if i in agenda_mensal:
                        st.markdown(f"<h2 class='mes-titulo'>{meses_lista[i]}</h2>", unsafe_allow_html=True)
                        for ev in sorted(agenda_mensal[i], key=lambda x: x.published_parsed.tm_mday):
                            dia_num = str(ev.published_parsed.tm_mday).zfill(2)
                            # Tag colorida baseada no título
                            cor_tag = COR_LARANJA if "evento" in ev.title.lower() else COR_VERDE
                            st.markdown(f"""
                                <div class="evento-item">
                                    <span class="dia-destaque">{dia_num}</span> 
                                    <div style="flex-grow:1;">
                                        <a href="{ev.link}" target="_blank" style="text-decoration:none; color:{COR_TEXTO}; font-weight:500;">
                                            {ev.title[:120]}...
                                        </a>
                                    </div>
                                    <span class="tag-cal" style="background:{cor_tag}22; color:{cor_tag}; border: 1px solid {cor_tag}55;">AGENDA</span>
                                </div>
                            """, unsafe_allow_html=True)

# --- ABA 6: DIAGNÓSTICO ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Censo Semestral de Inovação - Coleta em conformidade com a LGPD.")
    with st.form("form_startup_censo"):
        n_st = st.text_input("Nome da Startup")
        submit = st.form_submit_button("Enviar")
        if submit and n_st:
            st.success("Diagnóstico registrado com sucesso!")

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA CRONOLÓGICA</p>", unsafe_allow_html=True)