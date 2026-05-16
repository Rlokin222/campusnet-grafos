import streamlit as st
from src.network_service import process_campus_network
from src.visualization.graph_plotter import plot_campus_graph

# Configuração da página - Tema Enterprise
st.set_page_config(
    page_title="CampusNet Solutions",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Corporativo (Sem emojis, fontes sóbrias, layout limpo)
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

        .header-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.2rem;
            letter-spacing: -0.5px;
        }
        .header-subtitle {
            color: #a0aec0;
            font-size: 1rem;
            margin-bottom: 1.5rem;
            font-weight: 400;
        }

        .metric-card {
            background-color: #1e222d;
            border: 1px solid #2b313f;
            border-radius: 4px;
            padding: 1.2rem;
            text-align: left;
            border-left: 4px solid #2962ff;
        }
        .metric-label { color: #8a8d93; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-weight: 500;}
        .metric-value { color: #ffffff; font-size: 1.5rem; font-weight: 700; }
        .metric-value-sm { color: #ffffff; font-size: 1.1rem; font-weight: 500; }

        .badge-ok  { background: rgba(0, 200, 83, 0.1); color: #00c853; padding: 4px 12px; border-radius: 2px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(0, 200, 83, 0.2); }
        .badge-err { background: rgba(213, 0, 0, 0.1); color: #d50000; padding: 4px 12px; border-radius: 2px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(213, 0, 0, 0.2); }

        .analysis-card {
            background-color: #1e222d;
            border: 1px solid #2b313f;
            border-radius: 4px;
            padding: 1rem;
            height: 100%;
        }
        .analysis-label { color: #8a8d93; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem;}
        .analysis-value { color: #ffffff; font-size: 1rem; font-weight: 500; margin-bottom: 0.2rem;}
        .analysis-subtext { color: #2962ff; font-size: 0.9rem; font-weight: 600; }

        .section-title {
            font-size: 1.1rem;
            font-weight: 500;
            color: #ffffff;
            margin-bottom: 1rem;
            margin-top: 1.5rem;
            border-bottom: 1px solid #2b313f;
            padding-bottom: 0.5rem;
        }
        
        /* Ajustes das abas do Streamlit */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            border-bottom: 1px solid #2b313f;
        }
        .stTabs [data-baseweb="tab"] {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### CampusNet Solutions")
    st.caption("Módulo de Engenharia de Redes")
    
    st.write("")
    uploaded_file = st.file_uploader(
        "Importar Topologia (JSON)",
        type=["json"],
        help="Arquivo contendo definições de vértices (com coordenadas) e arestas.",
    )

    st.write("")
    st.markdown("**Controles de Visualização**")
    bg_map_type = st.radio(
        "Camada Base do Mapa",
        options=["Nenhum", "Blueprint", "Satélite"],
        index=1,
        help="Altera o estilo do mapa de fundo. Requer dataset com coordenadas físicas."
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="header-title">Planejamento de Infraestrutura (AGM)</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Análise de custos e rotas ótimas utilizando o Algoritmo de Kruskal</div>', unsafe_allow_html=True)

if uploaded_file is None:
    st.info("Aguardando importação do dataset. Por favor, carregue um arquivo JSON no painel lateral.")
    
    with st.expander("Especificação Técnica do JSON"):
        st.code("""{
  "vertices": {
    "Prédio A": {"x": 300, "y": 450},
    "Prédio B": {"x": 500, "y": 600}
  },
  "arestas": [
    {
      "origem": "Prédio A",
      "destino": "Prédio B",
      "distancia": 120.0,
      "fator_terreno": 1.0,
      "obstaculos": 0,
      "andares": 1
    }
  ]
}""", language="json")
    st.stop()

# ---------------------------------------------------------------------------
# Processamento
# ---------------------------------------------------------------------------
with st.spinner("Processando topologia de rede..."):
    try:
        raw_bytes: bytes = uploaded_file.read()
        result = process_campus_network(raw_bytes)
    except Exception as exc:
        st.error(f"Falha na validação do arquivo: {exc}")
        st.stop()

graph = result.graph

# ---------------------------------------------------------------------------
# Layout Principal (Abas)
# ---------------------------------------------------------------------------
tab_dashboard, tab_metodologia = st.tabs(["Painel de Análise", "Metodologia de Captação de Dados"])

with tab_dashboard:
    # -----------------------------------------------------------------------
    # KPIs Gerais
    # -----------------------------------------------------------------------
    col_status, col_v, col_e, col_cost = st.columns(4)

    with col_status:
        badge = '<span class="badge-ok">Conectividade Validada</span>' if result.is_connected else '<span class="badge-err">Falha de Conexão</span>'
        st.markdown(f'<div class="metric-card"><div class="metric-label">Status da Rede</div><div class="metric-value-sm" style="margin-top: 5px;">{badge}</div></div>', unsafe_allow_html=True)

    with col_v:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Pontos de Acesso (Nós)</div><div class="metric-value">{graph.num_vertices}</div></div>', unsafe_allow_html=True)

    with col_e:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Conexões Possíveis</div><div class="metric-value">{graph.num_edges}</div></div>', unsafe_allow_html=True)
        
    with col_cost:
        st.markdown(f'<div class="metric-card" style="border-left-color: #00c853;"><div class="metric-label">Custo Estimado (AGM)</div><div class="metric-value">R$ {result.total_cost:,.2f}</div></div>', unsafe_allow_html=True)

    if not result.is_connected:
        st.error(f"Topologia inválida: Foram detectados nós isolados sem rota de conexão ({', '.join(result.isolated_nodes)}).")
        st.stop()

    st.write("")

    # -----------------------------------------------------------------------
    # Mapa Visual
    # -----------------------------------------------------------------------
    st.markdown('<div class="section-title">Visualização Espacial da Árvore Geradora Mínima</div>', unsafe_allow_html=True)
    fig = plot_campus_graph(graph, result.mst_edges, bg_map_type=bg_map_type)
    st.pyplot(fig, use_container_width=True)

    # -----------------------------------------------------------------------
    # Análise Financeira
    # -----------------------------------------------------------------------
    st.markdown('<div class="section-title">Análise Financeira e Estatísticas</div>', unsafe_allow_html=True)
    
    aresta_min = min(result.mst_edges, key=lambda e: e.peso)
    aresta_max = max(result.mst_edges, key=lambda e: e.peso)
    custo_todas = sum(e.peso for e in graph.edges)
    economia = custo_todas - result.total_cost

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown(f'<div class="analysis-card"><div class="analysis-label">Rota de Menor Custo</div><div class="analysis-value">{aresta_min.origem} → {aresta_min.destino}</div><div class="analysis-subtext">R$ {aresta_min.peso:,.2f}</div></div>', unsafe_allow_html=True)
    with a2:
        st.markdown(f'<div class="analysis-card"><div class="analysis-label">Rota de Maior Custo</div><div class="analysis-value">{aresta_max.origem} → {aresta_max.destino}</div><div class="analysis-subtext" style="color:#d50000;">R$ {aresta_max.peso:,.2f}</div></div>', unsafe_allow_html=True)
    with a3:
        st.markdown(f'<div class="analysis-card"><div class="analysis-label">Total de Cabos (AGM)</div><div class="analysis-value">{len(result.mst_edges)} Trechos</div><div class="analysis-subtext" style="color:#8a8d93;">Média: R$ {result.total_cost / len(result.mst_edges):,.2f} / trecho</div></div>', unsafe_allow_html=True)
    with a4:
        st.markdown(f'<div class="analysis-card"><div class="analysis-label">Eficiência de Custo</div><div class="analysis-value">Redução de {graph.num_edges - len(result.mst_edges)} conexões</div><div class="analysis-subtext" style="color:#00c853;">Economia: R$ {economia:,.2f}</div></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Tabela Analítica
    # -----------------------------------------------------------------------
    st.markdown('<div class="section-title">Relatório de Roteamento</div>', unsafe_allow_html=True)
    
    custo_acumulado = 0.0
    table_data = []
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
    
    st.caption(f"Processamento concluído em {result.total_time_ms:.2f}ms (Motor: Kruskal O(E log E)).")

with tab_metodologia:
    st.markdown("### Processo de Engenharia de Dados", unsafe_allow_html=True)
    st.write("A modelagem do grafo e o levantamento de custos não ocorrem de forma abstrata. No cenário real de implantação da CampusNet, os dados são alimentados no formato JSON através das seguintes etapas técnicas:")
    
    st.markdown("#### 1. Análise de Planta Baixa (AutoCAD/Revit)")
    st.write("Utilizamos plantas arquitetônicas (*blueprints*) reais do campus para extrair as posições absolutas dos prédios. Essas posições são convertidas em coordenadas `(x, y)` no nosso JSON, permitindo que a visualização da rede seja renderizada fisicamente sobre o mapa da instituição.")
    
    st.markdown("#### 2. Vistoria Técnica em Campo (Site Survey)")
    st.write("A distância em linha reta não define o custo real. Técnicos de campo realizam vistorias preenchendo os seguintes dados para cada possível conexão:")
    st.markdown("- **Fator de Terreno:** Solo macio (1.0), asfalto (1.5) ou rocha (2.0) afetam o custo de escavação.")
    st.markdown("- **Obstáculos Físicos:** Contagem de paredes de concreto, tubulações de gás ou elementos que requerem desvio/perfuração especializada.")
    st.markdown("- **Diferença de Andares:** Instalações verticais (shafts) exigem equipamentos de segurança e elevadores de carga.")
    
    st.markdown("#### 3. Precificação e Conversão Algorítmica")
    st.write("Os dados do levantamento são integrados ao sistema. A fórmula interna do CampusNet consolida os dados de *survey* com os valores de mercado para cabos de fibra óptica (por metro) e mão de obra, transformando a física do campus em um peso financeiro para cada aresta do grafo. Após isso, o Algoritmo de Kruskal é executado para definir o projeto de implantação mais viável.")

