def decodificar(binario, raiz):
    """
    Entrada: string binária + raiz da árvore
    Saída: texto original
    """
    if raiz is None:
        return ""

    resultado = []
    node = raiz
    for bit in binario:
        node = node.left if bit == '0' else node.right
        if node is None:
            raise ValueError("Bitstream inválido para a árvore fornecida")
        if node.char is not None:
            resultado.append(node.char)
            node = raiz

    return ''.join(resultado)
