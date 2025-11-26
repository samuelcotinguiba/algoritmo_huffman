import json
import os
import sys
import runpy

# Carregar Node
_m = runpy.run_path(os.path.join(os.path.dirname(__file__), 'node.py'))
Node = _m['Node']


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
    """
    Salva a árvore de Huffman em um arquivo JSON
    """
    data = serializar_para_dict(raiz)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Árvore salva em: {caminho}")


def carregar_arvore(caminho='arvore_huffman.json'):
    """
    Carrega a árvore de Huffman de um arquivo JSON
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        data = json.load(f)
    raiz = dict_para_arvore(data)
    print(f"✓ Árvore carregada de: {caminho}")
    return raiz
