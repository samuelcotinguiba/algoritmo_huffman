def plotar_arvore(raiz):
    """
    Desenha a árvore binária usando matplotlib.
    """
    import matplotlib.pyplot as plt

    if raiz is None:
        print("Árvore vazia.")
        return

    positions = {}

    def assign_pos(node, depth=0, x=[0]):
        if node is None:
            return
        assign_pos(node.left, depth + 1, x)
        positions[node] = (x[0], -depth)
        x[0] += 1
        assign_pos(node.right, depth + 1, x)

    assign_pos(raiz)

    fig, ax = plt.subplots(figsize=(8, 4))
    for node, (x, y) in positions.items():
        label = f"{node.char}:{node.freq}" if node.char is not None else f"*:{node.freq}"
        ax.text(x, y, label, ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white'))
        if node.left:
            x2, y2 = positions[node.left]
            ax.plot([x, x2], [y, y2], 'k-')
        if node.right:
            x2, y2 = positions[node.right]
            ax.plot([x, x2], [y, y2], 'k-')

    ax.axis('off')
    plt.tight_layout()
    plt.show()
