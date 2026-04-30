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

# 2. CSS DE ALTO CONTRASTE & DESIGN ELEGANTE
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* Customização das Abas */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }}

    /* Estilo dos Cards */
    .card {{ 
        background: linear-gradient(145deg, #1E2129, #161B22); 
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; 
        transition: 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }}
    
    /* Botões Arredondados e Elegantes */
    div.stButton > button {{
        background-color: transparent; color: white; border: 2px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; width: 100%; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; box-shadow: 0 0 15px {COR_VERDE}; }}

    /* Estilo do Formulário */
    .stForm {{ background-color: #161B22; border: 1px solid #333; border-radius: 15px; padding: 30px; }}
    h1, h2, h3 {{ color: #FFFFFF !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA (Injeção Geográfica Inteligente)
def fetch_radar_data(termo_base, extra_v="", regiao="Lavras", d_ini=None, d_fim=None):
    mapa_geo = {
        "Lavras": '(Lavras MG OR "Lavras/MG")',
        "Sul de Minas": '("Sul de Minas" OR Varginha OR "Pouso Alegre")',
        "Minas Gerais": '("Minas Gerais" OR MG)',
        "Brasil": "Brasil"
    }
    geo_query = mapa_geo.get(regiao, mapa_geo["Lavras"])
    query = f"({termo_base}) AND ({geo_query})"
    if extra_v: query += f" AND ({extra_v})"
    
    d_ini = d_ini if d_ini else date.today() - timedelta(days=30)
    d_fim = d_fim if d_fim else date.today()
    query += f" after:{d_ini.strftime('%Y-%m-%d')} before:{d_fim.strftime('%Y-%m-%d')}"
    
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)

# 4. HEADER
st.markdown(f"""<div style="text-align:center; padding: 30px 0;">
    <img src="https://raw.githubusercontent.com/fagulha02/noticias-de-lavras/main/logo_vale.png" width="180">
    <h1 style="margin-top:15px; font-size: 2.5rem;">Radar de Inteligência</h1>
    <p style="color:{COR_VERDE}; letter-spacing: 3px; font-weight: 400;">VALE DOS IPÊS • HUB DE OPORTUNIDADES</p>
</div>""", unsafe_allow_html=True)

if 'db' not in st.session_state: st.session_state.db = {}

tabs = st.tabs(["📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🏆 PREMIAÇÕES", "🗓️ CALENDÁRIO", "🚀 DIAGNÓSTICO"])

def render_filtros(key_prefix, default_days=30):
    c_geo, c_ex, c_d1, c_d2, c_btn = st.columns([1.2, 1.5, 1, 1, 1])
    with c_geo: reg = st.selectbox("Região:", ["Lavras", "Sul de Minas", "Minas Gerais", "Brasil"], key=f"geo_{key_prefix}")
    with c_ex: extra = st.text_input("🔍 Palavra-chave:", key=f"ex_{key_prefix}")
    with c_d1: ini = st.date_input("De:", value=date.today() - timedelta(days=default_days), key=f"ini_{key_prefix}")
    with c_d2: fim = st.date_input("Até:", value=date.today(), key=f"fim_{key_prefix}")
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    return reg, extra, ini, fim, c_btn

# --- ABA NOTÍCIAS ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    tema = st.selectbox("Tópico Base:", ["Todos", "Economia", "Inovação", "UFLA"], key="n_tema")
    reg, extra, d_i, d_f, c_btn = render_filtros("not", 7)
    if c_btn.button("BUSCAR", key="btn_not"):
        mapa = {"Todos": "inovação OR tecnologia OR economia", "Economia": "economia OR mercado", "Inovação": "inovação OR startups", "UFLA": "UFLA"}
        st.session_state.db['n'] = fetch_radar_data(mapa[tema], extra, reg, d_i, d_f)
    if 'n' in st.session_state.db:
        for item in st.session_state.db['n'][:15]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Ler mais →</a></div>', unsafe_allow_html=True)

# --- ABA DIAGNÓSTICO (O FORMULÁRIO COMPLETO) ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Diagnóstico e Monitoramento de Startups do Ecossistema de Inovação Vale dos Ipês")
    st.info("Preencha o Censo Semestral para monitoramento da maturidade e ações de fomento.")
    
    with st.form("diagnostico_censo"):
        st.markdown("### 1. Informações Gerais e Localização")
        c1, c2 = st.columns(2)
        with c1:
            nome_st = st.text_input("Nome da Startup/Projeto *")
            cnpj_cpf = st.text_input("CNPJ ou CPF (Fundador) *")
            origem = st.selectbox("Origem do Projeto", ["Ideia própria", "Spin-off acadêmica", "Hackathon/Evento", "Transferência Tecnológica", "Outro"])
        with c2:
            vertical = st.selectbox("Vertical de Atuação", ["AgTech", "FoodTech", "HealthTech", "GovTech", "EdTech", "FinTech", "Outra"])
            fase = st.selectbox("Fase Atual", ["Ideação", "Validação", "Operação (MVP)", "Tração", "Escala"])
            tecnologias = st.multiselect("Tecnologias Utilizadas", ["IA", "Blockchain", "IoT", "Robótica", "Big Data", "Cloud Computing"])
        
        st.text_area("Resumo da Solução (O que vocês resolvem?)")
        st.text_input("Endereço da Operação (Em Lavras)")

        st.markdown("---")
        st.markdown("### 2. Mercado, Modelo e Tração")
        c3, c4 = st.columns(2)
        with c3:
            faturamento = st.selectbox("Faturamento Bruto Anual", ["Ainda não fatura", "Até R$ 100k", "R$ 100k - R$ 500k", "Acima de R$ 1M"])
            clientes = st.number_input("Quantidade de Clientes Ativos", min_value=0, step=1)
        with c4:
            investimento = st.radio("Já captou investimento externo?", ["Não", "Sim (Anjo)", "Sim (Fundo/VC)", "Sim (Fomento Público)"])
            vagas = st.text_input("Vagas de emprego diretas hoje em Lavras")

        st.markdown("---")
        st.markdown("### 3. Lavras: Vale dos Ipês e LVRS+")
        st.multiselect("Interesse em Incentivos Municipais", ["ISS Tecnológico", "Isenção de IPTU", "Sandbox Regulatório"])
        st.multiselect("Com quais projetos do LVRS+ pretende interagir?", ["Cluster AgroFoodTech", "IpêTech", "Cinturão do Alimento", "Escola do Futuro"])
        
        st.text_area("Qual o maior gargalo atual para o crescimento nos próximos 6 meses?")

        if st.form_submit_button("REGISTRAR DIAGNÓSTICO"):
            if nome_st and cnpj_cpf:
                st.success(f"Diagnóstico de '{nome_st}' enviado com sucesso ao ecossistema!")
                st.balloons()
            else:
                st.error("Por favor, preencha os campos obrigatórios (*)")

# --- ABAS SIMPLIFICADAS (EXEMPLO) ---
with tabs[1]: st.info("Filtre e busque eventos na aba superior.")
with tabs[2]: st.info("Busque editais e vagas na aba superior.")

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • 2026</p>", unsafe_allow_html=True)