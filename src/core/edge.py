"""
Módulo que define a estrutura de uma aresta do grafo.
"""
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Edge:
    """
    Representa uma aresta não-dirigida e ponderada do grafo.

    Attributes:
        peso:   Custo calculado pela fórmula de negócio (usado na ordenação).
        origem: Identificador do vértice de origem.
        destino: Identificador do vértice de destino.
    """

    # 'peso' é o primeiro campo para que a ordenação natural (order=True)
    # compare arestas pelo custo, como exige o Kruskal.
    peso: float
    origem: str
    destino: str

    def __str__(self) -> str:
        return f"{self.origem} <-> {self.destino}  (peso: {self.peso:.2f})"
