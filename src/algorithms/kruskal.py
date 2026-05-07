# Implementação do Algoritmo de Kruskal para calcular a AGM (Árvore Geradora Mínima).
#
# A ideia é simples:
#   1. Ordena todas as arestas do menor para o maior custo.
#   2. Vai pegando aresta por aresta — se ela conectar dois componentes
#      diferentes (sem ciclo), adiciona na AGM.
#   3. Para quando a AGM tiver V-1 arestas (uma AGM sempre tem exatamente isso).
#
# Complexidade total: O(E log E), dominada pela etapa de ordenação.
from src.core.disjoint_set import UnionFind
from src.core.edge import Edge
from src.core.graph import Graph


def run_kruskal(graph: Graph) -> tuple[list[Edge], float]:
    """
    Roda o Kruskal no grafo e devolve as arestas da AGM com o custo total.

    Se o grafo estiver vazio, devolve uma lista vazia e custo zero.
    Se o grafo for desconexo, lança um ValueError — não tem AGM possível.
    """
    if graph.num_vertices == 0:
        return [], 0.0

    # Passo 1 — Ordena as arestas pelo peso (menor custo primeiro)
    # O dataclass Edge já sabe se comparar por peso, então sorted() funciona direto
    sorted_edges: list[Edge] = sorted(graph.edges)  # O(E log E)

    # Passo 2 — Inicializa o Union-Find com todos os vértices do grafo
    uf = UnionFind(graph.vertices)  # O(V)

    mst_edges: list[Edge] = []
    total_cost: float = 0.0
    target_size = graph.num_vertices - 1  # a AGM tem exatamente V-1 arestas

    # Passo 3 — Percorre as arestas em ordem crescente de custo
    for edge in sorted_edges:  # O(E · α(V)) ≈ O(E)
        # union() retorna True se os vértices estavam em componentes diferentes
        # (ou seja, a aresta não forma ciclo) — aí podemos adicionar
        if uf.union(edge.origem, edge.destino):
            mst_edges.append(edge)
            total_cost += edge.peso

            # Otimização: se já temos V-1 arestas, a AGM está completa
            if len(mst_edges) == target_size:
                break

    # Se não conseguimos V-1 arestas, o grafo é desconexo
    if len(mst_edges) < target_size:
        raise ValueError(
            f"O grafo é desconexo. Precisamos de {target_size} arestas, "
            f"mas só encontramos {len(mst_edges)}."
        )

    return mst_edges, round(total_cost, 4)
