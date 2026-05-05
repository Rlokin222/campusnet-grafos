"""
Interface Streamlit do CampusNet — Cálculo da Árvore Geradora Mínima (AGM).
Execute com:  streamlit run src/app.py
"""
import streamlit as st

from src.network_service import process_campus_network
from src.visualization.graph_plotter import plot_campus_graph

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusNet – AGM",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS customizado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .hero-title {
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .hero-sub {
            color: #a0aec0;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid #2d3748;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
        }
        .metric-label { color: #a0aec0; font-size: 0.85rem; margin-bottom: 0.3rem; }
        .metric-value { color: #fff; font-size: 1.6rem; font-weight: 700; }
        .badge-ok  { background:#22543d; color:#9ae6b4; padding:2px 10px; border-radius:20px; font-size:.8rem; }
        .badge-err { background:#742a2a; color:#fed7d7; padding:2px 10px; border-radius:20px; font-size:.8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/network.png",
        width=72,
    )
    st.markdown("## 🌐 CampusNet")
    st.caption("Árvore Geradora Mínima para cabeamento de rede universitária.")
    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Carregar topologia (JSON)",
        type=["json"],
        help="O arquivo deve conter as chaves **vertices** e **arestas**.",
    )

    st.divider()
    st.markdown(
        """
        **Fórmula de custo:**
        ```
        Custo = (distância × fator_terreno)
              + (obstáculos × 50)
              + (andares × 100)
        ```
        """
    )
    st.caption("Algoritmo: **Kruskal** com Union-Find (path compression + union by rank)")

# ---------------------------------------------------------------------------
# Área principal — Cabeçalho
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-title">🌐 CampusNet</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Planejamento de cabeamento de rede via Árvore Geradora Mínima</p>',
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info(
        "👈 Carregue um arquivo JSON de topologia na barra lateral para começar.",
        icon="📋",
    )
    st.stop()

# ---------------------------------------------------------------------------
# Processamento via Camada de Serviço
# ---------------------------------------------------------------------------
try:
    raw_bytes: bytes = uploaded_file.read()
    result = process_campus_network(raw_bytes)
except (ValueError, KeyError) as exc:
    st.error(f"❌ Erro ao processar o arquivo: {exc}")
    st.stop()

graph = result.graph

# ---------------------------------------------------------------------------
# Métricas do grafo
# ---------------------------------------------------------------------------
col_status, col_v, col_e = st.columns(3)

with col_v:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Vértices</div>'
        f'<div class="metric-value">{graph.num_vertices}</div></div>',
        unsafe_allow_html=True,
    )
with col_e:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Arestas</div>'
        f'<div class="metric-value">{graph.num_edges}</div></div>',
        unsafe_allow_html=True,
    )
with col_status:
    badge = (
        '<span class="badge-ok">✔ Conexo</span>'
        if result.is_connected
        else '<span class="badge-err">✘ Desconexo</span>'
    )
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Conectividade</div>'
        f'<div class="metric-value">{badge}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Erro: grafo desconexo
# ---------------------------------------------------------------------------
if not result.is_connected:
    st.error(
        f"🚫 **Grafo desconexo!** Não é possível calcular a AGM.\n\n"
        f"Vértices isolados (sem caminho para o restante da rede): "
        f"**{', '.join(result.isolated_nodes)}**\n\n"
        f"Adicione arestas que conectem esses nós e recarregue o arquivo."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Resultados da AGM
# ---------------------------------------------------------------------------
st.divider()
st.subheader("📊 Resultado da AGM")

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Custo Total (R$)</div>'
        f'<div class="metric-value">R$ {result.total_cost:,.2f}</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Cabos na AGM</div>'
        f'<div class="metric-value">{len(result.mst_edges)}</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Tempo de Execução</div>'
        f'<div class="metric-value">{result.total_time_ms:.3f} ms</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Visualização do Grafo
# ---------------------------------------------------------------------------
st.subheader("🗺️ Visualização do Grafo e da AGM")
st.caption(
    "Arestas **azul ciano** = selecionadas pela AGM | "
    "Arestas **cinza tracejado** = descartadas pelo Kruskal"
)

fig = plot_campus_graph(graph, result.mst_edges)
st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Tabela de cabos
# ---------------------------------------------------------------------------
st.subheader("🔌 Cabos selecionados pela AGM")
table_data = [
    {
        "Nº": i + 1,
        "Origem": e.origem,
        "Destino": e.destino,
        "Custo (R$)": f"R$ {e.peso:,.2f}",
    }
    for i, e in enumerate(result.mst_edges)
]
st.dataframe(table_data, use_container_width=True, hide_index=True)

st.divider()

# ---------------------------------------------------------------------------
# Detalhes de desempenho
# ---------------------------------------------------------------------------
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

st.caption("CampusNet · Teoria dos Grafos · Python 3.10+ · Streamlit")
