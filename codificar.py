def codificar(texto, codigos):
    """
    Entrada: texto e dicionário de códigos
    Saída: string binária codificada
    """
    return ''.join(codigos[ch] for ch in texto)
