import os
import sys
import runpy

# Carregar módulos da pasta funcoes
script_dir = os.path.dirname(os.path.abspath(__file__))
funcoes_dir = os.path.join(script_dir, 'funcoes')

_m = runpy.run_path(os.path.join(funcoes_dir, 'contar_frequencias.py'))
contar_frequencias = _m['contar_frequencias']
_m = runpy.run_path(os.path.join(funcoes_dir, 'construir_arvore.py'))
construir_arvore = _m['construir_arvore']
_m = runpy.run_path(os.path.join(funcoes_dir, 'gerar_codigos.py'))
gerar_codigos = _m['gerar_codigos']
_m = runpy.run_path(os.path.join(funcoes_dir, 'codificar.py'))
codificar = _m['codificar']
_m = runpy.run_path(os.path.join(funcoes_dir, 'decodificar.py'))
decodificar = _m['decodificar']
_m = runpy.run_path(os.path.join(funcoes_dir, 'decodificar_binario.py'))
decodificar_binario = _m['decodificar_binario']
_m = runpy.run_path(os.path.join(funcoes_dir, 'exibir_codigos.py'))
exibir_codigos = _m['exibir_codigos']
_m = runpy.run_path(os.path.join(funcoes_dir, 'salvar_carregar_arvore.py'))
salvar_arvore = _m['salvar_arvore']
carregar_arvore = _m['carregar_arvore']
listar_arvores = _m['listar_arvores']
_m = runpy.run_path(os.path.join(funcoes_dir, 'plotar_arvore.py'))
plotar_arvore = _m['plotar_arvore']


def main():
	print("=== Algoritmo de Huffman ===")
	print("\n1 - Codificar texto")
	print("2 - Decodificar binário")
	print("3 - Listar árvores salvas")
	opcao = input("\nEscolha uma opção (1/2/3): ").strip()
	
	if opcao == '1':
		# CODIFICAÇÃO
		texto = input("\nDigite o texto para codificar: ")
		
		if not texto:
			print("Texto vazio!")
			return
	
		# Pipeline completo
		freqs = contar_frequencias(texto)
		raiz = construir_arvore(freqs)
		codigos = gerar_codigos(raiz)
		
		# Exibir tabela de códigos (0s e 1s)
		exibir_codigos(codigos)
		
		# Codificação
		codificado = codificar(texto, codigos)
		
		# Salvar árvore com texto original no histórico
		salvar_arvore(raiz, texto)
		
		print(f"\n[ENTRADA] {texto}")
		print(f"[CODIFICADO] {codificado}")
		
		# Decodificação com processo detalhado
		decodificado = decodificar_binario(codificado, raiz)
		
		# Estatísticas
		print(f"\n=== ESTATÍSTICAS ===")
		print(f"Tamanho original: {len(texto) * 8} bits")
		print(f"Tamanho codificado: {len(codificado)} bits")
		print(f"Taxa de compressão: {len(codificado) / (len(texto) * 8) * 100:.1f}%")
		
		# Opcional: mostrar árvore
		ver_arvore = input("\nMostrar árvore? (s/n): ").lower()
		if ver_arvore == 's':
			try:
				plotar_arvore(raiz)
			except Exception as e:
				print(f"Erro ao plotar: {e}")
				print("Instale matplotlib: pip3 install matplotlib")
	
	elif opcao == '2':
		# DECODIFICAÇÃO
		binario = input("\nDigite o código binário para decodificar: ").strip()
		
		if not binario:
			print("Código vazio!")
			return
		
		if not all(c in '01' for c in binario):
			print("Erro: O código deve conter apenas 0s e 1s!")
			return
		
		try:
			# Listar e escolher árvore
			arvores = listar_arvores()
			if not arvores:
				print("\n✗ Nenhuma árvore salva. Codifique um texto primeiro.")
				return
			
			escolha = input("\nEscolha o número da árvore (Enter = última): ").strip()
			indice = -1 if not escolha else int(escolha) - 1
			
			# Carregar árvore escolhida
			raiz = carregar_arvore(indice)
			
			# Gerar códigos para exibição
			codigos = gerar_codigos(raiz)
			exibir_codigos(codigos)
			
			# Decodificar
			print(f"\n[BINÁRIO] {binario}")
			decodificado = decodificar_binario(binario, raiz)
			print(f"\n✓ Decodificação bem-sucedida!")
			
		except FileNotFoundError:
			print("\n✗ Erro: Árvore não encontrada!")
			print("Execute a codificação primeiro para gerar a árvore.")
			return
		except (ValueError, IndexError) as e:
			print(f"\n✗ Erro: {e}")
			return
		except Exception as e:
			print(f"Erro na decodificação: {e}")
			return
		
		# Opcional: mostrar árvore
		ver_arvore = input("\nMostrar árvore? (s/n): ").lower()
		if ver_arvore == 's':
			try:
				plotar_arvore(raiz)
			except Exception as e:
				print(f"Erro ao plotar: {e}")
				print("Instale matplotlib: pip3 install matplotlib")
	
	elif opcao == '3':
		# LISTAR ÁRVORES
		listar_arvores()
	
	else:
		print("Opção inválida!")


if __name__ == "__main__":
	while True:
		main()
		
		continuar = input("\n\nDeseja continuar? (s/n): ").lower().strip()
		if continuar != 's':
			print("\n✓ Programa encerrado. Até logo!")
			break
		print("\n" + "="*50 + "\n")