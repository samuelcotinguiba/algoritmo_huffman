# Algoritmo de Huffman - Compressão de Dados

## 📋 Sumário
1. [Introdução](#introdução)
2. [Requisitos](#requisitos)
3. [Instalação](#instalação)
4. [Como Usar](#como-usar)
5. [Arquitetura do Projeto](#arquitetura-do-projeto)
6. [Documentação das Funções](#documentação-das-funções)
7. [O Algoritmo de Huffman](#o-algoritmo-de-huffman)
8. [Análise de Complexidade](#análise-de-complexidade)
9. [Exemplos](#exemplos)

---

## 🎯 Introdução

### Contexto Histórico

Este projeto implementa o **Algoritmo de Huffman**, uma técnica fundamental de compressão de dados sem perdas desenvolvida por David A. Huffman em 1952, durante seu doutorado no MIT. O algoritmo foi publicado no artigo seminal "A Method for the Construction of Minimum-Redundancy Codes" na revista *Proceedings of the IRE*.

### Fundamentação Teórica

O algoritmo de Huffman resolve o problema da **codificação ótima de símbolos** através da construção de uma árvore binária que minimiza o comprimento médio esperado do código. Baseia-se em dois princípios fundamentais da Teoria da Informação:

1. **Princípio da Entropia de Shannon**: A quantidade mínima de informação necessária para representar um símbolo é proporcional ao logaritmo negativo de sua probabilidade.

2. **Codificação de Prefixo Livre**: Nenhum código válido é prefixo de outro código, garantindo decodificação unívoca sem necessidade de delimitadores.

### Características Matemáticas

O algoritmo de Huffman garante:
- **Optimalidade**: Produz o código de prefixo com menor comprimento médio possível para um dado conjunto de frequências
- **Greedy**: Utiliza estratégia gulosa (sempre escolhe os dois menores elementos)
- **Complexidade Temporal**: O(n log n), onde n é o número de símbolos únicos
- **Invariante**: A propriedade de prefixo livre é mantida em toda a construção

### Aplicações Práticas

- **Compressão de Arquivos**: ZIP, GZIP, BZIP2
- **Codificação de Imagens**: JPEG (após transformada DCT)
- **Codificação de Áudio**: MP3 (em conjunto com outros algoritmos)
- **Protocolos de Rede**: HTTP/2 (HPACK usa Huffman para compressão de headers)
- **Banco de Dados**: Compressão de índices e colunas
- **Telecomunicações**: Codificação de sinais para transmissão eficiente

### Limitações e Considerações

- **Overhead da Árvore**: É necessário transmitir/armazenar a árvore de Huffman junto com os dados
- **Dados Uniformes**: Pouca compressão quando todos os símbolos têm frequência similar
- **Huffman Adaptativo**: Para streams, existem variantes que atualizam a árvore dinamicamente
- **Alternativas Modernas**: Algoritmos como LZ77, LZ78 e suas variantes (LZSS, LZW) combinam Huffman com dicionários

---

## 📦 Requisitos

### Bibliotecas Python - Análise Detalhada

#### 1. **heapq** (biblioteca padrão - CPython)

```python
import heapq
```

**Fundamentação Teórica**:
O módulo `heapq` implementa uma estrutura de dados chamada **heap binária mínima** (min-heap), que é essencial para a eficiência do algoritmo de Huffman.

**Estrutura de Dados**:
- **Heap**: Árvore binária completa onde cada nó pai tem valor menor ou igual aos filhos
- **Representação**: Lista Python onde `heap[k] <= heap[2*k+1]` e `heap[k] <= heap[2*k+2]`
- **Propriedade Fundamental**: O menor elemento está sempre na raiz (`heap[0]`)

**Operações e Complexidades**:

A heap binária oferece operações eficientes fundamentais para o algoritmo de Huffman. A inserção através de `heappush(heap, item)` possui complexidade O(log n) devido ao processo de "bubbling up" na altura da árvore. A remoção do elemento mínimo via `heappop(heap)` também é O(log n), executando "bubbling down" após remover a raiz. O acesso ao mínimo é extremamente eficiente em O(1), pois o menor elemento sempre está em `heap[0]`. A operação `heapify(list)` constrói uma heap em O(n) usando o algoritmo de Floyd, mais eficiente que inserções sucessivas.

**Por que não usar outras estruturas?**:

1. **Lista Ordenada**:
   - Inserção: O(n) - precisa encontrar posição e deslocar elementos
   - Busca do mínimo: O(1)
   - **Desvantagem**: O(n) para inserção torna algoritmo O(n²)

2. **Lista Não Ordenada**:
   - Inserção: O(1)
   - Busca do mínimo: O(n) - precisa varrer toda lista
   - **Desvantagem**: Buscar mínimo m vezes = O(mn)

3. **Binary Search Tree (BST)**:
   - Operações: O(log n) no caso médio, O(n) no pior caso
   - **Desvantagem**: Necessita balanceamento (AVL, Red-Black)

4. **Fibonacci Heap**:
   - Inserção amortizada: O(1)
   - Remoção do mínimo: O(log n) amortizado
   - **Desvantagem**: Overhead de implementação, constantes maiores na prática

**Implementação no Huffman**:
```python
heap = []
for char, freq in frequencies.items():
    heappush(heap, (freq, Node(char, freq)))

while len(heap) > 1:
    freq1, node1 = heappop(heap)  # O(log n)
    freq2, node2 = heappop(heap)  # O(log n)
    merged = Node(None, freq1 + freq2)
    heappush(heap, (merged.freq, merged))  # O(log n)
```

**Complexidade Total**: O(n log n) para n símbolos únicos

---

#### 2. **json** (biblioteca padrão - RFC 8259)

```python
import json
```

**Especificação**:
JSON (JavaScript Object Notation) é um formato de intercâmbio de dados baseado em texto, definido pela RFC 8259 (2017).

**Características Técnicas**:
- **Formato**: Texto Unicode (UTF-8, UTF-16, UTF-32)
- **Estruturas**: Objetos `{}`, arrays `[]`, strings `""`, números, booleanos, null
- **Grammar**: Sintaxe livre de contexto (Context-Free Grammar)
- **MIME Type**: `application/json`

**Serialização da Árvore**:

Nossa implementação converte a árvore binária em uma estrutura JSON recursiva:

```json
{
  "char": null,
  "freq": 11,
  "left": {
    "char": "a",
    "freq": 5,
    "left": null,
    "right": null
  },
  "right": {
    "char": null,
    "freq": 6,
    "left": {...},
    "right": {...}
  }
}
```

**Comparação com Alternativas**:

JSON foi escolhido considerando diversas alternativas disponíveis. O formato **Pickle**, embora mais compacto e rápido, apresenta problemas críticos de segurança (pode executar código arbitrário) e é limitado ao Python. **XML** oferece legibilidade e portabilidade similares ao JSON, porém gera arquivos significativamente maiores e possui parsing mais lento. **MessagePack** e **Protocol Buffers** são superiores em velocidade e tamanho, mas sacrificam a legibilidade humana, crucial para fins educacionais.

**Por que JSON foi escolhido?**:

1. **Inspeção Manual**: Desenvolvedores podem abrir `arvore_huffman.json` e entender a estrutura
2. **Debug**: Fácil identificar problemas na árvore gerada
3. **Educacional**: Estudantes podem ver exatamente como a árvore é armazenada
4. **Portabilidade**: Pode ser lida por outras linguagens (JavaScript, Python, Java, etc.)
5. **Simplicidade**: Não requer esquema ou definição prévia

**Métodos Utilizados**:

```python
# Serialização (Python → JSON)
json.dump(
    data, 
    file, 
    ensure_ascii=False,  # Permite caracteres Unicode (é, ã, 中)
    indent=2             # Formatação legível (não compacta)
)

# Desserialização (JSON → Python)
data = json.load(file)
```

**Encoding**: `ensure_ascii=False` permite:
- Caracteres acentuados: `{"char": "é"}`
- Emojis: `{"char": "😀"}`
- Idiomas não-latinos: `{"char": "日"}`

Sem esse parâmetro, seria escapado: `{"char": "\u00e9"}`

---

#### 3. **matplotlib** (externa - versão 3.x)

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
```

**Fundamentos da Biblioteca**:

Matplotlib é uma biblioteca de visualização 2D/3D baseada na sintaxe do MATLAB, desenvolvida por John D. Hunter em 2003.

**Arquitetura em Camadas**:

1. **Backend Layer**: Interface com sistemas de janelas (Tk, Qt, GTK, macOS)
2. **Artist Layer**: Objetos primitivos (Line2D, Rectangle, Text)
3. **Scripting Layer**: Interface `pyplot` (API simplificada)

**Módulos Utilizados**:

##### 3.1. `matplotlib.pyplot`

```python
import matplotlib.pyplot as plt
```

**Funções Essenciais**:

O módulo pyplot fornece as ferramentas necessárias para visualização. Iniciamos com `plt.subplots(figsize=(16, 10))` que cria a figura e eixos de 16x10 polegadas. As arestas da árvore são desenhadas com `ax.plot(x, y)`, enquanto `ax.text(x, y, s)` adiciona os labels dos nós e códigos binários 0/1. Os limites dos eixos são ajustados via `ax.set_xlim()` e `ax.set_ylim()` para controlar o zoom. A proporção `ax.set_aspect('equal')` garante que os círculos não fiquem distorcidos. `ax.axis('off')` remove os eixos para interface limpa, `plt.title()` adiciona o título, `plt.tight_layout()` evita cortes nos elementos, e finalmente `plt.show()` exibe a visualização interativa.

##### 3.2. `matplotlib.patches`

```python
import matplotlib.patches as patches
```

**Patch**: Objeto geométrico 2D que pode ser adicionado a um Axes.

**Classes Utilizadas**:

```python
# Círculo para nós da árvore
circle = patches.Circle(
    (x, y),              # Centro (coordenadas)
    radius=0.5,          # Raio em unidades de dados
    facecolor='lightgreen',  # Cor de preenchimento
    edgecolor='black',   # Cor da borda
    linewidth=2.5,       # Espessura da borda
    zorder=2             # Ordem de desenho (maior = frente)
)
ax.add_patch(circle)
```

**Sistema de Coordenadas**:

- **Data Coordinates**: Sistema de coordenadas dos dados (nossos nós)
- **Axes Coordinates**: Relativo aos eixos (0,0) = canto inferior esquerdo
- **Figure Coordinates**: Relativo à figura inteira
- **Display Coordinates**: Pixels da tela

Usamos **Data Coordinates** para posicionar tudo.

**Z-ordering** (profundidade):

```python
zorder=1  # Arestas (linhas) - atrás
zorder=2  # Círculos dos nós - meio
zorder=3  # Texto (caracteres) - frente
```

**Algoritmo de Posicionamento**:

```python
def posicionar_inorder(node, depth=0):
    """
    In-order traversal garante folhas igualmente espaçadas
    
    Ordem: Esquerda → Raiz → Direita
    
    Folhas recebem posições sequenciais (0, 2, 4, 6, ...)
    Nós internos são posicionados no meio dos filhos
    """
    if node.left is None and node.right is None:
        positions[node] = (counter[0], -depth * 2)
        counter[0] += 2  # Espaçamento horizontal
    else:
        # Posição X = média dos filhos
        x = (positions[node.left][0] + positions[node.right][0]) / 2
        positions[node] = (x, -depth * 2)
```

**Esquema de Cores**:

O projeto utiliza um sistema de cores intuitivo para facilitar a interpretação visual da árvore. As folhas (caracteres finais) são representadas em verde claro (`lightgreen`), enquanto nós internos aparecem em cinza claro (`lightgray`). As arestas seguem uma convenção binária: azul (`blue`/`lightblue`) para caminhos à esquerda (bit 0) e vermelho (`red`/`lightcoral`) para caminhos à direita (bit 1), tornando óbvia a construção dos códigos binários.

**Configurações de Renderização**:

```python
fig, ax = plt.subplots(figsize=(16, 10))  # 16x10 polegadas
# DPI padrão = 100 → 1600x1000 pixels

# Proporção de aspecto igual
ax.set_aspect('equal')  # Círculos não ficam ovais

# Sem eixos
ax.axis('off')  # Remove grid, ticks, labels

# Título
plt.title(
    'Árvore de Huffman\n(0 = esquerda, 1 = direita)',
    fontsize=16,
    fontweight='bold',
    pad=20  # Espaçamento acima do gráfico
)
```

**Backend Detection**:

O código tenta usar o matplotlib sem especificar backend, permitindo que ele escolha automaticamente:

```python
try:
    import matplotlib
    # Sem matplotlib.use() - detecção automática
    import matplotlib.pyplot as plt
except:
    # Fallback para salvar arquivo
    pass
```

**Backends Disponíveis**:
- **TkAgg**: Tkinter (padrão em muitas instalações)
- **Qt5Agg**: PyQt5/PySide2
- **MacOSX**: Nativo do macOS
- **GTK3Agg**: Linux com GTK
- **Agg**: Apenas arquivo (sem GUI)

---

#### 4. **os** (biblioteca padrão - POSIX/Windows)

```python
import os
```

**Abstração de Sistema Operacional**:

O módulo `os` fornece interface portável para funcionalidades do SO.

**Funções Utilizadas**:

```python
# Verifica existência de arquivo
os.path.exists('arvore_huffman.json')  # bool

# Obtém diretório do script
os.path.dirname(os.path.abspath(__file__))  # string

# Junta caminhos de forma portável
os.path.join(dir, 'funcoes', 'node.py')
```

**Portabilidade Windows/Unix**:

```python
# Windows
os.path.join('funcoes', 'node.py')  # → 'funcoes\\node.py'

# Unix/macOS
os.path.join('funcoes', 'node.py')  # → 'funcoes/node.py'
```

**Por que não usar strings diretas?**:

```python
# ❌ Não portável
path = 'funcoes/node.py'  # Falha no Windows

# ✅ Portável
path = os.path.join('funcoes', 'node.py')
```

---

#### 5. **sys** (biblioteca padrão)

```python
import sys
```

**Uso**: Manipulação do `sys.path` para importação dinâmica de módulos.

```python
sys.path.insert(0, script_dir)
```

Adiciona diretório ao início do caminho de busca de módulos.

---

#### 6. **runpy** (biblioteca padrão)

```python
import runpy
```

**Propósito**: Executar módulos Python como scripts, obtendo seu namespace.

```python
_m = runpy.run_path('funcoes/node.py')
Node = _m['Node']  # Extrai classe Node
```

**Por que usamos isso?**:

Problema: Nome da pasta tem espaço (`"algoritmo de huffman "`)
- `import funcoes.node` falharia

Solução: `runpy.run_path()` carrega módulo por caminho absoluto
- Funciona independente do nome da pasta

---

## 🚀 Instalação

```bash
# Clone ou baixe o projeto
cd "algoritmo de huffman "

# Instale as dependências
pip3 install -r requirements.txt

# Execute o programa
python3 algoritmo_huffman.py
```

---

## 💻 Como Usar

### Modo 1: Codificar Texto
```bash
$ python3 algoritmo_huffman.py

=== CODIFICADOR/DECODIFICADOR DE HUFFMAN ===
Escolha uma opção:
1 - Codificar texto
2 - Decodificar binário
Opção: 1

Digite o texto para codificar: hello world

Texto codificado: 1001011110001...
```

### Modo 2: Decodificar Binário
```bash
Opção: 2

Digite o código binário: 1001011110001...

Texto decodificado: hello world
```

---

## 🏗️ Arquitetura do Projeto

```
algoritmo de huffman/
├── algoritmo_huffman.py          # Arquivo principal (main)
├── requirements.txt              # Dependências
├── README.md                     # Documentação
├── arvore_huffman.json          # Árvore salva (gerado automaticamente)
└── funcoes/                     # Módulo com todas as funções
    ├── __init__.py
    ├── node.py                  # Classe Node
    ├── contar_frequencias.py    # Conta caracteres
    ├── construir_arvore.py      # Constrói árvore
    ├── gerar_codigos.py         # Gera códigos binários
    ├── codificar.py             # Codifica texto
    ├── decodificar.py           # Decodifica binário
    ├── exibir_codigos.py        # Mostra tabela de códigos
    ├── decodificar_binario.py   # Decodifica com detalhes
    ├── plotar_arvore.py         # Visualiza árvore
    └── salvar_carregar_arvore.py # Salva/carrega árvore JSON
```

---

## 📚 Documentação das Funções

### 1. `node.py` - Classe Node

```python
class Node:
    def __init__(self, char, freq):
        self.char = char       # Caractere (ou None para nós internos)
        self.freq = freq       # Frequência acumulada
        self.left = None       # Filho esquerdo (0)
        self.right = None      # Filho direito (1)
    
    def __lt__(self, other):
        return self.freq < other.freq
```

**Propósito**: Representa um nó na árvore binária de Huffman.

**Por que `__lt__`?**
- O `heapq` precisa comparar nós para ordenar
- Definimos que nós com menor frequência têm prioridade
- Isso garante que a heap sempre mantenha os menores na raiz

**Estrutura**:
- **Folhas**: `char != None`, contêm um caractere
- **Nós internos**: `char == None`, apenas frequência acumulada

---

### 2. `contar_frequencias.py`

```python
def contar_frequencias(texto):
    freq = {}
    for char in texto:
        freq[char] = freq.get(char, 0) + 1
    return freq
```

**Entrada**: String com o texto original
**Saída**: Dicionário `{caractere: frequência}`

**Exemplo**:
```python
contar_frequencias("banana")
# Retorna: {'b': 1, 'a': 3, 'n': 2}
```

**Complexidade**: O(n) onde n = tamanho do texto

**Por que dicionário?**
- Acesso O(1) para incrementar contadores
- Estrutura natural para mapear char → freq

---

### 3. `construir_arvore.py`

```python
def construir_arvore(freqs):
    heap = [Node(char, freq) for char, freq in freqs.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    return heap[0]
```

**Entrada**: Dicionário de frequências
**Saída**: Raiz da árvore de Huffman

**Algoritmo**:
1. Cria um nó folha para cada caractere
2. Insere todos na heap (ordenados por frequência)
3. **Loop**: Enquanto houver mais de 1 nó:
   - Remove os 2 nós de menor frequência
   - Cria nó pai com frequência = soma dos filhos
   - Insere nó pai de volta na heap
4. O último nó restante é a raiz

**Por que heap?**
- Sempre acessa os 2 menores em O(log n)
- Inserção do nó mesclado em O(log n)
- Total: O(n log n) para construir árvore completa

**Visualização**:
```
Frequências: {a:5, b:9, c:12, d:13, e:16, f:45}

Passo 1: Mescla a(5) + b(9) = ab(14)
Passo 2: Mescla c(12) + d(13) = cd(25)
Passo 3: Mescla ab(14) + e(16) = abe(30)
...continua até restar 1 nó
```

---

### 4. `gerar_codigos.py`

```python
def gerar_codigos(raiz):
    if raiz is None:
        return {}
    
    codigos = {}
    
    def dfs(node, codigo_atual):
        if node.char is not None:  # É folha
            codigos[node.char] = codigo_atual
            return
        
        if node.left:
            dfs(node.left, codigo_atual + "0")
        if node.right:
            dfs(node.right, codigo_atual + "1")
    
    dfs(raiz, "")
    return codigos
```

**Entrada**: Raiz da árvore
**Saída**: Dicionário `{caractere: código binário}`

**Algoritmo DFS (Depth-First Search)**:
- Percorre a árvore recursivamente
- **Esquerda = 0**, **Direita = 1**
- Ao chegar numa folha, salva o código acumulado
- Códigos são **prefixo-livres** (nenhum código é prefixo de outro)

**Exemplo**:
```
    root
   /    \
  0      1
 / \      \
a   b      c

Códigos: {a: "00", b: "01", c: "1"}
```

**Complexidade**: O(n) onde n = número de nós

---

### 5. `codificar.py`

```python
def codificar(texto, codigos):
    return ''.join(codigos[char] for char in texto)
```

**Entrada**: Texto original + dicionário de códigos
**Saída**: String binária

**Exemplo**:
```python
codigos = {'a': '0', 'b': '10', 'c': '11'}
codificar("abc", codigos)
# Retorna: "01011"
```

**Complexidade**: O(m) onde m = comprimento do texto

**Por que join?**
- Concatenar strings com `+` é O(n²) em Python
- `join()` é O(n) pois aloca memória uma vez só

---

### 6. `decodificar.py`

```python
def decodificar(binario, raiz):
    if not binario or raiz is None:
        return ""
    
    resultado = []
    atual = raiz
    
    for bit in binario:
        if bit == '0':
            atual = atual.left
        else:
            atual = atual.right
        
        if atual.char is not None:  # Chegou numa folha
            resultado.append(atual.char)
            atual = raiz  # Volta para raiz
    
    return ''.join(resultado)
```

**Entrada**: String binária + raiz da árvore
**Saída**: Texto decodificado

**Algoritmo**:
1. Começa na raiz
2. Para cada bit:
   - `0` → vai para esquerda
   - `1` → vai para direita
3. Ao chegar numa folha:
   - Adiciona o caractere no resultado
   - **Volta para a raiz** (propriedade prefixo-livre)
4. Continua até processar todos os bits

**Por que funciona?**
- Códigos são prefixo-livres
- Logo, cada caminho da raiz até folha é único
- Não há ambiguidade na decodificação

**Complexidade**: O(m) onde m = tamanho do binário

---

### 7. `exibir_codigos.py`

```python
def exibir_codigos(codigos):
    print("\n" + "="*50)
    print("TABELA DE CÓDIGOS HUFFMAN")
    print("="*50)
    print(f"{'Caractere':<15} {'Código Binário':<20}")
    print("-"*50)
    
    for char, codigo in sorted(codigos.items()):
        char_display = repr(char) if char in [' ', '\n', '\t'] else char
        print(f"{char_display:<15} {codigo:<20}")
    
    print("="*50)
```

**Propósito**: Exibir tabela formatada de códigos

**Detalhe importante**:
```python
char_display = repr(char) if char in [' ', '\n', '\t'] else char
```
- Caracteres invisíveis (espaço, quebra de linha) são exibidos como `' '`, `'\n'`
- Melhora legibilidade da tabela

---

### 8. `decodificar_binario.py`

```python
def decodificar_binario(binario, raiz):
    print("\n" + "="*50)
    print("PROCESSO DE DECODIFICAÇÃO")
    print("="*50)
    
    resultado = []
    atual = raiz
    codigo_atual = ""
    
    for i, bit in enumerate(binario):
        codigo_atual += bit
        
        if bit == '0':
            atual = atual.left
        else:
            atual = atual.right
        
        if atual.char is not None:
            resultado.append(atual.char)
            print(f"Código '{codigo_atual}' → '{atual.char}'")
            atual = raiz
            codigo_atual = ""
    
    texto_final = ''.join(resultado)
    print("="*50)
    return texto_final
```

**Propósito**: Decodificar **mostrando cada passo** no terminal

**Diferença de `decodificar()`**:
- Imprime cada código → caractere
- Útil para debugging e aprendizado
- Mostra exatamente como a árvore é percorrida

---

### 9. `plotar_arvore.py`

```python
def plotar_arvore(raiz):
    # ... código complexo de visualização ...
```

**Propósito**: Desenhar árvore binária usando matplotlib

**Algoritmo de Posicionamento**:
```python
def calcular_posicoes(node, x=0, y=0, dx=2, nivel=0):
    # In-order traversal para posicionamento
    # Garante que nós não se sobrepõem
```

**Por que in-order?**
- Distribui nós uniformemente no eixo X
- Folhas ficam igualmente espaçadas
- Evita sobreposição automática

**Elementos visuais**:
- **Círculos**: Nós da árvore
  - Verde: Folhas (caracteres)
  - Cinza: Nós internos
- **Linhas**: Arestas
  - Azul: Esquerda (0)
  - Vermelho: Direita (1)
- **Labels 0/1**: Mostram caminho binário

**Configurações**:
```python
dx = 2  # Espaçamento horizontal entre folhas
dy = 2  # Espaçamento vertical entre níveis
raio = 0.5  # Tamanho dos círculos
```

---

### 10. `salvar_carregar_arvore.py`

```python
def serializar_para_dict(node):
    """Converte árvore em dicionário"""
    if node is None:
        return None
    return {
        'char': node.char,
        'freq': node.freq,
        'left': serializar_para_dict(node.left),
        'right': serializar_para_dict(node.right)
    }

def dict_para_arvore(data):
    """Reconstrói árvore a partir de dicionário"""
    if data is None:
        return None
    node = Node(data['char'], data['freq'])
    node.left = dict_para_arvore(data['left'])
    node.right = dict_para_arvore(data['right'])
    return node

def salvar_arvore(raiz, caminho='arvore_huffman.json'):
    """Salva a árvore de Huffman em um arquivo JSON"""
    data = serializar_para_dict(raiz)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Árvore salva em: {caminho}")

def carregar_arvore(caminho='arvore_huffman.json'):
    """Carrega a árvore de Huffman de um arquivo JSON"""
    with open(caminho, 'r', encoding='utf-8') as f:
        data = json.load(f)
    raiz = dict_para_arvore(data)
    print(f"✓ Árvore carregada de: {caminho}")
    return raiz
```

**Propósito**: Salvar e carregar árvore de Huffman em formato JSON

**Funções incluídas**:
- `serializar_para_dict()`: Converte árvore em dicionário (função auxiliar interna)
- `dict_para_arvore()`: Reconstrói árvore do dicionário (função auxiliar interna)
- `salvar_arvore()`: Interface pública para salvar árvore em JSON
- `carregar_arvore()`: Interface pública para carregar árvore do JSON

**Por que recursivo?**
- Árvores são estruturas recursivas por natureza
- Cada nó é processado da mesma forma
- JSON suporta estruturas aninhadas perfeitamente

**Formato JSON**:
```json
{
  "char": null,
  "freq": 100,
  "left": {
    "char": "a",
    "freq": 45,
    "left": null,
    "right": null
  },
  "right": { ... }
}
```

**Parâmetros importantes**:
- `ensure_ascii=False`: Permite caracteres UTF-8 (acentos, emojis)
- `indent=2`: Formata JSON legível

**Uso**:
```python
# Salvar
salvar_arvore(raiz)  # Salva em 'arvore_huffman.json'

# Carregar
raiz = carregar_arvore()  # Carrega de 'arvore_huffman.json'
```

---

## 🌳 O Algoritmo de Huffman

### Teoria

O algoritmo de Huffman é baseado em **codificação ótima de prefixo**:

1. **Objetivo**: Minimizar o comprimento médio do código
2. **Estratégia**: Caracteres frequentes → códigos curtos
3. **Garantia**: Nenhum código é prefixo de outro

### Exemplo Completo

**Texto**: `"ABRACADABRA"`

#### Passo 1: Contar Frequências
```
A: 5
B: 2
R: 2
C: 1
D: 1
```

#### Passo 2: Construir Árvore

```
Iteração 1: Mescla C(1) + D(1) = CD(2)
Heap: [B:2, R:2, CD:2, A:5]

Iteração 2: Mescla B(2) + R(2) = BR(4)
Heap: [CD:2, BR:4, A:5]

Iteração 3: Mescla CD(2) + BR(4) = CDBR(6)
Heap: [A:5, CDBR:6]

Iteração 4: Mescla A(5) + CDBR(6) = ACDBR(11)
Heap: [ACDBR:11]

Árvore final:
        (11)
       /    \
      A(5)  (6)
           /   \
         (2)   BR(4)
        /  \    /  \
      C(1) D(1) B(2) R(2)
```

#### Passo 3: Gerar Códigos
```
A: 0
C: 100
D: 101
B: 110
R: 111
```

#### Passo 4: Codificar
```
ABRACADABRA
0-110-111-0-100-0-101-0-110-111-0
= 0110111010001010110111​0
```

**Original**: 11 caracteres × 8 bits = 88 bits
**Comprimido**: 23 bits
**Taxa de compressão**: 73.9%

#### Passo 5: Decodificar
```
Binário: 0110111010001010110111​0

0 → A
110 → B
111 → R
0 → A
100 → C
0 → A
101 → D
0 → A
110 → B
111 → R
0 → A

Resultado: ABRACADABRA ✓
```

---

## 📊 Análise de Complexidade

### Tempo

| Operação | Complexidade | Justificativa |
|----------|--------------|---------------|
| Contar frequências | O(n) | Percorre texto uma vez |
| Construir heap inicial | O(m log m) | m caracteres únicos |
| Construir árvore | O(m log m) | m-1 mesclagens |
| Gerar códigos | O(m) | DFS visita cada nó |
| Codificar | O(n) | Percorre texto |
| Decodificar | O(n) | Percorre binário |
| **Total** | **O(n + m log m)** | n >> m na prática |

### Espaço

| Estrutura | Complexidade | Detalhes |
|-----------|--------------|----------|
| Frequências | O(m) | Dicionário com m chaves |
| Heap | O(m) | No máximo m nós |
| Árvore | O(m) | 2m-1 nós total |
| Códigos | O(m) | Dicionário |
| Texto codificado | O(n × k) | k = comprimento médio código |
| **Total** | **O(m + n × k)** | k < 8 tipicamente |

---

## 💡 Exemplos

### Exemplo 1: Texto Repetitivo
```python
texto = "aaaaabbbcc"
# Frequências: a:5, b:3, c:2

# Códigos ótimos:
# a: 0    (mais frequente)
# b: 10   
# c: 11   

# Original: 10 × 8 = 80 bits
# Comprimido: 5×1 + 3×2 + 2×2 = 15 bits
# Compressão: 81.25%
```

### Exemplo 2: Texto Uniforme
```python
texto = "abcd"
# Frequências: a:1, b:1, c:1, d:1

# Códigos:
# a: 00
# b: 01
# c: 10
# d: 11

# Original: 4 × 8 = 32 bits
# Comprimido: 4 × 2 = 8 bits
# Compressão: 75% (mesma de 2 bits fixos)
```

### Exemplo 3: Texto Real
```python
texto = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

# Caracteres mais frequentes:
# ' ': 8 vezes → código curto
# 'i': 7 vezes → código curto
# 't': 5 vezes

# Taxa de compressão típica: 40-60%
```

---

## 🔧 Melhorias Futuras

1. **Suporte a arquivos**
   - Ler/escrever arquivos binários
   - Compressão de imagens, PDFs

2. **Huffman Adaptativo**
   - Atualiza árvore dinamicamente
   - Melhor para streams

3. **Huffman Canônico**
   - Salva apenas comprimentos dos códigos
   - Reduz overhead da árvore

4. **Interface gráfica**
   - GUI com Tkinter
   - Visualização em tempo real

5. **Otimizações**
   - Usar bitarray para economizar memória
   - Paralelizar codificação de arquivos grandes

---

## 📖 Referências

- Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes"
- Cormen, T. H. et al. "Introduction to Algorithms" 
- [Wikipedia: Huffman Coding]

---

## 👨‍💻 Autor

Samuel Cotinguiba

---

## 📄 Licença

Este projeto é livre para uso educacional.
