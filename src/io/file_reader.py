# Lê o arquivo JSON com os dados do campus e valida se tem o formato certo.
import json
from pathlib import Path
from typing import Any


def load_json(source: str | Path) -> dict[str, Any]:
    """
    Lê um arquivo JSON do disco e devolve os dados.

    Espera um arquivo com as chaves 'vertices' e 'arestas'.
    Se não encontrar o arquivo ou as chaves, lança um erro.
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
    Mesma coisa que load_json, mas recebe o conteúdo em bytes.
    Isso é necessário porque o Streamlit entrega o arquivo assim
    quando o usuário faz o upload.
    """
    data: dict[str, Any] = json.loads(raw_bytes.decode("utf-8"))
    _validate_schema(data)
    return data


def _validate_schema(data: dict[str, Any]) -> None:
    """Verifica se o JSON tem as duas chaves que o programa precisa."""
    required_keys = {"vertices", "arestas"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(
            f"Arquivo JSON inválido. Chaves ausentes: {missing}. "
            f"Chaves esperadas: {required_keys}"
        )
