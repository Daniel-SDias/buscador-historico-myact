import json

def compare_json():
    try:
        with open('historico.json', 'r', encoding='utf-8') as f1, \
             open('historico_1.json', 'r', encoding='utf-8') as f2:
            d1 = json.load(f1)
            d2 = json.load(f2)
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return

    print(f"Total itens H1: {len(d1)}")
    print(f"Total itens H1_1: {len(d2)}")

    if len(d1) != len(d2):
        print("❌ Tamanhos diferentes!")
        return

    diffs = 0
    for i in range(len(d1)):
        if d1[i] != d2[i]:
            diffs += 1
            if diffs <= 3:
                print(f"\n--- Diferença no índice {i} ---")
                print(f"Novo (H1): {d1[i]}")
                print(f"Antigo (H1_1): {d2[i]}")
            if diffs >= 100: # Cap total output
                break
    
    if diffs == 0:
        print("\n✅ Os arquivos são identicamente iguais em conteúdo!")
    else:
        print(f"\n❌ Foram encontradas {diffs} diferenças.")

if __name__ == "__main__":
    compare_json()
