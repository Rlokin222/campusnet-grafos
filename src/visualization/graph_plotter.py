# Módulo de visualização — desenha o grafo do campus com matplotlib e networkx.
# Suporta plotagem lúdica padrão ou sobreposição sobre mapas do mundo real.
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

from src.core.edge import Edge
from src.core.graph import Graph

# Paleta Corporativa (Enterprise)
_BG_COLOR = "#1e222d" # Dark slate
_NODE_COLOR = "#2962ff" # Professional Blue
_NODE_BORDER = "#ffffff"
_MST_EDGE_COLOR = "#2962ff"
_NON_MST_EDGE_COLOR = "#434651"
_LABEL_COLOR = "#ffffff"
_MST_LABEL_COLOR = "#ffffff"
_MST_LABEL_BG = "#1e222d"
_NON_MST_LABEL_COLOR = "#8a8d93"


def _build_nx_graph(graph: Graph) -> nx.Graph:
    """Converte nosso Graph para um grafo do networkx."""
    G: nx.Graph = nx.Graph()
    G.add_nodes_from(graph.vertices)
    for edge in graph.edges:
        G.add_edge(edge.origem, edge.destino, weight=edge.peso)
    return G


def plot_campus_graph(
    graph: Graph,
    mst_edges: list[Edge],
    figsize: tuple[int, int] = (16, 9),
    seed: int = 42,
    bg_map_type: str = "Nenhum"
) -> plt.Figure:
    """
    Gera a figura com o grafo completo do campus.

    - bg_map_type: "Blueprint", "Satélite" ou "Nenhum".
    """
    G = _build_nx_graph(graph)

    mst_set: set[frozenset[str]] = {
        frozenset([e.origem, e.destino]) for e in mst_edges
    }
    mst_edge_list = [(e.origem, e.destino) for e in mst_edges]
    non_mst_edge_list = [
        (u, v)
        for u, v in G.edges()
        if frozenset([u, v]) not in mst_set
    ]

    # Decide layout
    coords = graph.coords
    use_map = False
    img = None
    
    # Se houver mapa selecionado e imagem existir
    if bg_map_type in ["Blueprint", "Satélite"]:
        filename = "campus_blueprint.png" if bg_map_type == "Blueprint" else "campus_satellite.png"
        img_path = Path("data/assets") / filename
        if img_path.exists():
            img = mpimg.imread(str(img_path))
            use_map = True

    if use_map and coords and len(coords) == graph.num_vertices:
        # Usa coordenadas reais do JSON
        pos = coords
    else:
        # Fallback para layout padrão
        pos = nx.spring_layout(G, seed=seed, k=2.8)
        use_map = False

    fig, ax = plt.subplots(figsize=figsize, facecolor=_BG_COLOR)
    ax.set_facecolor(_BG_COLOR)

    if use_map and img is not None:
        # Desenha a imagem de fundo. extent=[esquerda, direita, base, topo]
        # Imagens têm Y invertido (0 é o topo). Nossa coordenada também (y=1000 é base).
        ax.imshow(img, extent=[0, 1920, 1080, 0])
        ax.set_xlim(0, 1920)
        ax.set_ylim(1080, 0) # Eixo Y invertido para casar com a matriz da imagem

    # Arestas descartadas
    nx.draw_networkx_edges(
        G, pos,
        edgelist=non_mst_edge_list,
        edge_color=_NON_MST_EDGE_COLOR,
        width=1.0,
        alpha=0.6,
        style="dashed",
        ax=ax,
    )

    # Arestas da AGM
    nx.draw_networkx_edges(
        G, pos,
        edgelist=mst_edge_list,
        edge_color=_MST_EDGE_COLOR,
        width=3.5,
        alpha=1.0,
        ax=ax,
    )

    # Nós
    nx.draw_networkx_nodes(
        G, pos,
        node_color=_NODE_COLOR,
        node_size=1000,
        edgecolors=_NODE_BORDER,
        linewidths=1.5,
        alpha=0.95,
        ax=ax,
    )

    # Rótulos dos nós
    nx.draw_networkx_labels(
        G, pos,
        font_color=_LABEL_COLOR,
        font_size=8,
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.2", facecolor=_NODE_COLOR, alpha=0.9, edgecolor="none"),
        ax=ax,
    )

    # Pesos das arestas da AGM
    mst_weights = {(e.origem, e.destino): f"R$ {e.peso:,.0f}" for e in mst_edges}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=mst_weights,
        font_color=_MST_LABEL_COLOR,
        font_size=8,
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=_MST_LABEL_BG, alpha=0.9, edgecolor=_MST_EDGE_COLOR),
        ax=ax,
    )

    # Pesos das arestas descartadas
    non_mst_weights = {
        (u, v): f"R$ {G[u][v]['weight']:,.0f}"
        for u, v in non_mst_edge_list
    }
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=non_mst_weights,
        font_color=_NON_MST_LABEL_COLOR,
        font_size=7,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=_BG_COLOR, alpha=0.7, edgecolor="none"),
        ax=ax,
    )

    legend_handles = [
        mpatches.Patch(color=_MST_EDGE_COLOR, label=f"Cabos Primários (AGM) - {len(mst_edges)} conexões"),
        mpatches.Patch(color=_NON_MST_EDGE_COLOR, label=f"Rotas Alternativas - {len(non_mst_edge_list)} conexões"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        facecolor=_BG_COLOR,
        edgecolor=_NON_MST_EDGE_COLOR,
        labelcolor=_LABEL_COLOR,
        fontsize=10,
    )

    # Remove título interno para deixar mais "dashboard", remove eixos
    ax.axis("off")
    fig.tight_layout(pad=0)

    return fig
