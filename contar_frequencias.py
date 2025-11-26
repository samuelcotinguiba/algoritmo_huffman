def contar_frequencias(texto):
    """
    Entrada: string
    Saída: dicionário {caractere: frequência}
    """
    freqs = {}
    for ch in texto:
        freqs[ch] = freqs.get(ch, 0) + 1
    return freqs
