"""
Camada de Serviço (Application Layer) — CampusNet.

Responsabilidade: orquestrar as operações entre a UI e o Domínio.
  1. Recebe os bytes brutos do arquivo JSON (vindos do upload)
  2. Delega a leitura para a camada de I/O
  3. Constrói o grafo via camada de Domínio
  4. Valida a conectividade
  5. Executa o Kruskal se o grafo for conexo
  6. Devolve um objeto de resultado estruturado para a UI
"""
import time
from dataclasses import dataclass, field

from src.algorithms.kruskal import run_kruskal
from src.core.edge import Edge
from src.core.graph import Graph
from src.io.file_reader import load_json_from_bytes


@dataclass
class ProcessingResult:
    """DTO com todos os dados necessários para a camada de Apresentação."""

    graph: Graph
    is_connected: bool
    isolated_nodes: list[str]
    mst_edges: list[Edge] = field(default_factory=list)
    total_cost: float = 0.0
    build_time_ms: float = 0.0
    kruskal_time_ms: float = 0.0

    @property
    def total_time_ms(self) -> float:
        return self.build_time_ms + self.kruskal_time_ms


def process_campus_network(raw_bytes: bytes) -> ProcessingResult:
    """
    Ponto de entrada único da camada de serviço.

    Args:
        raw_bytes: Conteúdo binário do arquivo JSON enviado pelo usuário.

    Returns:
        ProcessingResult com o grafo, o resultado da AGM e métricas de tempo.

    Raises:
        ValueError: Se o JSON for inválido ou o schema estiver incorreto.
    """
    # — Etapa 1: Leitura e construção do grafo —
    t0 = time.perf_counter()
    data = load_json_from_bytes(raw_bytes)
    graph = Graph.from_dict(data)
    build_time_ms = (time.perf_counter() - t0) * 1000

    # — Etapa 2: Validação de conectividade —
    is_connected, isolated = graph.check_connectivity()

    # — Etapa 3: Execução do Kruskal (apenas se conexo) —
    mst_edges: list[Edge] = []
    total_cost = 0.0
    kruskal_time_ms = 0.0

    if is_connected:
        t1 = time.perf_counter()
        mst_edges, total_cost = run_kruskal(graph)
        kruskal_time_ms = (time.perf_counter() - t1) * 1000

    return ProcessingResult(
        graph=graph,
        is_connected=is_connected,
        isolated_nodes=isolated,
        mst_edges=mst_edges,
        total_cost=total_cost,
        build_time_ms=build_time_ms,
        kruskal_time_ms=kruskal_time_ms,
    )
