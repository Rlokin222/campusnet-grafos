# Classe principal do grafo — aqui ficam os vértices, arestas e a lógica
# de calcular o custo de cada ligação entre os prédios do campus.
from collections import defaultdict, deque
from typing import Any

from src.core.edge import Edge


class Graph:
    """
    Grafo não-dirigido e ponderado representado por Lista de Adjacência.

    Aqui a gente guarda os prédios do campus como vértices e as possíveis
    conexões de cabo como arestas. O custo de cada aresta é calculado
    automaticamente pela fórmula do projeto:

        Custo = (distancia × fator_terreno) + (obstaculos × 50) + (andares × 100)
    """

    def __init__(self) -> None:
        # Conjunto com os nomes de todos os prédios (vértices)
        self._vertices: set[str] = set()
        # Lista de adjacência: para cada prédio, quais outros ele alcança
        self._adj: dict[str, list[Edge]] = defaultdict(list)
        # Lista com todas as arestas (sem duplicatas — só uma direção cada)
        self._edges: list[Edge] = []
        # Coordenadas opcionais para plotagem sobre mapas (x, y)
        self._coords: dict[str, tuple[float, float]] = {}

    @property
    def vertices(self) -> list[str]:
        """Devolve a lista de vértices em ordem alfabética."""
        return sorted(self._vertices)

    @property
    def edges(self) -> list[Edge]:
        """Devolve todas as arestas do grafo."""
        return list(self._edges)

    @property
    def num_vertices(self) -> int:
        return len(self._vertices)

    @property
    def num_edges(self) -> int:
        return len(self._edges)

    def add_vertex(self, label: str, x: float | None = None, y: float | None = None) -> None:
        """Adiciona um prédio (vértice). Opcionalmente com coordenadas para mapa."""
        self._vertices.add(label)
        if x is not None and y is not None:
            self._coords[label] = (x, y)

    @property
    def coords(self) -> dict[str, tuple[float, float]]:
        """Devolve as coordenadas dos vértices (se existirem)."""
        return dict(self._coords)

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
        Calcula o custo da ligação e adiciona a aresta no grafo.

        A fórmula considera distância, dificuldade do terreno, obstáculos
        físicos (paredes, dutos) e diferença de andares entre os prédios.
        """
        # Fórmula de custo definida no projeto
        peso = (distancia * fator_terreno) + (obstaculos * 50) + (andares * 100)
        edge = Edge(peso=round(peso, 4), origem=origem, destino=destino)

        # Registra os dois prédios como vértices (caso ainda não existam)
        self._vertices.add(origem)
        self._vertices.add(destino)

        # Grafo não-dirigido: a aresta aparece nos dois lados da adjacência
        self._adj[origem].append(edge)
        self._adj[destino].append(Edge(peso=edge.peso, origem=destino, destino=origem))

        # Mas na lista global guardamos só uma vez (sem duplicata)
        self._edges.append(edge)

        return edge

    def check_connectivity(self) -> tuple[bool, list[str]]:
        """
        Verifica se dá para chegar em todos os prédios a partir de qualquer um.

        Usamos BFS: começamos de um vértice e tentamos visitar todos os outros.
        Se sobrar algum não visitado, o grafo é desconexo e não tem AGM.

        Retorna:
            (True, [])           → todos conectados, pode rodar o Kruskal.
            (False, [v1, v2, …]) → lista com os prédios isolados.
        """
        if not self._vertices:
            return True, []

        visited: set[str] = set()
        start = next(iter(sorted(self._vertices)))  # começa do primeiro em ordem alfabética
        queue: deque[str] = deque([start])
        visited.add(start)

        # BFS clássica
        while queue:
            current = queue.popleft()
            for edge in self._adj[current]:
                if edge.destino not in visited:
                    visited.add(edge.destino)
                    queue.append(edge.destino)

        # Prédios que não foram alcançados pela BFS
        isolated = sorted(self._vertices - visited)
        is_connected = len(isolated) == 0
        return is_connected, isolated

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Graph":
        """
        Monta o grafo a partir do dicionário lido do arquivo JSON.

        O dicionário precisa ter as chaves 'vertices' e 'arestas',
        que é o formato que o file_reader já entrega validado.
        """
        graph = cls()

        vertices_data = data.get("vertices", [])
        if isinstance(vertices_data, dict):
            # Novo formato com coordenadas: {"Predio": {"x": 10, "y": 20}}
            for vertex, coords in vertices_data.items():
                graph.add_vertex(vertex, coords.get("x"), coords.get("y"))
        else:
            # Formato clássico: ["Predio A", "Predio B"]
            for vertex in vertices_data:
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
