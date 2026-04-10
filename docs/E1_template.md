# E1 — Proposta e Definição do Projeto (REVISADO)

> Disciplina: Teoria dos Grafos  
> Prazo original: 18 de março de 2026  
> Status: Corrigido com base no feedback da avaliação E1

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | CampusNet — Otimizador de Infraestrutura de Rede |
| Integrante 1 | Igor Nonaka (RA 37420518) |
| Integrante 2 | Marcus Gabriel (RA 39262901) |
| Integrante 3 | Ronald Lopes (RA 38899817) |
| Domínio de aplicação | Redes e Infraestrutura Física |

---

## 1. Contexto e Motivação

O projeto proposto trata do planejamento da instalação de uma rede de internet em um campus universitário. Em um campus, existem vários pontos que precisam de conexão, como blocos, bibliotecas, laboratórios e secretarias. Fazer esse planejamento manualmente pode gerar gastos desnecessários com cabeamento, especialmente quando há múltiplas rotas possíveis entre os locais. Além disso, a menor distância nem sempre é a melhor solução, pois fatores físicos e estruturais influenciam diretamente no custo final.

No cenário proposto, o usuário cadastra os pontos e as conexões possíveis, informando dados como distância, presença de obstáculos, tipo de terreno e diferença de andares. O sistema analisa esses múltiplos fatores para definir o custo real de cada ligação. Este problema é relevante porque impacta diretamente na redução de custos operacionais e no desperdício de materiais em obras de infraestrutura, permitindo uma expansão de rede mais eficiente e econômica.

Escopo e Limitações: O foco desta etapa é a interligação externa entre os prédios e setores do campus. O planejamento detalhado de roteadores dentro das salas e ambientes internos é considerado um trabalho futuro e não faz parte da entrega atual.

## 2. Objetivo Geral

O sistema deve planejar a rede de internet de um campus universitário, conectando todos os pontos necessários com o menor custo total possível por meio da modelagem em grafos e algoritmos de otimização.

## 3. Objetivos Específicos

* Implementar o cadastro de pontos (vértices) e das conexões possíveis (arestas) com seus respectivos parâmetros físicos.
* Calcular o peso de cada aresta através de uma fórmula de soma ponderada que considere distância, obstáculos e terreno.
* Validar se o grafo de entrada é conexo, alertando o usuário caso existam pontos que não podem ser alcançados pela rede.
* Calcular a melhor rede de conexão usando o algoritmo de Kruskal para Árvore Geradora Mínima.
* Exibir visualmente o grafo original e a solução otimizada, informando o custo total do projeto.

## 4. Público-Alvo / Caso de Uso Principal

O sistema é voltado para gestores de TI e estudantes que desejam simular o planejamento econômico de uma rede de campus. O usuário informa os pontos que precisam de conexão e as dificuldades físicas entre eles, e o sistema retorna a árvore de conexões que garante a conectividade total com o menor investimento financeiro.

## 5. Justificativa Técnica: Por que Grafos?

A modelagem em grafos é a abordagem ideal porque o problema é, por natureza, uma rede de pontos interligados. Cada prédio ou sala é mapeado como um vértice, enquanto cada caminho viável para os cabos é uma aresta. O grafo será ponderado, onde o peso da aresta não é apenas a distância, mas uma representação do custo real calculada por uma função que pondera obstáculos e tipos de solo.

Como o objetivo é conectar todos os pontos sem ciclos (redundâncias) e com o menor custo, o problema mapeia-se diretamente para o conceito de Árvore Geradora Mínima (AGM). O uso do algoritmo de Kruskal é justificado pela eficiência em lidar com grafos esparsos, típicos de infraestruturas físicas de campus.

## 6. Tipo de Grafo

| Característica | Escolha | Justificativa |
| :--- | :--- | :--- |
| Direção | Não-dirigido | A conexão física via cabo permite tráfego nos dois sentidos. |
| Peso | Ponderado | Cada conexão possui custos distintos baseados em distância e dificuldades físicas. |
| Conectividade | Geral (Entrada) | O grafo inserido pelo usuário pode ser inicialmente desconexo; o sistema deve validar isso antes de gerar a AGM conectada. |
| Representação | Lista de Adjacência | Mais eficiente para grafos esparsos (onde nem todos os prédios se conectam diretamente a todos os outros). |

## 7. Diagrama Conceitual

O diagrama ilustra o campus universitário como um grafo, onde os prédios são vértices e as rotas de cabos são arestas com pesos numéricos baseados na fórmula de custo.

![Diagrama Conceitual do Campus](./docs/diagramaConceitual1.png)
Legenda: Exemplo de representação do campus como um grafo ponderado.

---

## Checklist de Entrega

Antes de submeter, confirme:

- [x] Texto entre 300 e 600 palavras (seções 1 a 5)
- [x] Todos os campos da tabela de identificação preenchidos
- [x] Tipo de grafo especificado com justificativa
- [x] Diagrama presente e referenciado no texto
- [x] Arquivo nomeado como `E1_NomeGrupo_Grafos.docx` (versão Word) ou PR aberto (versão GitHub)

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*


