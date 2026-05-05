# 🌐 CampusNet — Otimizador de Infraestrutura de Rede

> **Disciplina:** Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai  
> **Equipe:** Igor Nonaka · Marcus Gabriel · Ronald Lopes

Sistema que calcula a **Árvore Geradora Mínima (AGM)** para o planejamento de cabeamento de rede de um campus universitário, usando o **Algoritmo de Kruskal** com estrutura Union-Find otimizada.

---

## 📐 Fórmula de Custo

O peso de cada aresta não é informado diretamente — ele é calculado internamente pela regra de negócio:

```
Custo = (distância × fator_terreno) + (obstáculos × 50) + (diferença_andares × 100)
```

| Parâmetro | Descrição |
|---|---|
| `distancia` | Distância física entre os pontos (metros) |
| `fator_terreno` | Multiplicador de dificuldade do terreno (ex: 1.0 = plano, 1.5 = difícil) |
| `obstaculos` | Número de obstáculos físicos (paredes, dutos, etc.) |
| `andares` | Diferença de andares entre os pontos |

---

## 🗂️ Estrutura do Projeto

```
campusnet-grafos/
├── src/
│   ├── core/
│   │   ├── graph.py          # Grafo (Lista de Adjacência) + fórmula de custo
│   │   ├── edge.py           # Dataclass Edge (imutável, ordenável por peso)
│   │   └── disjoint_set.py   # Union-Find com path compression + union by rank
│   ├── algorithms/
│   │   └── kruskal.py        # Algoritmo de Kruskal — O(E log E)
│   ├── io/
│   │   └── file_reader.py    # Leitura de JSON (arquivo ou bytes/upload)
│   ├── visualization/
│   │   └── graph_plotter.py  # Visualização do grafo com networkx + matplotlib
│   ├── network_service.py    # Camada de Serviço — orquestra todas as etapas
│   └── app.py                # Interface Streamlit
├── tests/
│   └── test_kruskal.py       # 12 testes pytest (caso base, vazio, completo, desconexo)
├── data/
│   └── campus_mock.json      # Dataset de exemplo (10 nós, 15 arestas)
├── docs/
│   ├── assets/               # Screenshots da interface (mvp_entrada.png, mvp_resultado.png)
│   ├── E1_template.md
│   ├── E2_template.md
│   └── E3_template.md
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Pré-requisitos

- **Python 3.10+**  
- pip

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/Rlokin222/campusnet-grafos.git
cd campusnet-grafos
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a interface web

```bash
streamlit run src/app.py
```

O navegador abrirá automaticamente em **http://localhost:8501**.

---

## 🖥️ Como usar

1. Na barra lateral, clique em **"📂 Carregar topologia (JSON)"**
2. Faça o upload do arquivo `data/campus_mock.json` (ou do seu próprio arquivo)
3. O sistema irá:
   - Validar a conectividade do grafo via BFS
   - Executar o Kruskal e calcular a AGM
   - Exibir o grafo visual com as arestas da AGM destacadas
   - Mostrar a tabela de cabos selecionados e o custo total

---

## 📄 Formato do Arquivo JSON de Entrada

```json
{
  "vertices": ["Bloco_A", "Biblioteca", "Laboratorio"],
  "arestas": [
    {
      "origem": "Bloco_A",
      "destino": "Biblioteca",
      "distancia": 120.0,
      "fator_terreno": 1.0,
      "obstaculos": 0,
      "andares": 1
    }
  ]
}
```

---

## 🧪 Testes

```bash
pytest tests/ -v
```

**Resultado esperado:** 12 testes passando (caso base, grafo vazio, grafo completo K4, grafo desconexo).

---

## 📊 Complexidade do Algoritmo

| Etapa | Complexidade |
|---|---|
| Ordenação das arestas | O(E log E) |
| Iteração com Union-Find | O(E · α(V)) |
| **Total** | **O(E log E)** |
| Espaço (Union-Find) | O(V) |

onde α é a função inversa de Ackermann — praticamente constante para qualquer entrada real.
