# Aqui a gente chama tudo em ordem: lê o arquivo, monta o grafo,
# verifica se é conexo e roda o Kruskal. O resultado vai para a interface.
import time
from dataclasses import dataclass, field

from src.algorithms.kruskal import run_kruskal
from src.core.edge import Edge
from src.core.graph import Graph
from src.io.file_reader import load_json_from_bytes


@dataclass
class ProcessingResult:
    """
    Agrupa tudo que a interface precisa mostrar depois do processamento:
    o grafo, as arestas da AGM, o custo total e os tempos de execução.
    """

    graph: Graph
    is_connected: bool
    isolated_nodes: list[str]
    mst_edges: list[Edge] = field(default_factory=list)
    total_cost: float = 0.0
    build_time_ms: float = 0.0
    kruskal_time_ms: float = 0.0

    @property
    def total_time_ms(self) -> float:
        """Tempo total = leitura + Kruskal."""
        return self.build_time_ms + self.kruskal_time_ms


def process_campus_network(
    raw_bytes: bytes,
    custo_cabo_m: float | None = None,
    custo_obstaculo: float | None = None,
    custo_andar: float | None = None,
) -> ProcessingResult:
    """
    Função principal que a interface chama quando o usuário faz o upload.

    Passos:
        1. Lê o JSON e monta o grafo
        2. Verifica se o grafo é conexo (BFS)
        3. Se conexo, roda o Kruskal e calcula a AGM
        4. Devolve tudo organizado no ProcessingResult
    """
    # Etapa 1: lê o arquivo e constrói o grafo (medindo o tempo)
    t0 = time.perf_counter()
    data = load_json_from_bytes(raw_bytes)
    
    # Injeta os custos recebidos da UI no dicionário antes de construir o grafo
    if "parametros_custo" not in data:
        data["parametros_custo"] = {}
    if custo_cabo_m is not None: data["parametros_custo"]["cabo_m"] = custo_cabo_m
    if custo_obstaculo is not None: data["parametros_custo"]["obstaculo"] = custo_obstaculo
    if custo_andar is not None: data["parametros_custo"]["andar"] = custo_andar
        
    graph = Graph.from_dict(data)
    
    build_time_ms = (time.perf_counter() - t0) * 1000

    # Etapa 2: verifica se todos os prédios estão conectados
    is_connected, isolated = graph.check_connectivity()

    # Etapa 3: só roda o Kruskal se o grafo for conexo
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
