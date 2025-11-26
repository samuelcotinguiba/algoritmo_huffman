def decodificar_binario(binario, raiz):
    """
    Decodifica uma string binária usando a árvore de Huffman
    Exibe o processo passo a passo no terminal
    """
    if raiz is None:
        return ""

    print("\n=== PROCESSO DE DECODIFICAÇÃO ===")
    resultado = []
    node = raiz
    caminho = ""
    
    for i, bit in enumerate(binario):
        caminho += bit
        node = node.left if bit == '0' else node.right
        
        if node is None:
            raise ValueError(f"Bitstream inválido na posição {i}")
        
        # Quando encontra uma folha (caractere)
        if node.char is not None:
            char_display = repr(node.char) if node.char in [' ', '\n', '\t'] else node.char
            print(f"  {caminho} → {char_display}")
            resultado.append(node.char)
            node = raiz
            caminho = ""
    
    texto_final = ''.join(resultado)
    print(f"\n[RESULTADO] {texto_final}")
    return texto_final
