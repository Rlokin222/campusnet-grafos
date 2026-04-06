# E1 — Proposta e Definição do Projeto

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 18 de março de 2026  
> **Peso:** 10% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | |
| Integrante 1 | Nome —Igor Nonaka RA 37420518|
| Integrante 2 | Nome —Marcus Gabriel RA 39262901 |
| Integrante 3 | Nome —Ronald Lopes RA 38899817|
| Domínio de aplicação | ex.: logística, redes, jogos... |

---

## 1. Contexto e Motivação

> Descreva o problema do mundo real que será abordado. Por que ele é relevante?  
> *Orientação: 2 a 3 parágrafos. Seja específico — evite generalizações.*

 O projeto proposto trata do planejamento da instalação de uma rede de internet em um campus universitário. Em um campus, existem vários pontos que precisam de conexão, como blocos, biblioteca, laboratórios, secretaria, salas de aula e outros ambientes. Fazer esse planejamento manualmente pode gerar gastos desnecessários, principalmente quando há muitas possibilidades de ligação entre os pontos. Além disso, a menor distância entre dois locais nem sempre representa a melhor solução, já que fatores físicos e estruturais também influenciam no custo final da instalação.
No cenário proposto, o usuário poderá cadastrar diferentes pontos do campus onde deseja disponibilizar internet e informar quais conexões podem existir entre eles. Para cada conexão, será possível inserir dados como distância em metros, presença de obstáculos no caminho, tipo de terreno, diferença de andares entre os locais e outras dificuldades de instalação. Assim, o sistema poderá analisar não apenas se dois pontos podem ser conectados, mas também qual é o custo aproximado dessa ligação.
Esse problema é relevante porque representa uma aplicação real de otimização em redes, área que tem forte relação com a Teoria dos Grafos. Em vez de conectar os pontos de forma arbitrária, o sistema buscará uma solução que ligue todos os locais necessários com o menor custo total possível. Além disso, o projeto possui valor educacional, pois permite visualizar de maneira concreta como conceitos teóricos de grafos podem ser aplicados em um problema prático de infraestrutura. A proposta também pode ser expandida para um nível mais detalhado, incluindo o planejamento de roteadores dentro de salas e ambientes internos dos prédios.


---

## 2. Objetivo Geral

> O que o sistema deve ser capaz de fazer ao final?  
> *Orientação: 1 frase clara e objetiva. Ex.: "O sistema deve calcular a rota de menor custo entre dois pontos em um mapa urbano."*

 O sistema deve planejar a rede de internet de um campus universitário, conectando todos os pontos necessários com o menor custo total possível por meio da modelagem em grafos.
 

---

## 3. Objetivos Específicos

> Desmembre o objetivo geral em metas mensuráveis.  
> *Orientação: liste entre 3 e 5 itens. Cada item deve ser verificável — use verbos como "implementar", "calcular", "exibir", "carregar".*

- [Implementar o cadastro de pontos do campus, como blocos, setores e salas.] 
- [Implementar o cadastro das conexões possíveis entre os pontos, com seus respectivos custos.] 
- [ Calcular a melhor rede de conexão usando um algoritmo de árvore geradora mínima. ] 
- [ Exibir visualmente o grafo original e a solução otimizada encontrada. ] 
- [ Mostrar o custo total da rede planejada a partir das conexões escolhidas. ]

---

## 4. Público-Alvo / Caso de Uso Principal

> Para quem ou em qual cenário o sistema seria utilizado?  
> *Orientação: descreva um cenário concreto de uso. Ex.: "Um entregador de aplicativo que precisa otimizar a sequência de entregas em um bairro."*

O sistema é voltado para uso acadêmico e educacional, sendo pensado principalmente para estudantes e professores que desejam visualizar uma aplicação prática da Teoria dos Grafos. O caso de uso principal é a simulação do planejamento de rede de internet em um campus universitário, em que o usuário informa os pontos que precisam de conexão e as possíveis ligações entre eles, e o sistema retorna a forma mais econômica de interligar toda a estrutura.

---

## 5. Justificativa Técnica — Por que Grafos?

> Por que a modelagem em grafo é a abordagem mais adequada para este problema?  
> *Orientação: explique quais elementos do problema mapeiam naturalmente para vértices e arestas. Mencione se há pesos, direção, ou restrições que reforçam a escolha.*

 A modelagem em grafos é adequada porque o problema pode ser representado naturalmente como uma rede de pontos conectáveis. Cada bloco, prédio, laboratório, secretaria ou sala pode ser tratado como um vértice, enquanto cada ligação possível entre dois locais pode ser representada como uma aresta. Como cada conexão possui um custo associado, o grafo será ponderado, permitindo que o sistema leve em conta não apenas a existência de ligação entre os pontos, mas também o custo real aproximado de cada instalação.
Além disso, o problema exige encontrar uma forma de conectar todos os pontos necessários sem desperdício de conexões e com menor custo total, o que se encaixa diretamente no conceito de árvore geradora mínima. Nesse contexto, algoritmos clássicos da Teoria dos Grafos, como Kruskal, tornam-se apropriados para resolver o problema de maneira eficiente. Dessa forma, os grafos não serão usados apenas como representação visual, mas como a base da solução computacional do sistema.


---

## 6. Tipo de Grafo

> Especifique as características do grafo que o problema requer.

| Característica                   | Escolha             | Justificativa breve                                                                                       |
| -------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------- |
| Dirigido ou não-dirigido         | Não-dirigido        | A ligação entre dois pontos do campus vale nos dois sentidos.                                             |
| Ponderado ou não-ponderado       | Ponderado           | Cada conexão terá um peso baseado em distância, obstáculos, terreno, andares e dificuldade de instalação. |
| Conectado / bipartido / geral    | Conectado           | A proposta exige que todos os pontos da rede possam ser ligados.                                          |
| Representação interna pretendida | Lista de adjacência | É mais adequada para grafos esparsos e facilita o armazenamento das conexões com pesos.|
---

## 7. Diagrama Conceitual

> Insira aqui ao menos uma figura que ilustre o domínio do problema.  
> *Pode ser uma imagem exportada do Draw.io, Excalidraw, foto de esboço à mão etc.*  

<!-- imagem aqui -->

**Legenda:** 

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
