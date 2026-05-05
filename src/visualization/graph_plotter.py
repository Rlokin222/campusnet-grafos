"""
Módulo de visualização do grafo — CampusNet.

Renderiza o grafo completo do campus com destaque visual para as arestas
que compõem a Árvore Geradora Mínima (AGM).

Dependências: networkx, matplotlib
"""
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx

from src.core.edge import Edge
from src.core.graph import Graph

# Paleta de cores
_BG_COLOR = "#0e1117"
_NODE_COLOR = "#7b2ff7"
_MST_EDGE_COLOR = "#00d4ff"
_NON_MST_EDGE_COLOR = "#3d4a5c"
_LABEL_COLOR = "white"
_TITLE_COLOR = "white"
_MST_LABEL_COLOR = "#00d4ff"


def _build_nx_graph(graph: Graph) -> nx.Graph:
    """Constrói um grafo NetworkX a partir da instância de Graph do domínio."""
    G: nx.Graph = nx.Graph()
    G.add_nodes_from(graph.vertices)
    for edge in graph.edges:
        G.add_edge(edge.origem, edge.destino, weight=edge.peso)
    return G


def plot_campus_graph(
    graph: Graph,
    mst_edges: list[Edge],
    figsize: tuple[int, int] = (14, 8),
    seed: int = 42,
) -> plt.Figure:
    """
    Gera a figura matplotlib com o grafo completo do campus.

    - Arestas da AGM: destacadas em azul ciano com rótulo de peso.
    - Arestas descartadas: exibidas em cinza translúcido.
    - Vértices: roxo com rótulo branco.

    Args:
        graph:     Grafo completo do campus.
        mst_edges: Lista de arestas selecionadas pelo Kruskal.
        figsize:   Tamanho da figura em polegadas.
        seed:      Semente do layout spring para reprodutibilidade.

    Returns:
        Objeto Figure do matplotlib pronto para `st.pyplot()`.
    """
    G = _build_nx_graph(graph)

    # Conjuntos de arestas para separar MST das demais
    mst_set: set[frozenset[str]] = {
        frozenset([e.origem, e.destino]) for e in mst_edges
    }
    mst_edge_list = [(e.origem, e.destino) for e in mst_edges]
    non_mst_edge_list = [
        (u, v)
        for u, v in G.edges()
        if frozenset([u, v]) not in mst_set
    ]

    # Layout
    pos = nx.spring_layout(G, seed=seed, k=2.5)

    # ── Figura ────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=figsize, facecolor=_BG_COLOR)
    ax.set_facecolor(_BG_COLOR)

    # Arestas descartadas (fundo)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=non_mst_edge_list,
        edge_color=_NON_MST_EDGE_COLOR,
        width=1.2,
        alpha=0.6,
        style="dashed",
        ax=ax,
    )

    # Arestas da AGM (destaque)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=mst_edge_list,
        edge_color=_MST_EDGE_COLOR,
        width=3.0,
        alpha=1.0,
        ax=ax,
    )

    # Nós
    nx.draw_networkx_nodes(
        G, pos,
        node_color=_NODE_COLOR,
        node_size=900,
        alpha=0.95,
        ax=ax,
    )

    # Rótulos dos nós
    nx.draw_networkx_labels(
        G, pos,
        font_color=_LABEL_COLOR,
        font_size=7.5,
        font_weight="bold",
        ax=ax,
    )

    # Rótulos de peso apenas nas arestas da AGM
    mst_weights = {(e.origem, e.destino): f"R${e.peso:,.0f}" for e in mst_edges}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=mst_weights,
        font_color=_MST_EDGE_COLOR,
        font_size=7,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=_BG_COLOR, alpha=0.7),
        ax=ax,
    )

    # Legenda
    legend_handles = [
        mpatches.Patch(color=_MST_EDGE_COLOR, label=f"Aresta da AGM ({len(mst_edges)})"),
        mpatches.Patch(color=_NON_MST_EDGE_COLOR, label=f"Aresta descartada ({len(non_mst_edge_list)})"),
        mpatches.Patch(color=_NODE_COLOR, label=f"Nó ({graph.num_vertices})"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        facecolor="#1a1a2e",
        edgecolor="#2d3748",
        labelcolor=_LABEL_COLOR,
        fontsize=9,
    )

    ax.set_title(
        "Grafo do Campus — Arestas da AGM destacadas em azul",
        color=_TITLE_COLOR,
        fontsize=13,
        pad=16,
        fontweight="bold",
    )
    ax.axis("off")
    fig.tight_layout()

    return fig
