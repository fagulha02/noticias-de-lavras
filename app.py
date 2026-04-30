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

# 2. CSS DE ALTO CONTRASTE & UI
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}
    
    /* Estilo dos Cards */
    .card {{ 
        background: linear-gradient(145deg, #1E2129, #161B22); 
        padding: 22px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; 
        transition: 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}
    .badge {{ font-size: 0.7rem; padding: 3px 10px; border-radius: 5px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }}
    
    /* Botões Arredondados */
    div.stButton > button {{
        background-color: transparent; color: white; border: 2px solid {COR_VERDE} !important;
        border-radius: 50px; padding: 10px 40px; font-weight: 700; width: 100%; transition: 0.4s;
    }}
    div.stButton > button:hover {{ background-color: {COR_VERDE} !important; color: #0E1117 !important; box-shadow: 0 0 20px {COR_VERDE}; }}
    
    /* Expander/Texto Retrátil */
    .stExpander {{ background-color: {COR_FUNDO_MENU}; border: 1px solid #333 !important; border-radius: 10px !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA
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
    query += f" after:{d_ini.strftime('%Y-%m-%d')} before:{d_f.strftime('%Y-%m-%d') if 'd_f' in locals() else date.today().strftime('%Y-%m-%d')}"
    
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
    return reg, extra, ini, fim, c_btn

# --- ABAS DE BUSCA (Notícias, Eventos, etc) ---
# [As abas seguem o padrão do seu código funcional original]
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    reg, extra, d_i, d_f, c_btn = render_filtros("not", 7)
    if c_btn.button("BUSCAR", key="btn_not"):
        st.session_state.db['n'] = fetch_radar_data("inovação OR tecnologia OR economia", extra, reg, d_i, d_f)
    if 'n' in st.session_state.db:
        for item in st.session_state.db['n'][:10]:
            st.markdown(f'<div class="card" style="border-left: 5px solid {COR_AZUL};"><span class="badge" style="background:{COR_AZUL}33; color:{COR_AZUL};">Notícia</span><h3>{item.title}</h3><a href="{item.link}" target="_blank">Ler mais →</a></div>', unsafe_allow_html=True)

# --- ABA DIAGNÓSTICO (REESTRUTURADA COM TEXTO RETRÁTIL) ---
with tabs[5]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Diagnóstico e Monitoramento de Startups do Ecossistema Vale dos Ipês")
    
    # TEXTO RETRÁTIL DO CENSO (Baseado na sua imagem)
    st.markdown("## Diagnóstico e Monitoramento de Startups do Ecossistema de Inovação Vale dos Ipês")

# Texto Institucional Completo e Retrátil
with st.expander("📄 LEIA O MANIFESTO DO CENSO SEMESTRAL - VALE DOS IPÊS", expanded=False):
    st.markdown(f"""
    <div style="color: {COR_TEXTO}; line-height: 1.8; text-align: justify; font-size: 0.95rem; background-color: #1A1E24; padding: 25px; border-radius: 10px; border: 1px solid #333;">
        <strong>Prezado(a) Empreendedor(a),</strong><br><br>
        É com satisfação que convidamos a sua startup a integrar o <strong>Censo Semestral Vale dos Ipês</strong>, uma iniciativa estratégica da Superintendência de Inovação e parceria com os ambientes de inovação do ecossistema, para consolidar Lavras como a <strong>Capital do Futuro do Alimento</strong>.<br><br>
        Este diagnóstico é o instrumento fundamental para que possamos compreender a maturidade do nosso ecossistema e, a partir de dados reais, formular políticas públicas e ações de fomento que atendam com precisão às necessidades de quem empreende no nosso território.<br><br>
        A sua participação, atualizada a cada seis meses, permite que o <strong>LVRS+ (Pacto pela Inovação de Lavras)</strong> atue de forma personalizada, oferecendo suporte direto através dos nossos ambientes de inovação, os 12 Projetos Prioritários, programas de incentivo fiscal e conexões com investidores.<br><br>
        Mais do que um levantamento estatístico, este censo visa monitorar o peso da tecnologia, do agrofoodtech e outros setores importantes no PIB de Lavras, garantindo que o seu negócio ganhe a projeção nacional e internacional que merece.<br><br>
        Pela densidade das informações solicitadas, que abrangem desde a governança e faturamento até o impacto social e tecnológico, o preenchimento pode levar entre <strong>50 a 60 minutos</strong>, mas o impacto gerado para o fortalecimento do seu negócio e da nossa cidade será duradouro. Contamos com você para construirmos juntos a Lavras do amanhã.<br><br>
        <strong>Vale dos Ipês - Onde a inovação encontra o futuro.</strong>
    </div>
    """, unsafe_allow_html=True)
    # FORMULÁRIO COMPLETO
    with st.form("censo_completo"):
        st.markdown("### 1. Identificação da Startup")
        c1, c2 = st.columns(2)
        with c1:
            nome_st = st.text_input("Nome da Startup/Projeto *")
            cnpj = st.text_input("CNPJ ou CPF (Fundador) *")
        with c2:
            setor = st.selectbox("Vertical de Atuação", ["AgTech", "FoodTech", "HealthTech", "FinTech", "EdTech", "Outros"])
            fase = st.selectbox("Fase Atual", ["Ideação", "Validação", "Operação (MVP)", "Tração", "Escala"])
        
        st.text_area("Resumo da Solução (O que vocês resolvem?)")
        
        st.markdown("---")
        st.markdown("### 2. Sócios e Maturidade")
        c3, c4 = st.columns(2)
        with c3:
            num_socios = st.number_input("Nº de Sócios Fundadores", min_value=1, step=1)
            investimento = st.radio("Já captou investimento externo?", ["Não", "Sim (Anjo/VC)", "Sim (Fomento Público)"])
        with c4:
            faturamento = st.selectbox("Faturamento Anual", ["Não fatura", "Até R$ 100k", "R$ 100k - R$ 500k", "Acima de R$ 1M"])
            vagas = st.text_input("Vagas diretas hoje em Lavras")

        st.markdown("---")
        st.markdown("### 3. Conexão LVRS+")
        st.multiselect("Com quais projetos você deseja interagir?", 
                       ["Cluster AgroFoodTech", "IpêTech", "Cinturão do Alimento", "Escola do Futuro"])
        
        st.text_area("Qual o maior desafio para os próximos 6 meses?")

        if st.form_submit_button("REGISTRAR DIAGNÓSTICO"):
            if nome_st and cnpj:
                st.success(f"Diagnóstico de '{nome_st}' registrado com sucesso!")
                st.balloons()
            else:
                st.error("Preencha os campos obrigatórios (*)")

st.markdown("<br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • 2026</p>", unsafe_allow_html=True)