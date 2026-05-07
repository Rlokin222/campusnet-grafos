# Interface do CampusNet — roda com: streamlit run src/app.py
import streamlit as st

from src.network_service import process_campus_network
from src.visualization.graph_plotter import plot_campus_graph

# Configuração da página
st.set_page_config(
    page_title="CampusNet – AGM",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado — cores, fontes e cards
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* Título principal com degradê */
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.1rem;
            line-height: 1.2;
        }
        .hero-sub {
            color: #718096;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
            font-weight: 300;
        }

        /* Cards de métricas */
        .metric-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid #2d3748;
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            text-align: center;
            transition: border-color 0.2s;
        }
        .metric-card:hover { border-color: #4a5568; }
        .metric-icon  { font-size: 1.8rem; margin-bottom: 0.3rem; }
        .metric-label { color: #718096; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
        .metric-value { color: #f7fafc; font-size: 1.7rem; font-weight: 700; }
        .metric-value-sm { color: #f7fafc; font-size: 1.2rem; font-weight: 600; }

        /* Badges de status */
        .badge-ok  { background: #1a4731; color: #68d391; padding: 3px 14px; border-radius: 20px; font-size: .82rem; font-weight: 600; border: 1px solid #276749; }
        .badge-err { background: #742a2a; color: #fc8181; padding: 3px 14px; border-radius: 20px; font-size: .82rem; font-weight: 600; border: 1px solid #9b2c2c; }

        /* Card de análise */
        .analysis-card {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a1a2e 100%);
            border: 1px solid #2d3748;
            border-left: 4px solid #00d4ff;
            border-radius: 12px;
            padding: 1rem 1.4rem;
            margin-bottom: 0.7rem;
        }
        .analysis-label { color: #718096; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.07em; }
        .analysis-value { color: #f7fafc; font-size: 1.1rem; font-weight: 600; margin-top: 0.1rem; }

        /* Seção de título */
        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .divider-line {
            border: none;
            border-top: 1px solid #2d3748;
            margin: 1.5rem 0;
        }

        /* Passos na sidebar */
        .step-item {
            display: flex;
            align-items: flex-start;
            gap: 0.7rem;
            margin-bottom: 0.8rem;
        }
        .step-num {
            background: linear-gradient(135deg, #00d4ff, #7b2ff7);
            color: white;
            font-weight: 700;
            font-size: 0.75rem;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }
        .step-text { color: #a0aec0; font-size: 0.85rem; line-height: 1.4; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/network.png", width=64)
    st.markdown("## 🌐 CampusNet")
    st.caption("Planejamento de cabeamento via Árvore Geradora Mínima.")
    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Carregar topologia (JSON)",
        type=["json"],
        help="O arquivo deve ter as chaves **vertices** e **arestas**.",
    )

    st.divider()

    # Como funciona — 3 passos simples
    st.markdown("**📖 Como funciona**")
    st.markdown(
        """
        <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-text">Faça o upload do arquivo JSON com os prédios e conexões do campus.</div>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-text">O sistema verifica se o grafo é conexo usando BFS.</div>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-text">O Kruskal encontra a rede de cabos de menor custo total (AGM).</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        """
        **Fórmula de custo:**
        ```
        Custo = (distância × terreno)
              + (obstáculos × 50)
              + (andares × 100)
        ```
        """
    )
    st.caption("Algoritmo: **Kruskal** com Union-Find (path compression + union by rank) · **O(E log E)**")

# ---------------------------------------------------------------------------
# Hero / Cabeçalho principal
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-title">🌐 CampusNet</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Planejamento de cabeamento universitário via Árvore Geradora Mínima (Kruskal + Union-Find)</p>',
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info(
        "👈 Carregue um arquivo JSON de topologia na barra lateral para começar.",
        icon="📋",
    )

    # Mini explicação quando não há arquivo carregado
    with st.expander("💡 Formato esperado do arquivo JSON"):
        st.code(
            """{
  "vertices": ["Bloco_A", "Biblioteca", "Laboratorio"],
  "arestas": [
    {
      "origem": "Bloco_A",
      "destino": "Biblioteca",
      "distancia": 120.0,
      "fator_terreno": 1.0,
      "obstaculos": 0,
      "andares": 1
    }
  ]
}""",
            language="json",
        )
    st.stop()

# ---------------------------------------------------------------------------
# Processamento
# ---------------------------------------------------------------------------
with st.spinner("⚙️ Processando o grafo..."):
    try:
        raw_bytes: bytes = uploaded_file.read()
        result = process_campus_network(raw_bytes)
    except (ValueError, KeyError) as exc:
        st.error(f"❌ Erro ao processar o arquivo: {exc}")
        st.stop()

graph = result.graph

# ---------------------------------------------------------------------------
# Cards — visão geral do grafo carregado
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

col_status, col_v, col_e = st.columns(3)

with col_status:
    badge = (
        '<span class="badge-ok">✔ Conexo</span>'
        if result.is_connected
        else '<span class="badge-err">✘ Desconexo</span>'
    )
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">🔗</div>'
        f'<div class="metric-label">Conectividade</div>'
        f'<div class="metric-value-sm">{badge}</div></div>',
        unsafe_allow_html=True,
    )

with col_v:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">🏢</div>'
        f'<div class="metric-label">Prédios (Vértices)</div>'
        f'<div class="metric-value">{graph.num_vertices}</div></div>',
        unsafe_allow_html=True,
    )

with col_e:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">🔌</div>'
        f'<div class="metric-label">Conexões (Arestas)</div>'
        f'<div class="metric-value">{graph.num_edges}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Grafo desconexo — exibe o erro e para
# ---------------------------------------------------------------------------
if not result.is_connected:
    st.error(
        f"🚫 **Grafo desconexo!** Não é possível calcular a AGM.\n\n"
        f"Prédios sem conexão com o restante da rede: "
        f"**{', '.join(result.isolated_nodes)}**\n\n"
        f"Adicione arestas que conectem esses nós e recarregue o arquivo."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Cards — resultado da AGM
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider-line">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Resultado da AGM</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">💰</div>'
        f'<div class="metric-label">Custo Total</div>'
        f'<div class="metric-value">R$ {result.total_cost:,.0f}</div></div>',
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">🔗</div>'
        f'<div class="metric-label">Cabos na AGM</div>'
        f'<div class="metric-value">{len(result.mst_edges)}</div></div>',
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">⚡</div>'
        f'<div class="metric-label">Tempo de Execução</div>'
        f'<div class="metric-value-sm">{result.total_time_ms:.3f} ms</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Análise da AGM
# ---------------------------------------------------------------------------
if result.mst_edges:
    st.markdown('<div class="section-title">🔍 Análise da AGM</div>', unsafe_allow_html=True)

    aresta_min = min(result.mst_edges, key=lambda e: e.peso)
    aresta_max = max(result.mst_edges, key=lambda e: e.peso)
    custo_todas = sum(e.peso for e in graph.edges)
    economia = custo_todas - result.total_cost
    custo_medio = result.total_cost / len(result.mst_edges)

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.markdown(
            f'<div class="analysis-card">'
            f'<div class="analysis-label">🟢 Cabo mais barato</div>'
            f'<div class="analysis-value">{aresta_min.origem} → {aresta_min.destino}</div>'
            f'<div style="color:#68d391;font-size:.9rem;margin-top:2px">R$ {aresta_min.peso:,.0f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with a2:
        st.markdown(
            f'<div class="analysis-card">'
            f'<div class="analysis-label">🔴 Cabo mais caro</div>'
            f'<div class="analysis-value">{aresta_max.origem} → {aresta_max.destino}</div>'
            f'<div style="color:#fc8181;font-size:.9rem;margin-top:2px">R$ {aresta_max.peso:,.0f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with a3:
        st.markdown(
            f'<div class="analysis-card">'
            f'<div class="analysis-label">💡 Custo médio por cabo</div>'
            f'<div class="analysis-value">R$ {custo_medio:,.0f}</div>'
            f'<div style="color:#718096;font-size:.85rem;margin-top:2px">por conexão</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with a4:
        st.markdown(
            f'<div class="analysis-card">'
            f'<div class="analysis-label">✂️ Economia vs. cabeamento completo</div>'
            f'<div class="analysis-value" style="color:#68d391">R$ {economia:,.0f}</div>'
            f'<div style="color:#718096;font-size:.85rem;margin-top:2px">usando {graph.num_edges - len(result.mst_edges)} conexões a menos</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.write("")

# ---------------------------------------------------------------------------
# Visualização do grafo
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider-line">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🗺️ Visualização do Grafo e da AGM</div>', unsafe_allow_html=True)
st.caption(
    "Arestas **azul ciano** = selecionadas pela AGM &nbsp;|&nbsp; "
    "Arestas **cinza tracejado** = descartadas pelo Kruskal"
)

fig = plot_campus_graph(graph, result.mst_edges)
st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Tabela de cabos selecionados
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider-line">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔌 Cabos selecionados pela AGM</div>', unsafe_allow_html=True)

custo_acumulado = 0.0
table_data = []
for i, e in enumerate(result.mst_edges):
    custo_acumulado += e.peso
    table_data.append(
        {
            "Nº": i + 1,
            "Origem": e.origem,
            "Destino": e.destino,
            "Custo (R$)": f"R$ {e.peso:,.2f}",
            "Custo Acumulado": f"R$ {custo_acumulado:,.2f}",
        }
    )

st.dataframe(table_data, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Detalhes de desempenho (expansível)
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

with st.expander("⚙️ Detalhes de desempenho"):
    perf_cols = st.columns(2)
    with perf_cols[0]:
        st.metric("Leitura + construção do grafo", f"{result.build_time_ms:.3f} ms")
    with perf_cols[1]:
        st.metric("Execução do Kruskal", f"{result.kruskal_time_ms:.3f} ms")
    st.caption(
        f"Complexidade: O(E log E) = O({graph.num_edges} × log {graph.num_edges}) "
        f"para a ordenação das {graph.num_edges} arestas."
    )

st.write("")
st.caption("CampusNet · Teoria dos Grafos · Python 3.10+ · Streamlit")
