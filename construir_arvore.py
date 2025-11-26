from heapq import heappush, heappop
from node import Node

def construir_arvore(freqs):
    """
    Entrada: dicionário de frequências
    Saída: raiz da árvore de Huffman
    """
    heap = []
    for ch, f in freqs.items():
        heappush(heap, (f, Node(ch, f)))

    if not heap:
        return None

    while len(heap) > 1:
        f1, n1 = heappop(heap)
        f2, n2 = heappop(heap)
        parent = Node(None, f1 + f2)
        parent.left = n1
        parent.right = n2
        heappush(heap, (parent.freq, parent))

    return heappop(heap)[1]
