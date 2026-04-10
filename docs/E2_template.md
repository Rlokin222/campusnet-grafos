Markdown
# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 13 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | CampusNet - Otimizador de Infraestrutura de Rede |
| Repositório GitHub |https://github.com/Rlokin222/campusnet-grafos |
| Integrante 1 | Igor Nonaka — RA 37420518 |
| Integrante 2 | Marcus Gabriel — RA 39262901 |
| Integrante 3 | Ronald Lopes — RA 38899817 |

---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Algoritmo de Kruskal (com estrutura Union-Find) |
| Categoria | Algoritmo Guloso (Greedy) |
| Complexidade de tempo | $O(E \log E)$ ou $O(E \log V)$ |
| Complexidade de espaço | $O(V)$ |
| Problema que resolve | Encontrar a Árvore Geradora Mínima (AGM) em um grafo ponderado e não-dirigido, minimizando o custo total de cabeamento. |

**Por que este algoritmo foi escolhido?**

O problema consiste em conectar diversos prédios de um campus universitário sem gerar ciclos e garantindo o menor custo de instalação. Como não há necessidade de conectar todos os prédios a todos os outros de forma direta, a rede modelada resultará em um grafo esparso. O algoritmo de Kruskal é altamente otimizado para grafos esparsos, pois ele ordena as arestas pelo peso (custo) e as adiciona iterativamente, ignorando conexões que formariam ciclos, o que se alinha perfeitamente ao nosso objetivo de evitar desperdício de infraestrutura.

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| Algoritmo de Prim | Embora o algoritmo de Prim também encontre a AGM, ele tem melhor desempenho em grafos densos. Como a infraestrutura de um campus possui conexões limitadas, a ordenação de arestas do Kruskal torna a execução mais eficiente e direta para o nosso domínio. |

**Limitações no contexto do problema:**

A principal limitação é que o algoritmo de Kruskal pressupõe que o grafo de entrada seja conexo para gerar uma AGM que cubra todos os vértices. Se o usuário inserir dados onde um prédio não possui nenhuma rota física viável para o resto do campus, o algoritmo padrão não conseguirá interligar a rede inteira. Será necessária uma validação prévia de conectividade (via BFS ou DFS) antes de executar o Kruskal.

**Referência bibliográfica:**

> CORMEN, T. H. et al. Algoritmos: teoria e prática. 3. ed. Rio de Janeiro: Elsevier, 2012.

---

## 2. Arquitetura em Camadas

> Insira o diagrama abaixo. Pode ser exportado do Draw.io, Excalidraw, etc.

![Diagrama de arquitetura](./docs/DiagramaMD2Arquitetura.png) 
*(Lembre-se de gerar o desenho com as 4 caixinhas abaixo e salvar na pasta docs!)*

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/CLI) | Coletar dados do usuário e exibir o grafo visualmente. | `app.py` (Interface em Streamlit) |
| Aplicação (Service) | Orquestrar as requisições: validar se o grafo é conexo e invocar a função de cálculo de peso por aresta. | `network_service.py` |
| Domínio (Core) | Conter a lógica matemática, a estrutura da Lista de Adjacência e a execução do Kruskal (Union-Find). | `graph.py`, `edge.py`, `kruskal.py` |
| Infraestrutura (I/O) | Ler e formatar os arquivos de entrada (JSON) com os dados físicos do campus. | `file_reader.py` |

---

## 3. Estrutura de Diretórios

