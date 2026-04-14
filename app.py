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

# 2. CSS CUSTOMIZADO (Design Elegante e Centralizado)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    .stApp {{ background-color: #0E1117; }}
    * {{ font-family: 'Montserrat', sans-serif; color: {COR_TEXTO}; }}

    /* Cards Estilizados */
    .card {{
        background: {COR_FUNDO_CARD};
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    .card:hover {{ border-color: {COR_VERDE}; transform: translateY(-3px); }}

    /* Botões com Contorno Forte e Centralização */
    div.stButton > button {{
        background-color: transparent;
        color: white;
        border: 3px solid {COR_VERDE} !important;
        border-radius: 50px;
        padding: 12px 50px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s ease;
        display: block;
        margin: 0 auto;
    }}
    
    div.stButton > button:hover {{
        background-color: {COR_VERDE} !important;
        box-shadow: 0 0 20px {COR_VERDE};
        color: #0E1117 !important;
    }}

    .btn-eventos div.stButton > button {{ border-color: {COR_LARANJA} !important; }}
    .btn-eventos div.stButton > button:hover {{ background-color: {COR_LARANJA} !important; box-shadow: 0 0 20px {COR_LARANJA}; }}

    .header-container {{ text-align: center; padding: 50px 0; background: linear-gradient(180deg, #161B22 0%, #0E1117 100%); border-bottom: 1px solid #333; }}
    .logo-img {{ filter: drop-shadow(0 0 15px rgba(255,255,255,0.3)); margin-bottom: 20px; }}
    
    /* Estilização para o formulário de diagnóstico */
    .stExpander {{ background: {COR_FUNDO_CARD} !important; border: 1px solid #333 !important; border-radius: 15px !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR DE BUSCA COM TRATAMENTO DE URL
def buscar_dados(termo, local=""):
    query = f"{termo} {local}".strip()
    query_encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
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

# 5. ESTRUTURA DE ABAS
tab_noticias, tab_eventos, tab_oportunidades, tab_diagnostico = st.tabs([
    "📰 NOTÍCIAS", "📅 EVENTOS", "💡 OPORTUNIDADES", "🚀 DIAGNÓSTICO STARTUP"
])

# --- ABA NOTÍCIAS ---
with tab_noticias:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        topico_noticia = st.selectbox("Selecione o Tópico", ["Geral", "Economia", "Educação", "Inovação", "Saúde", "Rankings"])
        btn_not = st.button("ATUALIZAR RADAR", key="btn_not")

    if btn_not:
        termos_map = {
            "Geral": "Lavras MG", "Economia": "investimento startup Lavras",
            "Educação": "UFLA pesquisa Lavras", "Inovação": "inovação tecnologia Lavras",
            "Saúde": "saúde hospital Lavras", "Rankings": "ranking melhores cidades Lavras MG"
        }
        with st.spinner("Sincronizando por data..."):
            noticias = buscar_dados(termos_map[topico_noticia])
            noticias_ord = sorted(noticias, key=lambda x: x.published_parsed, reverse=True)
            for n in noticias_ord[:12]:
                data = datetime(*n.published_parsed[:6]).strftime('%d/%m/%Y %H:%M')
                st.markdown(f"""
                    <div class="card" style="border-left: 5px solid {COR_AZUL};">
                        <small style="color:{COR_AZUL}; font-weight:700;">{topico_noticia.upper()}</small>
                        <h3 style="margin:12px 0; font-size:1.3rem;">{n.title}</h3>
                        <p style="color:#888; font-size:0.85rem;">📅 Publicado em: {data}</p>
                        <a href="{n.link}" target="_blank" style="color:{COR_AZUL}; text-decoration:none; font-weight:700;">LER NOTÍCIA →</a>
                    </div>
                """, unsafe_allow_html=True)

# --- ABA EVENTOS ---
with tab_eventos:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid_ev, _ = st.columns([1, 2, 1])
    with col_mid_ev:
        local_ev = st.selectbox("Abrangência Regional", ["Lavras", "Minas Gerais", "Brasil", "Mundial"])
        tema_ev = st.selectbox("Tema do Evento", ["Todos os temas", "Tecnologia", "Empreendedorismo", "Cultura", "Universitário"])
        st.markdown('<div class="btn-eventos">', unsafe_allow_html=True)
        btn_ev = st.button("BUSCAR EVENTOS", key="btn_ev")
        st.markdown('</div>', unsafe_allow_html=True)

    if btn_ev:
        with st.spinner("Mapeando agenda..."):
            termo_final = f"eventos {tema_ev if tema_ev != 'Todos os temas' else ''}"
            eventos = buscar_dados(termo_final, local_ev)
            eventos_ord = sorted(eventos, key=lambda x: x.published_parsed, reverse=True)
            for e in eventos_ord[:12]:
                data_e = datetime(*e.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""
                    <div class="card" style="border-left: 5px solid {COR_LARANJA};">
                        <small style="color:{COR_LARANJA}; font-weight:700;">{tema_ev.upper()}</small>
                        <h3 style="margin:12px 0; font-size:1.3rem;">{e.title}</h3>
                        <p style="color:#888; font-size:0.85rem;">📅 Divulgado em: {data_e}</p>
                        <a href="{e.link}" target="_blank" 
                           style="display:inline-block; margin-top:10px; padding:10px 30px; background:{COR_LARANJA}; color:white; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:700;">
                           VER DETALHES
                        </a>
                    </div>
                """, unsafe_allow_html=True)

# --- NOVA ABA: OPORTUNIDADES ---
with tab_oportunidades:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid_op, _ = st.columns([1, 2, 1])
    with col_mid_op:
        perfil_op = st.selectbox("Quem é você?", [
            "Empresas Consolidadas", "Startups", "Empreendedores", "Estudantes"
        ])
        abrangencia_op = st.radio("Abrangência", ["Local (Lavras/MG)", "Nacional (Brasil)"], horizontal=True)
        btn_op = st.button("MAPEAR OPORTUNIDADES", key="btn_op")

    if btn_op:
        # Lógica de mapeamento baseada no seu alinhamento de ideias
        perfis_map = {
            "Empresas Consolidadas": "inovação aberta open innovation parcerias tecnologias",
            "Startups": "edital fomento rodada investimento startup aporte anjo fapemig",
            "Empreendedores": "oportunidade mercado tendência franquia inovação nicho",
            "Estudantes": "vaga estágio startup trainee inovação bolsa pesquisa ufla"
        }
        loc_op = "Lavras MG" if abrangencia_op == "Local (Lavras/MG)" else "Brasil"
        
        with st.spinner("Buscando oportunidades estratégicas..."):
            ops = buscar_dados(perfis_map[perfil_op], loc_op)
            ops_ord = sorted(ops, key=lambda x: x.published_parsed, reverse=True)
            for o in ops_ord[:12]:
                data_o = datetime(*o.published_parsed[:6]).strftime('%d/%m/%Y')
                st.markdown(f"""
                    <div class="card" style="border-left: 5px solid {COR_VERDE};">
                        <small style="color:{COR_VERDE}; font-weight:700;">OPORTUNIDADE PARA {perfil_op.upper()}</small>
                        <h3 style="margin:12px 0; font-size:1.3rem;">{o.title}</h3>
                        <p style="color:#888; font-size:0.85rem;">📅 Detectado em: {data_o}</p>
                        <a href="{o.link}" target="_blank" 
                           style="display:inline-block; margin-top:10px; padding:10px 30px; background:{COR_VERDE}; color:#0E1117; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:700;">
                           SABER MAIS SOBRE A OPORTUNIDADE
                        </a>
                    </div>
                """, unsafe_allow_html=True)

# --- ABA DIAGNÓSTICO STARTUP ---
with tab_diagnostico:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color:{COR_VERDE}; font-weight:700;'>Censo Semestral de Inovação</h2>
            <p style='color:#888;'>Diagnóstico e Monitoramento de Startups — Vale dos Ipês</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🔒 Consentimento & Privacidade (LGPD)", expanded=True):
        st.write("Em conformidade com a LGPD (Lei nº 13.709/2018), informe seu consentimento:")
        c1 = st.checkbox("Autorizo o tratamento de dados empresariais para planejamento de políticas públicas.")
        c2 = st.checkbox("Autorizo o tratamento de dados pessoais dos sócios para contato institucional.")
        c3 = st.checkbox("Estou ciente do uso de dados anonimizados em relatórios do ecossistema.")

    if c1 and c2 and c3:
        with st.form("form_startup_diagnostico"):
            st.markdown(f"<h4 style='color:{COR_AZUL};'>🏢 Informações Gerais</h4>", unsafe_allow_html=True)
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nome_st = st.text_input("Nome da Startup *")
                cnpj_st = st.text_input("CNPJ ou CPF do representante")
            with col_f2:
                vertical_st = st.selectbox("Vertical de atuação", ["AgriTech", "HealthTech", "GovTech", "EdTech", "FinTech", "Outro"])
                fase_st = st.select_slider("Fase do negócio", options=["Ideação", "Validação", "Operação", "Tração", "Escala"])
            resumo_st = st.text_area("Resumo da Solução (Dor e Proposta de Valor)")
            st.markdown(f"<h4 style='color:{COR_LARANJA};'>👥 Sócios & Fundadores</h4>", unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                socio_n = st.text_input("Sócio Principal *")
                socio_e = st.text_input("E-mail para contato *")
            with col_s2:
                socio_t = st.text_input("Telefone (WhatsApp) *")
                socio_l = st.text_input("LinkedIn (Perfil)")
            st.markdown(f"<h4 style='color:{COR_VERDE};'>📈 Tração & Lavras</h4>", unsafe_allow_html=True)
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                fat_st = st.selectbox("Faturamento Bruto Anual", ["Ainda não faturamos", "Até R$ 50k", "R$ 50k a R$ 250k", "Acima de R$ 250k"])
            with col_t2:
                recursos_st = st.radio("Possui recursos para os próximos 12 meses?", ["Sim", "Sim, com risco", "Não"])
            projetos_lvrs = st.multiselect("Projetos LVRS+ com potencial de interação:", 
                                         ["Cluster AgroFoodTech", "Hub IpêTech", "Blue Zone Lavras", "Festival do Futuro", "Circuito Vale dos Ipês"])
            st.markdown("<br>", unsafe_allow_html=True)
            submit_diag = st.form_submit_button("ENVIAR DIAGNÓSTICO")
            if submit_diag:
                if nome_st and socio_e:
                    st.success("✔ Diagnóstico enviado com sucesso! Sua startup agora está no mapa do Vale dos Ipês.")
                    st.balloons()
                else:
                    st.error("Campos obrigatórios (*) não preenchidos.")
    else:
        st.info("⚠ Aceite os termos de privacidade acima para liberar o formulário.")

st.markdown("<br><br><p style='text-align:center; opacity:0.3; font-size:0.7rem;'>VALE DOS IPÊS • HUB DE INTELIGÊNCIA E OPORTUNIDADES</p>", unsafe_allow_html=True)