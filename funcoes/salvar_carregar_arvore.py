import json
import os
import runpy
from datetime import datetime

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


def salvar_arvore(raiz, texto_original='', caminho='arvores_huffman.json'):
    """
    Salva múltiplas árvores de Huffman em um arquivo JSON com histórico
    """
    # Carregar árvores existentes
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        dados = {"arvores": []}
    
    # Adicionar nova entrada
    nova_entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "texto": texto_original,
        "arvore": serializar_para_dict(raiz)
    }
    
    dados["arvores"].append(nova_entrada)
    
    # Salvar
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Árvore #{len(dados['arvores'])} salva em: {caminho}")


def carregar_arvore(indice=-1, caminho='arvores_huffman.json'):
    """
    Carrega uma árvore específica do histórico (padrão: última)
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo {caminho} não encontrado")
    
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    if not dados.get("arvores"):
        raise ValueError("Nenhuma árvore salva")
    
    entrada = dados["arvores"][indice]
    print(f"\n✓ Árvore carregada de: {entrada['timestamp']}")
    texto_preview = entrada['texto'][:50] + "..." if len(entrada['texto']) > 50 else entrada['texto']
    print(f"  Texto original: \"{texto_preview}\"")
    
    return dict_para_arvore(entrada['arvore'])


def listar_arvores(caminho='arvores_huffman.json'):
    """
    Lista todas as árvores salvas no histórico
    """
    if not os.path.exists(caminho):
        print("Nenhuma árvore salva ainda.")
        return []
    
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    if not dados.get("arvores"):
        print("Nenhuma árvore salva ainda.")
        return []
    
    print("\n=== ÁRVORES SALVAS ===")
    for i, entrada in enumerate(dados["arvores"], 1):
        texto_preview = entrada['texto'][:30] + "..." if len(entrada['texto']) > 30 else entrada['texto']
        print(f"{i}. [{entrada['timestamp']}] \"{texto_preview}\"")
    
    return dados["arvores"]
