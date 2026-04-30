import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, date, timedelta
import collections

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Radar Vale dos Ipês | Desktop Pro",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILIZAÇÃO CUSTOMIZADA (CSS) - Design Elegante e Escuro
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }
    
    .stApp {
        background-color: #0E1117;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* Cards de Notícias */
    .news-card {
        background-color: #1C2128;
        border: 1px solid #30363D;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .news-card:hover {
        transform: translateY(-2px);
        border-color: #92BC4E;
    }
    .news-tag {
        background-color: rgba(146, 188, 78, 0.1);
        color: #92BC4E;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Formulário - Design Elegante */
    .stForm {
        background-color: #161B22;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #30363D;
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    .stButton>button {
        border-radius: 8px;
        padding: 0.6rem 2rem;
        background-color: #92BC4E !important;
        color: #0E1117 !important;
        font-weight: 700;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #A8D162 !important;
        transform: scale(1.02);
    }

    /* Ajuste de inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #0E1117 !important;
        border: 1px solid #30363D !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE BACKEND ---
def buscar_noticias(query_base, extra="", regiao="Lavras", dias=30):
    mapa_geo = {
        "Lavras": 'Lavras MG OR "Lavras/MG"',
        "Sul de Minas": '"Sul de Minas" OR Varginha OR Pouso Alegre',
        "Minas Gerais": 'Minas Gerais OR MG',
        "Brasil": 'Brasil'
    }
    geo = mapa_geo.get(regiao, "Lavras MG")
    d_ini = (date.today() - timedelta(days=dias)).strftime('%Y-%m-%d')
    q = f"({query_base}) ({geo}) {extra} after:{d_ini}"
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    return feedparser.parse(url).entries

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png", width=160)
    st.markdown("### Painel de Controle")
    regiao_global = st.selectbox("Foco Geográfico", ["Lavras", "Sul de Minas", "Minas Gerais", "Brasil"])
    dias_global = st.slider("Período de Busca (dias)", 7, 180, 30)
    st.markdown("---")
    st.caption("© 2026 Vale dos Ipês - Versão Desktop Pro")

# --- CORPO PRINCIPAL ---
st.title("🌳 Radar de Inteligência")

tab1, tab2, tab3 = st.tabs(["📰 Monitoramento", "🗓️ Agenda", "🚀 Diagnóstico de Startups"])

# ABA 1: MONITORAMENTO
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        extra_query = st.text_input("O que você busca hoje?", placeholder="Ex: Café, Inteligência Artificial, Investimento...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_busca = st.button("EXECUTAR BUSCA")

    if btn_busca:
        with st.spinner("Varrendo o ecossistema..."):
            noticias = buscar_noticias("inovação OR tecnologia OR economia OR edital", extra_query, regiao_global, dias_global)
            if noticias:
                for item in noticias[:15]:
                    st.markdown(f"""
                    <div class="news-card">
                        <span class="news-tag">Oportunidade / Notícia</span>
                        <h4 style="margin-top:10px; color:white;">{item.title}</h4>
                        <p style="font-size:0.85rem; color:#8B949E;">Fonte: {item.source.text}</p>
                        <a href="{item.link}" target="_blank" style="color:#92BC4E; text-decoration:none; font-weight:600;">Ver detalhes →</a>
                    </div>
                    """, unsafe_allow_html=True)

# ABA 2: AGENDA
with tab2:
    st.header("Calendário de Eventos")
    if st.button("BUSCAR EVENTOS PRÓXIMOS"):
        eventos = buscar_noticias("evento OR workshop OR congresso OR meet-up", "", regiao_global, 90)
        for ev in eventos[:10]:
            st.info(f"**{ev.title}**\n\nFonte: {ev.source.text} | [Link]({ev.link})")

# ABA 3: FORMULÁRIO (DIAGNÓSTICO COMPLETO)
with tab3:
    st.header("Diagnóstico e Monitoramento de Startups do Ecossistema de Inovação Vale dos Ipês")
    st.markdown("Preencha o Censo Semestral para monitoramento da maturidade e ações de fomento.")
    
    with st.form("censo_vale_ipes", clear_on_submit=False):
        
        # --- SEÇÃO 1: IDENTIFICAÇÃO ---
        st.markdown("### 1. Identificação e Natureza")
        c1, c2 = st.columns(2)
        with c1:
            nome_startup = st.text_input("Nome da Startup/Projeto *")
            cnpj = st.text_input("CNPJ ou CPF (Fundador) *")
            vertical = st.selectbox("Vertical Principal", ["AgTech", "FoodTech", "HealthTech", "GovTech", "EdTech", "FinTech", "RetailTech", "Outra"])
        with c2:
            fase_maturidade = st.selectbox("Estágio Atual", ["Ideação", "Validação", "Operação (MVP)", "Tração", "Escala"])
            site = st.text_input("Site / Redes Sociais")
            tecnologias = st.multiselect("Tecnologias-Chave", ["IA", "Blockchain", "IoT", "Robótica", "Big Data", "Deep Tech"])
        
        resumo = st.text_area("Descrição da Solução (A dor que resolve e o produto)")

        st.markdown("---")
        
        # --- SEÇÃO 2: EQUIPE E MERCADO ---
        st.markdown("### 2. Sócios e Mercado")
        c3, c4 = st.columns(2)
        with c3:
            num_socios = st.number_input("Número de Fundadores", min_value=1, step=1)
            competencias = st.text_area("Principais competências do time (Negócios, Tech, Operações)")
        with c4:
            mercado_valor = st.text_input("Tamanho do Mercado Alvo (R$)")
            concorrentes = st.text_area("Quem são os principais concorrentes e sua vantagem competitiva?")

        st.markdown("---")

        # --- SEÇÃO 3: TRAÇÃO E FINANCEIRO ---
        st.markdown("### 3. Modelo de Negócio e Tração")
        c5, c6 = st.columns(2)
        with c5:
            faturamento = st.selectbox("Faturamento Bruto Anual", ["Não fatura", "Até R$ 100k", "R$ 100k - R$ 500k", "R$ 500k - R$ 1M", "Acima de R$ 1M"])
            clientes = st.number_input("Quantidade de Clientes Atuais", min_value=0, step=1)
        with c6:
            investimento = st.radio("Investimento Externo já captado?", ["Nenhum", "Anjo", "Seed / Venture Capital", "Fomento Público (Finep/Fapemig)"])
            empregos_lavras = st.text_input("Vagas de emprego diretas em Lavras")

        st.markdown("---")

        # --- SEÇÃO 4: IMPACTO LOCAL ---
        st.markdown("### 4. Lavras: Vale dos Ipês e LVRS+")
        c7, c8 = st.columns(2)
        with c7:
            incentivos = st.multiselect("Interesse em Incentivos Municipais", ["ISS Tecnológico", "Isenção de IPTU", "Sandbox Regulatório"])
        with c8:
            projetos_lvrs = st.multiselect("Projetos do LVRS+ que pretende interagir", ["Cluster AgroFoodTech", "IpêTech", "Cinturão do Alimento", "Escola do Futuro"])
        
        gargalos = st.text_area("O que mais impede o seu crescimento nos próximos 6 meses?")

        # BOTÃO DE SUBMISSÃO
        submit_btn = st.form_submit_button("REGISTRAR DIAGNÓSTICO COMPLETO")
        
        if submit_btn:
            if nome_startup and cnpj:
                st.success(f"Diagnóstico de {nome_startup} registrado com sucesso! Dados consolidados.")
                st.balloons()
            else:
                st.error("Por favor, preencha os campos obrigatórios (Nome e CNPJ/CPF).")

st.markdown("<br><p style='text-align:center; color:#484F58; font-size:0.8rem;'>Radar Vale dos Ipês - Software de Inteligência Local v1.0</p>", unsafe_allow_html=True)