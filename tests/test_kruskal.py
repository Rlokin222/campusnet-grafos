"""
Testes unitários do Algoritmo de Kruskal – CampusNet.
Execute com:  pytest tests/test_kruskal.py -v
"""
import pytest

from src.algorithms.kruskal import run_kruskal
from src.core.graph import Graph


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_simple_graph() -> Graph:
    """
    Grafo-triângulo com 3 vértices (A, B, C) e 3 arestas:

        A --[distancia=100, fator=1.0, obs=0, andares=0]--> B  custo=100
        B --[distancia=150, fator=1.0, obs=0, andares=0]--> C  custo=150
        A --[distancia=200, fator=1.0, obs=0, andares=0]--> C  custo=200

    AGM esperada: A-B (100) + B-C (150) = 250
    """
    g = Graph()
    g.add_edge("A", "B", distancia=100.0, fator_terreno=1.0, obstaculos=0, andares=0)
    g.add_edge("B", "C", distancia=150.0, fator_terreno=1.0, obstaculos=0, andares=0)
    g.add_edge("A", "C", distancia=200.0, fator_terreno=1.0, obstaculos=0, andares=0)
    return g


def _make_complete_graph() -> Graph:
    """
    Grafo completo K4 com 4 vértices e 6 arestas.
    Vértices: V1, V2, V3, V4.

    Custos (distancia * fator, sem obstaculos/andares):
        V1-V2 = 10   V1-V3 = 20   V1-V4 = 30
        V2-V3 = 15   V2-V4 = 25   V3-V4 = 35

    AGM de custo mínimo: V1-V2(10) + V2-V3(15) + V1-V4(30) = 55
    """
    g = Graph()
    edges = [
        ("V1", "V2", 10.0),
        ("V1", "V3", 20.0),
        ("V1", "V4", 30.0),
        ("V2", "V3", 15.0),
        ("V2", "V4", 25.0),
        ("V3", "V4", 35.0),
    ]
    for u, v, d in edges:
        g.add_edge(u, v, distancia=d, fator_terreno=1.0, obstaculos=0, andares=0)
    return g


# ---------------------------------------------------------------------------
# test_caso_base
# ---------------------------------------------------------------------------

class TestCasoBase:
    """Grafo simples com 3 vértices e 3 arestas."""

    def test_custo_total_correto(self):
        """A AGM do triângulo A-B-C deve custar exatamente 250."""
        graph = _make_simple_graph()
        _, total = run_kruskal(graph)
        assert total == pytest.approx(250.0), f"Custo esperado 250, obtido {total}"

    def test_numero_de_arestas_na_agm(self):
        """Uma AGM de 3 vértices deve ter exatamente 2 arestas (V-1)."""
        graph = _make_simple_graph()
        mst, _ = run_kruskal(graph)
        assert len(mst) == 2, f"Esperava 2 arestas, obteve {len(mst)}"

    def test_aresta_mais_cara_excluida(self):
        """A aresta A-C (custo 200) não deve estar na AGM."""
        graph = _make_simple_graph()
        mst, _ = run_kruskal(graph)
        pares = {(e.origem, e.destino) for e in mst}
        assert ("A", "C") not in pares and ("C", "A") not in pares, (
            "A aresta A-C deveria ser excluída da AGM."
        )

    def test_formula_peso_aplicada(self):
        """Verifica que a fórmula com obstáculos e andares é aplicada corretamente."""
        g = Graph()
        # Custo = (50 * 2.0) + (3 * 50) + (2 * 100) = 100 + 150 + 200 = 450
        edge = g.add_edge(
            "X", "Y",
            distancia=50.0,
            fator_terreno=2.0,
            obstaculos=3,
            andares=2,
        )
        assert edge.peso == pytest.approx(450.0)


# ---------------------------------------------------------------------------
# test_grafo_vazio
# ---------------------------------------------------------------------------

class TestGrafoVazio:
    """Comportamento com grafo sem vértices."""

    def test_retorna_lista_vazia(self):
        """Kruskal em grafo vazio deve retornar lista de arestas vazia."""
        g = Graph()
        mst, _ = run_kruskal(g)
        assert mst == []

    def test_retorna_custo_zero(self):
        """Kruskal em grafo vazio deve retornar custo 0."""
        g = Graph()
        _, total = run_kruskal(g)
        assert total == 0.0

    def test_conectividade_grafo_vazio(self):
        """Um grafo vazio deve ser considerado conexo (vacuamente verdadeiro)."""
        g = Graph()
        connected, isolated = g.check_connectivity()
        assert connected is True
        assert isolated == []

    def test_vertice_isolado_desconexo(self):
        """Um vértice isolado sem arestas deve tornar o grafo desconexo."""
        g = Graph()
        g.add_vertex("Isolado")
        g.add_edge("A", "B", distancia=10.0, fator_terreno=1.0, obstaculos=0, andares=0)
        connected, isolated = g.check_connectivity()
        assert connected is False
        assert "Isolado" in isolated


# ---------------------------------------------------------------------------
# test_grafo_completo
# ---------------------------------------------------------------------------

class TestGrafoCompleto:
    """Grafo completo K4 onde todos os nós se conectam entre si."""

    def test_agm_tem_v_menos_1_arestas(self):
        """K4 tem 4 vértices → AGM deve ter 3 arestas."""
        graph = _make_complete_graph()
        mst, _ = run_kruskal(graph)
        assert len(mst) == graph.num_vertices - 1

    def test_custo_total_otimo(self):
        """O custo da AGM de K4 deve ser 50 (V1-V2=10, V2-V3=15, V2-V4=25)."""
        graph = _make_complete_graph()
        _, total = run_kruskal(graph)
        assert total == pytest.approx(50.0), f"Custo esperado 50, obtido {total}"

    def test_sem_ciclo_na_agm(self):
        """Verifica que a AGM não contém ciclos (todas as arestas conectam componentes distintos)."""
        graph = _make_complete_graph()
        mst, _ = run_kruskal(graph)
        # Se houver N-1 arestas e o grafo for conexo, não há ciclo
        assert len(mst) == graph.num_vertices - 1

    def test_grafo_desconexo_levanta_erro(self):
        """Kruskal deve levantar ValueError se o grafo for desconexo."""
        g = Graph()
        # Componente 1: A-B
        g.add_edge("A", "B", distancia=10.0, fator_terreno=1.0, obstaculos=0, andares=0)
        # Componente 2: C-D (desconectado do primeiro)
        g.add_edge("C", "D", distancia=20.0, fator_terreno=1.0, obstaculos=0, andares=0)

        with pytest.raises(ValueError, match="desconexo"):
            run_kruskal(g)