```text
campusnet-grafos/
├── docs/
│   ├── README.md
│   ├── E1_template.md
│   ├── E2_template.md
│   └── arquitetura_e2.png
├── src/
│   ├── core/
│   │   ├── graph.py          
│   │   ├── edge.py
│   │   └── disjoint_set.py   # Estrutura Union-Find para o Kruskal
│   ├── algorithms/
│   │   └── kruskal.py      
│   ├── io/
│   │   └── file_reader.py
│   └── app.py                # Interface visual Streamlit
├── data/
│   └── campus_mock.json      # Dataset de teste
└── requirements.txt          


Justificativa de desvios: A estrutura foi mantida próxima ao sugerido, com a adição do arquivo disjoint_set.py na camada Core para separar a lógica de conjuntos disjuntos exigida pelo Kruskal, e app.py na raiz do src/ para facilitar a inicialização da interface Streamlit.

4. Definição do Dataset
Formato de entrada aceito:
O sistema aceitará o formato JSON, por ser de fácil leitura e estruturação. O arquivo conterá uma lista de vértices (prédios) e uma lista de arestas (conexões). As arestas não receberão um peso pré-calculado no JSON; em vez disso, receberão os parâmetros reais (distância, obstáculos, terreno, andares) para que a Camada de Aplicação calcule o peso final em tempo de execução usando a fórmula de soma ponderada.
Exemplo de estrutura do arquivo de entrada:
JSON
{
  "vertices": ["Biblioteca", "Bloco A", "Secretaria"],
  "arestas": [
    { 
      "origem": "Biblioteca", 
      "destino": "Bloco A", 
      "distancia_m": 120,
      "obstaculos": 1,
      "terreno": "asfalto",
      "diferenca_andares": 0
    }
  ]
}


Estratégia de geração aleatória:
Parâmetro
Descrição
Número de vértices
Configurável via argumento (ex: 10 a 50 prédios).
Densidade
Configurável (0.1 a 0.3) para garantir que o grafo gerado seja esparso.
Faixa de pesos
Parâmetros de distância (10m a 500m) e obstáculos (0 a 3) gerados aleatoriamente.


5. Backlog do Projeto
5.1 In-Scope — O que será implementado
#
Funcionalidade
Prioridade
Critério de aceite
1
Leitura de Dataset
Alta
Dado um arquivo JSON válido com prédios e rotas, quando o usuário fizer o upload, então o sistema deve carregar o grafo em memória utilizando uma Lista de Adjacência.
2
Cálculo de Custo (Peso)
Alta
Dado um grafo carregado, quando a leitura for finalizada, então o sistema aplica a fórmula de soma ponderada convertendo distância, terreno e obstáculos em um único valor numérico (peso da aresta).
3
Validação de Conectividade
Alta
Dado um grafo gerado a partir do JSON, quando o cálculo iniciar, então o sistema verifica se todos os vértices são alcançáveis, exibindo um erro caso o grafo seja desconexo.
4
Execução do Kruskal
Alta
Dado um grafo conexo e ponderado, quando o algoritmo for acionado, então o sistema retorna a Árvore Geradora Mínima (AGM) e o custo total financeiro do cabeamento.
5
Visualização de Rede
Média
Dado o resultado da AGM, quando o processamento terminar, então a interface exibe um diagrama interativo mostrando os prédios e destacando apenas as arestas selecionadas pelo algoritmo.

5.2 Out-of-Scope — O que NÃO será feito
Funcionalidade excluída
Motivo
Planejamento de roteadores dentro das salas.
Foge do escopo de modelagem da infraestrutura externa principal do campus. Será tratado como trabalho futuro de expansão.
Monitoramento de tráfego de rede em tempo real.
O sistema foca no planejamento estático da instalação física dos cabos, e não na gestão dinâmica ou roteamento de pacotes que exigiria algoritmos como Dijkstra.
Cálculo de redundância ou rotas de backup.
A proposta é pautada na Árvore Geradora Mínima, cujo objetivo matemático é interligar todos os pontos com o menor custo absoluto. Adicionar redundância implicaria na criação proposital de ciclos, quebrando a definição de uma árvore.


Checklist de Entrega
[x] Big-O de tempo e espaço declarados para cada algoritmo
[x] Ao menos 1 alternativa descartada com justificativa
[x] Diagrama de arquitetura com 4 camadas identificadas
[x] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
[x] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
[x] Ao menos 3 critérios de aceite no formato "dado / quando / então"
[x] Exemplo de estrutura de arquivo de entrada presente
