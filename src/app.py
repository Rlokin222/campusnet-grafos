import json
import pandas as pd
import streamlit as st
import folium
from folium.plugins import Geocoder
from geopy.distance import geodesic

try:
    from streamlit_folium import st_folium
except ImportError:
    st_folium = None

from src.network_service import process_campus_network
from src.visualization.graph_plotter import plot_campus_graph

# Configuração da página - Tema Enterprise
st.set_page_config(
    page_title="CampusNet Solutions",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicialização de Estado para o Construtor
if "builder_nodes" not in st.session_state:
    st.session_state.builder_nodes = {}
if "builder_edges" not in st.session_state:
    st.session_state.builder_edges = pd.DataFrame(columns=[
        "Origem", "Destino", "Distancia_m", "Fator_Terreno", "Obstaculos", "Andares"
    ])
if "generated_json" not in st.session_state:
    st.session_state.generated_json = None

# CSS Corporativo
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
        .header-title { font-size: 2.2rem; font-weight: 700; color: #ffffff; margin-bottom: 0.2rem; }
        .header-subtitle { color: #a0aec0; font-size: 1rem; margin-bottom: 1.5rem; }
        .metric-card { background-color: #1e222d; border: 1px solid #2b313f; padding: 1.2rem; border-left: 4px solid #2962ff; }
        .metric-label { color: #8a8d93; font-size: 0.75rem; text-transform: uppercase; font-weight: 500;}
        .metric-value { color: #ffffff; font-size: 1.5rem; font-weight: 700; }
        .badge-ok  { background: rgba(0, 200, 83, 0.1); color: #00c853; padding: 4px 12px; border-radius: 2px; font-size: 0.8rem; }
        .badge-err { background: rgba(213, 0, 0, 0.1); color: #d50000; padding: 4px 12px; border-radius: 2px; font-size: 0.8rem; }
        .section-title { font-size: 1.1rem; font-weight: 500; color: #ffffff; margin-bottom: 1rem; margin-top: 1.5rem; border-bottom: 1px solid #2b313f; padding-bottom: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### CampusNet Solutions")
    modo = st.radio("Módulo de Operação", ["Painel Analítico", "Construtor Interativo"])
    st.write("---")
    
    st.markdown("### 💰 Tabela de Custos Reais")
    st.caption("Edite os valores para simular os custos de mercado:")
    custo_cabo = st.number_input("Cabo por Metro (R$/m)", min_value=0.1, value=2.50, step=0.50)
    custo_obs = st.number_input("Taxa por Obstáculo (R$)", min_value=0.0, value=50.0, step=10.0)
    custo_andar = st.number_input("Taxa por Andar (R$)", min_value=0.0, value=100.0, step=10.0)
    st.write("---")

# ===========================================================================
# MODO 1: PAINEL ANALÍTICO
# ===========================================================================
if modo == "Painel Analítico":
    st.markdown('<div class="header-title">Planejamento de Infraestrutura (AGM)</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Análise de custos e rotas ótimas utilizando o Algoritmo de Kruskal</div>', unsafe_allow_html=True)

    with st.sidebar:
        uploaded_file = st.file_uploader(
            "Importar Topologia (JSON)",
            type=["json"],
            help="Arquivo contendo definições de vértices e arestas.",
        )
        st.markdown("**Controles de Visualização**")
        bg_map_type = st.radio(
            "Camada Base do Mapa",
            options=["Nenhum", "Blueprint", "Satélite"],
            index=0
        )
        
        if st.session_state.generated_json:
            st.success("JSON gerado pelo Construtor disponível na memória!")

    raw_bytes = None
    if uploaded_file is not None:
        raw_bytes = uploaded_file.read()
    elif st.session_state.generated_json is not None:
        raw_bytes = st.session_state.generated_json.encode('utf-8')

    if raw_bytes is None:
        st.info("Aguardando importação do dataset. Carregue um arquivo JSON ou crie um no Construtor Interativo.")
        st.stop()

    with st.spinner("Processando topologia de rede..."):
        try:
            result = process_campus_network(
                raw_bytes=raw_bytes,
                custo_cabo_m=custo_cabo,
                custo_obstaculo=custo_obs,
                custo_andar=custo_andar
            )
        except Exception as exc:
            st.error(f"Falha na validação do arquivo: {exc}")
            st.stop()

    graph = result.graph
    tab_dashboard, tab_metodologia = st.tabs(["Painel de Análise", "Metodologia de Captação e Custos"])

    with tab_dashboard:
        col_status, col_v, col_e, col_cost = st.columns(4)
        with col_status:
            badge = '<span class="badge-ok">Conectividade Validada</span>' if result.is_connected else '<span class="badge-err">Falha de Conexão</span>'
            st.markdown(f'<div class="metric-card"><div class="metric-label">Status da Rede</div><div style="margin-top: 5px;">{badge}</div></div>', unsafe_allow_html=True)
        with col_v:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Pontos de Acesso (Nós)</div><div class="metric-value">{graph.num_vertices}</div></div>', unsafe_allow_html=True)
        with col_e:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Conexões Possíveis</div><div class="metric-value">{graph.num_edges}</div></div>', unsafe_allow_html=True)
        with col_cost:
            st.markdown(f'<div class="metric-card" style="border-left-color: #00c853;"><div class="metric-label">Custo Estimado (AGM)</div><div class="metric-value">R$ {result.total_cost:,.2f}</div></div>', unsafe_allow_html=True)

        if not result.is_connected:
            st.error(f"Topologia inválida: Nós isolados encontrados ({', '.join(result.isolated_nodes)}).")
            st.stop()

        st.markdown('<div class="section-title">Visualização do Grafo</div>', unsafe_allow_html=True)
        fig = plot_campus_graph(graph, result.mst_edges, bg_map_type=bg_map_type)
        st.pyplot(fig, use_container_width=True)

        st.markdown('<div class="section-title">Relatório de Roteamento</div>', unsafe_allow_html=True)
        table_data = []
        custo_acumulado = 0.0
        for i, e in enumerate(result.mst_edges):
            custo_acumulado += e.peso
            table_data.append({
                "Ordem": f"{i + 1:02d}",
                "Ponto de Origem": e.origem,
                "Ponto de Destino": e.destino,
                "Custo Unitário": f"R$ {e.peso:,.2f}",
                "Custo Acumulado": f"R$ {custo_acumulado:,.2f}",
            })
        st.dataframe(table_data, use_container_width=True, hide_index=True)

    with tab_metodologia:
        st.markdown("### Processo de Engenharia de Dados", unsafe_allow_html=True)
        st.write("A modelagem do grafo e o levantamento de custos não ocorrem de forma abstrata. No cenário real de implantação da CampusNet, os dados são alimentados no formato JSON através das seguintes etapas técnicas:")
        
        st.markdown("#### 1. Mapeamento Geoespacial (GPS)")
        st.write("Utilizamos mapas reais via satélite (Folium/OpenStreetMap) para extrair as posições absolutas dos prédios na Terra. No **Construtor Interativo**, o usuário gera essas coordenadas `(Latitude, Longitude)` clicando no mapa, mapeando a posição global de cada edifício.")
        
        st.markdown("#### 2. Cálculo de Custo Monetário Final (Arestas)")
        st.write("O custo financeiro (R$) de cada conexão do grafo **depende diretamente dos parâmetros físicos**. O valor que você vê na Árvore Geradora Mínima não é inventado; ele segue nossa equação de engenharia de redes:")
        st.info("**Custo Monetário = (Distância Geodésica × Fator de Terreno) + (Obstáculos × 50) + (Diferença de Andares × 100)**")
        st.write("De onde vêm esses parâmetros?")
        st.markdown("- **Distância Física:** Calculada usando a fórmula geodésica baseada no formato elipsoide da Terra (em metros reais) e multiplicada pelo preço do cabo por metro.")
        st.markdown("- **Fator de Terreno:** Solo macio (1.0), asfalto (1.5) ou rocha (2.0) afetam o custo de perfuração.")
        st.markdown("- **Obstáculos:** Exigem taxas, laudos ou quebras complexas. Custo base adicionado: R$ 50,00 por barreira.")
        st.markdown("- **Andares:** Custo adicionado de R$ 100,00 por andar de desnível.")
        
        st.markdown("#### 3. Motor Algorítmico (Kruskal)")
        st.write("Após compilar esses parâmetros em um valor único em Reais (R$), o sistema roda o **Algoritmo de Kruskal**, descartando redundâncias para entregar o projeto mais enxuto e seguro para a universidade.")

# ===========================================================================
# MODO 2: CONSTRUTOR DE TOPOLOGIA (Folium Map)
# ===========================================================================
elif modo == "Construtor Interativo":
    st.markdown('<div class="header-title">Construtor de Topologia Geoespacial</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Navegue no mapa mundial, clique para adicionar prédios (GPS) e calcule a infraestrutura.</div>', unsafe_allow_html=True)

    if st_folium is None:
        st.error("Biblioteca `streamlit-folium` ausente. Execute: `pip install -r requirements.txt`")
        st.stop()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**1. Clique no mapa para capturar a Latitude e Longitude:**")
        # Centro inicial do mapa
        m = folium.Map(location=[-23.5505, -46.6333], zoom_start=14, tiles=None)
        
        # Adiciona as opções de Camadas (Ruas e Satélite)
        folium.TileLayer('OpenStreetMap', name='Ruas (Padrão)').add_to(m)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satélite (Esri)',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Adiciona o controle para o usuário alternar entre Satélite e Ruas
        folium.LayerControl().add_to(m)
        
        # Adiciona a barra de pesquisa (Lupa) sem forçar posição para evitar bugs no Streamlit
        Geocoder().add_to(m)
        
        # Adiciona marcadores para pontos já cadastrados
        for name, coords in st.session_state.builder_nodes.items():
            folium.Marker(
                [coords["lat"], coords["lon"]],
                popup=name,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
        # Captura os dados do mapa
        map_data = st_folium(m, width=700, height=500, key="interactive_map")
        
    with col2:
        st.markdown("**Adicionar Ponto**")
        lat, lon = None, None
        
        if map_data and map_data.get("last_clicked"):
            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]
            st.write(f"📍 Coordenada GPS capturada:\n**Lat: {lat:.6f}\nLon: {lon:.6f}**")
            
            node_name = st.text_input("Nome do Prédio/Local:")
            if st.button("Salvar Ponto no Mapa", type="primary"):
                if node_name:
                    st.session_state.builder_nodes[node_name] = {"lat": lat, "lon": lon}
                    st.rerun()
                else:
                    st.warning("Dê um nome ao ponto.")
        else:
            st.info("Clique em qualquer lugar do mapa para obter as coordenadas.")

        st.write("---")
        st.markdown("**Pontos Cadastrados:**")
        if st.session_state.builder_nodes:
            df_nodes = pd.DataFrame([
                {"Nome": k, "Lat": v["lat"], "Lon": v["lon"]} 
                for k, v in st.session_state.builder_nodes.items()
            ])
            # Tabela editável para os nós
            edited_nodes = st.data_editor(df_nodes, hide_index=True, num_rows="dynamic", use_container_width=True)
            
            # Sincronizar edições da tabela com o state
            new_nodes = {}
            for _, row in edited_nodes.iterrows():
                if pd.notna(row["Nome"]):
                    new_nodes[str(row["Nome"])] = {"lat": float(row["Lat"]), "lon": float(row["Lon"])}
            st.session_state.builder_nodes = new_nodes

            if st.button("Limpar Mapa"):
                st.session_state.builder_nodes = {}
                st.session_state.builder_edges = pd.DataFrame(columns=[
                    "Origem", "Destino", "Distancia_m", "Fator_Terreno", "Obstaculos", "Andares"
                ])
                st.rerun()
        else:
            st.caption("Nenhum prédio cadastrado ainda.")

    st.markdown('<div class="section-title">2. Tabela de Conexões e Custos Reais</div>', unsafe_allow_html=True)
    st.write("Defina as conexões entre os prédios. Clique abaixo para cruzar os pontos e calcular as distâncias reais em metros.")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Gerar Combinações e Distâncias GPS"):
            nodes_list = list(st.session_state.builder_nodes.keys())
            edges = []
            # Gera um grafo completo
            for i in range(len(nodes_list)):
                for j in range(i + 1, len(nodes_list)):
                    n1, n2 = nodes_list[i], nodes_list[j]
                    c1 = st.session_state.builder_nodes[n1]
                    c2 = st.session_state.builder_nodes[n2]
                    # Calcula distância geodésica em metros (reais)
                    p1 = (c1["lat"], c1["lon"])
                    p2 = (c2["lat"], c2["lon"])
                    dist_meters = round(geodesic(p1, p2).meters, 1)
                    
                    edges.append({
                        "Origem": n1, "Destino": n2, "Distancia_m": dist_meters,
                        "Fator_Terreno": 1.0, "Obstaculos": 0, "Andares": 0
                    })
            st.session_state.builder_edges = pd.DataFrame(edges)
            st.rerun()
    
    # Tabela editável (A distância gerada é real, mas o usuário pode ajustar se necessário)
    edited_df = st.data_editor(
        st.session_state.builder_edges,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Origem": st.column_config.SelectboxColumn("Origem", options=list(st.session_state.builder_nodes.keys()), required=True),
            "Destino": st.column_config.SelectboxColumn("Destino", options=list(st.session_state.builder_nodes.keys()), required=True),
            "Distancia_m": st.column_config.NumberColumn("Distância GPS (m)", min_value=0.1, format="%.1f"),
            "Fator_Terreno": st.column_config.NumberColumn("Fator Terreno", min_value=1.0, format="%.2f"),
            "Obstaculos": st.column_config.NumberColumn("Obstáculos (un)", min_value=0, step=1),
            "Andares": st.column_config.NumberColumn("Desnível (Andares)", min_value=0, step=1),
        }
    )
    
    st.session_state.builder_edges = edited_df

    st.write("---")
    if st.button("🏗️ Exportar Projeto e Calcular AGM", type="primary"):
        if len(st.session_state.builder_nodes) < 2:
            st.error("Cadastre pelo menos 2 pontos.")
        elif edited_df.empty:
            st.error("Cadastre pelo menos uma conexão.")
        else:
            arestas_json = []
            for _, row in edited_df.iterrows():
                if pd.isna(row["Origem"]) or pd.isna(row["Destino"]): continue
                arestas_json.append({
                    "origem": row["Origem"],
                    "destino": row["Destino"],
                    "distancia": float(row["Distancia_m"]),
                    "fator_terreno": float(row["Fator_Terreno"]),
                    "obstaculos": int(row["Obstaculos"]),
                    "andares": int(row["Andares"])
                })
            
            final_dict = {
                "parametros_custo": {
                    "cabo_m": custo_cabo,
                    "obstaculo": custo_obs,
                    "andar": custo_andar
                },
                "vertices": st.session_state.builder_nodes,
                "arestas": arestas_json
            }
            st.session_state.generated_json = json.dumps(final_dict, indent=2)
            st.success("JSON gerado com sucesso! Mude para o 'Painel Analítico' na barra lateral para ver o grafo final.")
