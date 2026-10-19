import json
from pathlib import Path
from bs4 import BeautifulSoup


def obter_data(div):
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None
    textos = [t.strip() for t in content_cell.find_all(
        string=True, recursive=False) if t.strip()]
    return textos[-1] if textos else None


def process_history(input_file='Minhaatividade_teste.html', output_file='historico.json'):
    caminho_arquivo = Path(input_file)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo de entrada não encontrado: {input_file}")

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        content = BeautifulSoup(file, "html.parser")

    historico = []
    for div in content.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"):
        data = obter_data(div)
        lista_info = div.find_all("a")

        if len(lista_info) == 0:
            continue

        if len(lista_info) > 2:
            video = lista_info[0]
            canal = lista_info[1]
            historico.append({
                "titulo_video": video.text.strip(),
                "link_video": video["href"],
                "nome_canal": canal.text.strip(),
                "link_canal": canal["href"],
                "data": data
            })
        else:
            pesquisa = lista_info[0]
            historico.append({
                "pesquisa": pesquisa.text.strip(),
                "link_pesquisa": pesquisa["href"],
                "data": data
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    process_history()
