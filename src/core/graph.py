"""
Módulo que define a classe Graph (grafo não-dirigido e ponderado).
Usa Lista de Adjacência como estrutura interna.
"""
from collections import defaultdict, deque
from typing import Any

from src.core.edge import Edge


class Graph:
    """
    Grafo não-dirigido e ponderado representado por Lista de Adjacência.

    A classe encapsula a fórmula de negócio do CampusNet:
        Custo = (distancia * fator_terreno) + (obstaculos * 50) + (andares * 100)
    """

    def __init__(self) -> None:
        # Conjunto de vértices (preserva ordem de inserção em Python 3.7+)
        self._vertices: set[str] = set()
        # Lista de adjacência: vértice → lista de arestas
        self._adj: dict[str, list[Edge]] = defaultdict(list)
        # Lista global de todas as arestas (sem duplicatas direcionais)
        self._edges: list[Edge] = []

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------

    @property
    def vertices(self) -> list[str]:
        """Retorna a lista ordenada de vértices."""
        return sorted(self._vertices)

    @property
    def edges(self) -> list[Edge]:
        """Retorna todas as arestas do grafo."""
        return list(self._edges)

    @property
    def num_vertices(self) -> int:
        return len(self._vertices)

    @property
    def num_edges(self) -> int:
        return len(self._edges)

    # ------------------------------------------------------------------
    # Mutação
    # ------------------------------------------------------------------

    def add_vertex(self, label: str) -> None:
        """Adiciona um vértice isolado ao grafo."""
        self._vertices.add(label)

    def add_edge(
        self,
        origem: str,
        destino: str,
        distancia: float,
        fator_terreno: float,
        obstaculos: int,
        andares: int,
    ) -> Edge:
        """
        Calcula o peso via fórmula de negócio e insere a aresta (não-dirigida).

        Fórmula:
            Custo = (distancia * fator_terreno) + (obstaculos * 50) + (andares * 100)

        Args:
            origem:        Vértice de origem.
            destino:       Vértice de destino.
            distancia:     Distância física em metros.
            fator_terreno: Multiplicador do terreno (1.0 = plano, 1.5 = difícil).
            obstaculos:    Número de obstáculos (paredes, dutos, etc.).
            andares:       Diferença de andares entre os pontos.

        Returns:
            A instância de Edge criada.
        """
        peso = (distancia * fator_terreno) + (obstaculos * 50) + (andares * 100)
        edge = Edge(peso=round(peso, 4), origem=origem, destino=destino)

        # Registra os vértices automaticamente
        self._vertices.add(origem)
        self._vertices.add(destino)

        # Lista de adjacência (grafo não-dirigido → inserção em ambas as direções)
        self._adj[origem].append(edge)
        self._adj[destino].append(Edge(peso=edge.peso, origem=destino, destino=origem))

        # Mantém apenas uma cópia na lista global de arestas
        self._edges.append(edge)

        return edge

    # ------------------------------------------------------------------
    # Conectividade
    # ------------------------------------------------------------------

    def check_connectivity(self) -> tuple[bool, list[str]]:
        """
        Verifica se o grafo é conexo usando BFS a partir do primeiro vértice.

        Returns:
            (True, [])           → Grafo conexo.
            (False, [v1, v2, …]) → Grafo desconexo; lista contém os vértices
                                   não alcançáveis a partir da origem.
        """
        if not self._vertices:
            return True, []

        visited: set[str] = set()
        start = next(iter(sorted(self._vertices)))
        queue: deque[str] = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            for edge in self._adj[current]:
                if edge.destino not in visited:
                    visited.add(edge.destino)
                    queue.append(edge.destino)

        isolated = sorted(self._vertices - visited)
        is_connected = len(isolated) == 0
        return is_connected, isolated

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Graph":
        """
        Constrói um grafo a partir do dicionário retornado pelo file_reader.

        Args:
            data: Dicionário com 'vertices' (list[str]) e 'arestas' (list[dict]).

        Returns:
            Instância de Graph populada.
        """
        graph = cls()

        for vertex in data.get("vertices", []):
            graph.add_vertex(vertex)

        for aresta in data.get("arestas", []):
            graph.add_edge(
                origem=aresta["origem"],
                destino=aresta["destino"],
                distancia=float(aresta["distancia"]),
                fator_terreno=float(aresta["fator_terreno"]),
                obstaculos=int(aresta["obstaculos"]),
                andares=int(aresta["andares"]),
            )

        return graph

    def __repr__(self) -> str:
        return f"Graph(vertices={self.num_vertices}, edges={self.num_edges})"
