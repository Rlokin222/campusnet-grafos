"""
Módulo responsável pela leitura de arquivos de entrada do CampusNet.
"""
import json
from pathlib import Path
from typing import Any


def load_json(source: str | Path) -> dict[str, Any]:
    """
    Lê um arquivo JSON do sistema de arquivos e retorna os dados brutos.

    Args:
        source: Caminho (str ou Path) para o arquivo .json.

    Returns:
        Dicionário com as chaves 'vertices' e 'arestas'.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o JSON não contiver as chaves esperadas.
    """
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with path.open(encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    _validate_schema(data)
    return data


def load_json_from_bytes(raw_bytes: bytes) -> dict[str, Any]:
    """
    Lê um JSON a partir de bytes (útil para uploads via Streamlit).

    Args:
        raw_bytes: Conteúdo binário do arquivo .json.

    Returns:
        Dicionário com as chaves 'vertices' e 'arestas'.

    Raises:
        ValueError: Se o JSON não contiver as chaves esperadas.
    """
    data: dict[str, Any] = json.loads(raw_bytes.decode("utf-8"))
    _validate_schema(data)
    return data


def _validate_schema(data: dict[str, Any]) -> None:
    """Valida se as chaves obrigatórias estão presentes."""
    required_keys = {"vertices", "arestas"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(
            f"Arquivo JSON inválido. Chaves ausentes: {missing}. "
            f"Chaves esperadas: {required_keys}"
        )
