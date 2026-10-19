import sys
import os

# Adiciona a pasta src ao sys.path para que o Python consiga encontrar o pacote buscador
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from buscador.core import process_history
except ImportError as e:
    print(f"Erro ao importar o módulo buscador: {e}")
    sys.exit(1)

def main():
    print("Iniciando a extração do histórico MyActivity...")
    try:
        # Tenta processar o arquivo padrão
        process_history()
        print("Processo concluído com sucesso! Verifique o arquivo historico.json")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o arquivo 'Minhaatividade.html' está na raiz do projeto.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
