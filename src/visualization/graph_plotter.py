# Módulo de visualização — desenha o grafo do campus com matplotlib e networkx.
# Mostra todas as arestas (com peso), destacando em azul as que fazem parte da AGM.
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx

from src.core.edge import Edge
from src.core.graph import Graph

# Paleta de cores da interface
_BG_COLOR = "#0e1117"
_NODE_COLOR = "#7b2ff7"
_NODE_BORDER = "#00d4ff"
_MST_EDGE_COLOR = "#00d4ff"
_NON_MST_EDGE_COLOR = "#3d4a5c"
_LABEL_COLOR = "white"
_MST_LABEL_COLOR = "#00d4ff"
_NON_MST_LABEL_COLOR = "#5a6a7e"


def _build_nx_graph(graph: Graph) -> nx.Graph:
    """Converte nosso Graph para um grafo do networkx (necessário para o desenho)."""
    G: nx.Graph = nx.Graph()
    G.add_nodes_from(graph.vertices)
    for edge in graph.edges:
        G.add_edge(edge.origem, edge.destino, weight=edge.peso)
    return G


def plot_campus_graph(
    graph: Graph,
    mst_edges: list[Edge],
    figsize: tuple[int, int] = (15, 9),
    seed: int = 42,
) -> plt.Figure:
    """
    Gera a figura com o grafo completo do campus.

    - Arestas da AGM: azul ciano, mais grossas, com o peso em destaque.
    - Arestas descartadas: cinza tracejado, finas, com peso menor e apagado.
    - Vértices: roxo com borda azul ciano e rótulo branco.
    """
    G = _build_nx_graph(graph)

    # Separa as arestas da AGM das que foram descartadas
    mst_set: set[frozenset[str]] = {
        frozenset([e.origem, e.destino]) for e in mst_edges
    }
    mst_edge_list = [(e.origem, e.destino) for e in mst_edges]
    non_mst_edge_list = [
        (u, v)
        for u, v in G.edges()
        if frozenset([u, v]) not in mst_set
    ]

    # Layout spring — organiza os nós de forma que fique legível
    pos = nx.spring_layout(G, seed=seed, k=2.8)

    fig, ax = plt.subplots(figsize=figsize, facecolor=_BG_COLOR)
    ax.set_facecolor(_BG_COLOR)

    # Primeiro desenha as arestas descartadas (embaixo, para não cobrir as da AGM)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=non_mst_edge_list,
        edge_color=_NON_MST_EDGE_COLOR,
        width=1.0,
        alpha=0.5,
        style="dashed",
        ax=ax,
    )

    # Depois as arestas da AGM (em cima, bem visíveis)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=mst_edge_list,
        edge_color=_MST_EDGE_COLOR,
        width=3.5,
        alpha=1.0,
        ax=ax,
    )

    # Nós com borda azul para dar efeito de glow
    nx.draw_networkx_nodes(
        G, pos,
        node_color=_NODE_COLOR,
        node_size=1100,
        alpha=0.95,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        G, pos,
        node_color="none",
        node_size=1200,
        edgecolors=_NODE_BORDER,
        linewidths=2.0,
        ax=ax,
    )

    # Rótulos dos nós (nome do prédio)
    nx.draw_networkx_labels(
        G, pos,
        font_color=_LABEL_COLOR,
        font_size=7,
        font_weight="bold",
        ax=ax,
    )

    # Pesos das arestas da AGM (em destaque, azul ciano)
    mst_weights = {(e.origem, e.destino): f"R${e.peso:,.0f}" for e in mst_edges}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=mst_weights,
        font_color=_MST_LABEL_COLOR,
        font_size=7.5,
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#0d1b2a", alpha=0.85, edgecolor=_MST_EDGE_COLOR),
        ax=ax,
    )

    # Pesos das arestas descartadas (menores e apagados)
    non_mst_weights = {
        (u, v): f"R${G[u][v]['weight']:,.0f}"
        for u, v in non_mst_edge_list
    }
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=non_mst_weights,
        font_color=_NON_MST_LABEL_COLOR,
        font_size=6,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=_BG_COLOR, alpha=0.6, edgecolor="none"),
        ax=ax,
    )

    # Legenda
    legend_handles = [
        mpatches.Patch(color=_MST_EDGE_COLOR, label=f"AGM — {len(mst_edges)} cabos selecionados"),
        mpatches.Patch(color=_NON_MST_EDGE_COLOR, label=f"Descartadas — {len(non_mst_edge_list)} conexões"),
        mpatches.Patch(color=_NODE_COLOR, label=f"{graph.num_vertices} prédios (vértices)"),
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
        "Grafo do Campus — Arestas da AGM em azul ciano",
        color="white",
        fontsize=13,
        pad=18,
        fontweight="bold",
    )
    ax.axis("off")
    fig.tight_layout()

    return fig
