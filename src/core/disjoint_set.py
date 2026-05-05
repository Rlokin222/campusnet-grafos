"""
Implementação da estrutura Disjoint Set (Union-Find) com:
- Path Compression  →  find() quase O(1)
- Union by Rank     →  mantém a árvore rasa
Complexidade amortizada: O(α(n)) por operação, onde α é a inversa de Ackermann.
"""


class UnionFind:
    """
    Estrutura de conjuntos disjuntos para detecção de ciclos no Kruskal.

    Args:
        vertices: Sequência de identificadores únicos dos vértices.
    """

    def __init__(self, vertices: list[str]) -> None:
        # Cada vértice começa como seu próprio representante
        self._parent: dict[str, str] = {v: v for v in vertices}
        # Rank é usado como estimativa da altura da árvore
        self._rank: dict[str, int] = {v: 0 for v in vertices}

    # ------------------------------------------------------------------
    # Operações públicas
    # ------------------------------------------------------------------

    def find(self, x: str) -> str:
        """
        Retorna o representante (raiz) do conjunto que contém *x*.
        Aplica Path Compression durante a busca.
        """
        if self._parent[x] != x:
            # Compressão: aponta diretamente para a raiz
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: str, y: str) -> bool:
        """
        Une os conjuntos que contêm *x* e *y*.

        Returns:
            True  se os elementos estavam em conjuntos diferentes (aresta válida).
            False se já pertenciam ao mesmo conjunto (formaria ciclo).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Ciclo detectado

        # Union by Rank: a árvore menor pendurada na maior
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x

        # Incrementa rank apenas quando as duas árvores têm a mesma altura
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        return True

    def connected(self, x: str, y: str) -> bool:
        """Retorna True se *x* e *y* pertencem ao mesmo conjunto."""
        return self.find(x) == self.find(y)
