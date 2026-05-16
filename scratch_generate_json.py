import json
import math

nodes = {
    "Portaria": {"x": 960, "y": 1000},
    "Reitoria": {"x": 960, "y": 800},
    "Auditorio": {"x": 960, "y": 400},
    "Biblioteca": {"x": 600, "y": 600},
    "Bloco_Exatas": {"x": 300, "y": 300},
    "Bloco_Humanas": {"x": 700, "y": 200},
    "Refeitorio": {"x": 1300, "y": 600},
    "Laboratorios": {"x": 1200, "y": 300},
    "Ginasio": {"x": 1600, "y": 200},
    "Alojamento": {"x": 1700, "y": 800},
}

connections = [
    ("Portaria", "Reitoria", 1.0, 0, 0),
    ("Reitoria", "Biblioteca", 1.2, 0, 1),
    ("Reitoria", "Refeitorio", 1.0, 0, 0),
    ("Reitoria", "Auditorio", 1.0, 0, 0),
    ("Biblioteca", "Bloco_Exatas", 1.5, 1, 0),
    ("Biblioteca", "Auditorio", 1.0, 0, 0),
    ("Bloco_Exatas", "Bloco_Humanas", 1.0, 0, 0),
    ("Auditorio", "Bloco_Humanas", 1.0, 0, 0),
    ("Auditorio", "Laboratorios", 1.0, 0, 0),
    ("Refeitorio", "Laboratorios", 1.2, 0, 0),
    ("Refeitorio", "Ginasio", 1.0, 0, 0),
    ("Refeitorio", "Alojamento", 1.0, 0, 0),
    ("Laboratorios", "Ginasio", 1.5, 1, 0),
    ("Ginasio", "Alojamento", 1.0, 0, 0),
    ("Portaria", "Alojamento", 1.0, 0, 0),
]

arestas = []
for u, v, ft, obs, andares in connections:
    dx = nodes[u]["x"] - nodes[v]["x"]
    dy = nodes[u]["y"] - nodes[v]["y"]
    dist = math.sqrt(dx**2 + dy**2) / 2.5 # Scale to meters
    arestas.append({
        "origem": u,
        "destino": v,
        "distancia": round(dist, 1),
        "fator_terreno": ft,
        "obstaculos": obs,
        "andares": andares
    })

data = {
    "vertices": nodes,
    "arestas": arestas
}

with open("data/campus_realista.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
