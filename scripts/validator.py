import json
from bs4 import BeautifulSoup
from pathlib import Path

def obter_data(div):
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None
    textos = [t.strip() for t in content_cell.find_all(
        string=True, recursive=False) if t.strip()]
    return textos[-1] if textos else None

def analyze_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        content = BeautifulSoup(file, "html.parser")
    
    divs = content.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp")
    total_divs = len(divs)
    
    processed = 0
    skipped_no_links = 0
    skipped_low_link_count = 0 # items that don't fit the current script's logic (though the current script handles any > 0)
    
    details = []

    for i, div in enumerate(divs):
        links = div.find_all("a")
        if len(links) == 0:
            skipped_no_links += 1
            details.append(f"Item {i}: Ignorado (0 links)")
        elif len(links) <= 2:
            processed += 1 # current script treats this as research
        elif len(links) > 2:
            processed += 1 # current script treats this as video
        else:
            skipped_low_link_count += 1

    print(f"--- Análise de {html_path} ---")
    print(f"Total de blocos de atividade encontrados: {total_divs}")
    print(f"Total de itens que seriam processados: {processed}")
    print(f"Total de itens IGNORADOS (sem links): {skipped_no_links}")
    
    if skipped_no_links > 0:
        print("\nExemplos de itens ignorados:")
        for d in details[:5]:
            print(d)

if __name__ == "__main__":
    analyze_html("Minhaatividade_teste.html")
