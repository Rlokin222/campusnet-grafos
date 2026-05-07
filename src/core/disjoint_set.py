# Implementação do Union-Find (Conjuntos Disjuntos) usado pelo Kruskal
# para detectar ciclos na hora de montar a AGM.
#
# Duas otimizações que aprendemos na aula:
#   - Path Compression: quando buscamos a raiz de um elemento, a gente
#     já atualiza o pai dele para apontar direto pra raiz. Assim a
#     próxima busca é quase imediata.
#   - Union by Rank: na hora de unir dois conjuntos, a gente coloca a
#     árvore menor embaixo da maior. Isso evita que a estrutura fique
#     desequilibrada.
# Com essas duas juntas, cada operação roda em O(α(n)) — praticamente O(1).


class UnionFind:
    """
    Estrutura de conjuntos disjuntos para o algoritmo de Kruskal.

    Cada vértice começa no seu próprio conjunto. Quando adicionamos uma
    aresta à AGM, unimos os conjuntos dos dois vértices. Se eles já
    estiverem no mesmo conjunto, a aresta criaria um ciclo, e então descartamos.
    """

    def __init__(self, vertices: list[str]) -> None:
        # No início, cada vértice é seu próprio "pai" (conjunto individual)
        self._parent: dict[str, str] = {v: v for v in vertices}
        # O rank serve como estimativa da altura da árvore (usamos no union)
        self._rank: dict[str, int] = {v: 0 for v in vertices}

    def find(self, x: str) -> str:
        """
        Sobe na árvore até encontrar a raiz do conjunto de x.
        Enquanto sobe, já atualiza o pai de x para apontar direto
        pra raiz, isso é o path compression.
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])  # aponta direto pra raiz
        return self._parent[x]

    def union(self, x: str, y: str) -> bool:
        """
        tenta unir os conjuntos de x e y.

        retorna True se a união aconteceu (os dois estavam em conjuntos
        diferentes, e então, é uma aresta válida para a AGM).
        retorna False se já estavam no mesmo conjunto, formando um ciclo.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # já estão conectados, não podemos adicionar essa aresta

        # Coloca a árvore menor embaixo da maior (union by rank)
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x

        # Só aumenta o rank quando as duas árvores têm a mesma altura
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        return True

    def connected(self, x: str, y: str) -> bool:
        """retorna True se x e y já estão no mesmo conjunto."""
        return self.find(x) == self.find(y)
