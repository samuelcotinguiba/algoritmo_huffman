def exibir_codigos(codigos):
    """
    Exibe os códigos de Huffman de forma organizada
    Mostrando caractere -> código binário (0s e 1s)
    """
    print("\n=== TABELA DE CÓDIGOS HUFFMAN ===")
    print(f"{'Caractere':<15} {'Código Binário':<20} {'Bits'}")
    print("-" * 50)
    
    # Ordenar por tamanho do código (mais eficientes primeiro)
    for char, codigo in sorted(codigos.items(), key=lambda x: (len(x[1]), x[0])):
        char_display = repr(char) if char in [' ', '\n', '\t'] else char
        print(f"{char_display:<15} {codigo:<20} {len(codigo)}")
    
    print("-" * 50)
