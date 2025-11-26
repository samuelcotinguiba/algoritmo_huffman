def plotar_arvore(raiz):
    """
    Desenha a árvore binária usando matplotlib com melhor visualização.
    """
    try:
        import matplotlib
        # Sem definir backend - deixa o matplotlib escolher automaticamente
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    except ImportError as e:
        print(f"Erro ao importar matplotlib: {e}")
        print("Instale com: pip3 install matplotlib")
        return

    if raiz is None:
        print("Árvore vazia.")
        return

    positions = {}
    
    def altura_arvore(node):
        if node is None:
            return 0
        return 1 + max(altura_arvore(node.left), altura_arvore(node.right))
    
    def contar_folhas(node):
        """Conta folhas para calcular largura necessária"""
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return contar_folhas(node.left) + contar_folhas(node.right)
    
    # Primeira passada: posicionar folhas usando in-order
    counter = [0]
    def posicionar_folhas(node, depth=0):
        if node is None:
            return
        posicionar_folhas(node.left, depth + 1)
        if node.left is None and node.right is None:
            # É uma folha
            positions[node] = (counter[0], -depth * 2)
            counter[0] += 2
        posicionar_folhas(node.right, depth + 1)
    
    # Segunda passada: posicionar nós internos (post-order)
    def posicionar_internos(node, depth=0):
        if node is None:
            return
        posicionar_internos(node.left, depth + 1)
        posicionar_internos(node.right, depth + 1)
        
        # Se não é folha, calcular posição baseada nos filhos
        if node.left is not None or node.right is not None:
            if node.left and node.right:
                x = (positions[node.left][0] + positions[node.right][0]) / 2
            elif node.left:
                x = positions[node.left][0] + 1
            else:
                x = positions[node.right][0] - 1
            positions[node] = (x, -depth * 2)
    
    try:
        posicionar_folhas(raiz)
        posicionar_internos(raiz)
    except Exception as e:
        print(f"Erro ao calcular posições: {e}")
        return
    
    fig, ax = plt.subplots(figsize=(max(16, contar_folhas(raiz) * 2), 10))
    
    # Desenhar arestas com labels 0 e 1
    for node, (x, y) in positions.items():
        if node.left:
            x2, y2 = positions[node.left]
            ax.plot([x, x2], [y, y2], 'k-', linewidth=2, zorder=1)
            # Label "0" na aresta esquerda
            mid_x, mid_y = (x + x2) / 2 - 0.1, (y + y2) / 2
            ax.text(mid_x, mid_y, '0', fontsize=12, color='blue', 
                   bbox=dict(boxstyle='circle', facecolor='lightblue', edgecolor='blue'))
        if node.right:
            x2, y2 = positions[node.right]
            ax.plot([x, x2], [y, y2], 'k-', linewidth=2, zorder=1)
            # Label "1" na aresta direita
            mid_x, mid_y = (x + x2) / 2 + 0.1, (y + y2) / 2
            ax.text(mid_x, mid_y, '1', fontsize=12, color='red',
                   bbox=dict(boxstyle='circle', facecolor='lightcoral', edgecolor='red'))
    
    # Desenhar nós
    for node, (x, y) in positions.items():
        if node.char is not None:
            # Nó folha (caractere)
            char_display = repr(node.char) if node.char in [' ', '\n', '\t'] else node.char
            label = f"{char_display}\n({node.freq})"
            color = 'lightgreen'
        else:
            # Nó interno
            label = f"*\n({node.freq})"
            color = 'lightgray'
        
        circle = patches.Circle((x, y), 0.5, facecolor=color, edgecolor='black', linewidth=2.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
    
    # Ajustar limites do gráfico
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    margin = 1.5
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title('Árvore de Huffman\n(0 = esquerda, 1 = direita)', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    try:
        plt.show()
    except Exception as e:
        # Se falhar ao exibir, salva em arquivo como fallback
        print(f"\nNão foi possível exibir na tela. Salvando em arquivo...")
        arquivo_saida = 'arvore_huffman.png'
        plt.savefig(arquivo_saida, dpi=150, bbox_inches='tight')
        print(f"✓ Árvore salva em: {arquivo_saida}")
        plt.close()
