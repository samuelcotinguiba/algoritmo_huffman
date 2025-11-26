def gerar_codigos(raiz):
    """
    Entrada: raiz da árvore
    Saída: dict {caractere: código binário}
    """
    codigos = {}

    def dfs(node, prefix):
        if node is None:
            return
        # folha
        if node.char is not None:
            # caso especial: árvore com um único caractere
            codigos[node.char] = prefix or "0"
            return
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(raiz, "")
    return codigos
