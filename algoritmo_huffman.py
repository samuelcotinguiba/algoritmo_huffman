import os
import sys

# Garantir que o diretório do script esteja em sys.path (evita problemas com nomes de pastas)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Carregar módulos diretamente pelos caminhos dos arquivos para evitar problemas
import runpy

_m = runpy.run_path(os.path.join(script_dir, 'contar_frequencias.py'))
contar_frequencias = _m['contar_frequencias']
_m = runpy.run_path(os.path.join(script_dir, 'construir_arvore.py'))
construir_arvore = _m['construir_arvore']
_m = runpy.run_path(os.path.join(script_dir, 'gerar_codigos.py'))
gerar_codigos = _m['gerar_codigos']
_m = runpy.run_path(os.path.join(script_dir, 'codificar.py'))
codificar = _m['codificar']
_m = runpy.run_path(os.path.join(script_dir, 'decodificar.py'))
decodificar = _m['decodificar']
_m = runpy.run_path(os.path.join(script_dir, 'plotar_arvore.py'))
plotar_arvore = _m['plotar_arvore']


def main():
	print("=== Algoritmo de Huffman ===")
	texto = input("Digite o texto para codificar: ")
	
	if not texto:
		print("Texto vazio!")
		return

	# Pipeline completo
	freqs = contar_frequencias(texto)
	raiz = construir_arvore(freqs)
	codigos = gerar_codigos(raiz)
	codificado = codificar(texto, codigos)
	decodificado = decodificar(codificado, raiz)

	# Saída
	print(f"\n[ENTRADA] {texto}")
	print(f"[CODIFICADO] {codificado}")
	print(f"[DECODIFICADO] {decodificado}")
	print(f"\nTamanho original: {len(texto) * 8} bits")
	print(f"Tamanho codificado: {len(codificado)} bits")
	print(f"Taxa de compressão: {len(codificado) / (len(texto) * 8) * 100:.1f}%")
	
	# Opcional: mostrar árvore
	ver_arvore = input("\nMostrar árvore? (s/n): ").lower()
	if ver_arvore == 's':
		try:
			plotar_arvore(raiz)
		except:
			print("matplotlib não instalado. Use: pip3 install matplotlib")


if __name__ == "__main__":
	main()