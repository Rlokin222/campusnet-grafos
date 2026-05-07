# Representa uma aresta do grafo — tem origem, destino e peso (custo).
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Edge:
    """
    Aresta do grafo do campus.

    O campo 'peso' vem primeiro porque o Python usa a ordem dos campos
    para comparar dataclasses. O Kruskal precisa ordenar as arestas
    do menor para o maior custo, então isso facilita muito.

    Atributos:
        peso:    Custo calculado pela fórmula do projeto.
        origem:  Nome do prédio de onde sai o cabo.
        destino: Nome do prédio onde o cabo chega.
    """

    peso: float
    origem: str
    destino: str

    def __str__(self) -> str:
        return f"{self.origem} <-> {self.destino}  (custo: R$ {self.peso:.2f})"
