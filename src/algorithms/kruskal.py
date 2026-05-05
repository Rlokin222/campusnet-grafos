"""
Implementação do Algoritmo de Kruskal para cálculo da Árvore Geradora Mínima (AGM).

Complexidade:
    - Ordenação das arestas: O(E log E)
    - Iteração com Union-Find:  O(E · α(V))  →  praticamente O(E)
    Total: O(E log E)
"""
from src.core.disjoint_set import UnionFind
from src.core.edge import Edge
from src.core.graph import Graph


def run_kruskal(graph: Graph) -> tuple[list[Edge], float]:
    """
    Executa o Algoritmo de Kruskal sobre o grafo recebido e retorna a AGM.

    O algoritmo:
        1. Ordena todas as arestas por peso crescente.
        2. Inicializa o Union-Find com todos os vértices.
        3. Para cada aresta, verifica se conecta dois componentes distintos.
           - Se sim: adiciona à AGM e une os componentes.
           - Se não: descarta (formaria ciclo).
        4. Para quando a AGM tem V-1 arestas (grafo conexo).

    Args:
        graph: Instância de Graph devidamente populada.

    Returns:
        Tupla (mst_edges, total_cost):
            mst_edges  - lista de Edge que compõem a AGM, em ordem de adição.
            total_cost - soma dos pesos da AGM.

    Raises:
        ValueError: Se o grafo for vazio ou desconexo (AGM impossível).
    """
    if graph.num_vertices == 0:
        return [], 0.0

    # Passo 1 — Ordenação O(E log E)
    sorted_edges: list[Edge] = sorted(graph.edges)  # Edge é ordered=True por peso

    # Passo 2 — Inicialização do Union-Find
    uf = UnionFind(graph.vertices)

    mst_edges: list[Edge] = []
    total_cost: float = 0.0
    target_size = graph.num_vertices - 1  # Uma AGM tem exatamente V-1 arestas

    # Passo 3 — Iteração O(E · α(V))
    for edge in sorted_edges:
        if uf.union(edge.origem, edge.destino):
            mst_edges.append(edge)
            total_cost += edge.peso

            # Otimização: encerra cedo quando a AGM está completa
            if len(mst_edges) == target_size:
                break

    # Passo 4 — Validação de conectividade
    if len(mst_edges) < target_size:
        raise ValueError(
            f"O grafo é desconexo. A AGM requer {target_size} arestas, "
            f"mas apenas {len(mst_edges)} foram encontradas."
        )

    return mst_edges, round(total_cost, 4)
