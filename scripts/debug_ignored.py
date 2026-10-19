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

def debug_ignored_items(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        content = BeautifulSoup(file, "html.parser")
    
    divs = content.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp")
    
    ignored_count = 0
    for i, div in enumerate(divs):
        links = div.find_all("a")
        if len(links) == 0:
            ignored_count += 1
            print(f"--- Item Ignorado {i} ---")
            # Print a simplified version of the div content to see what's inside
            print(div.get_text(separator=' | ', strip=True))
            print("-" * 30)
            if ignored_count >= 10: # Limit to first 10 to avoid flooding
                break

if __name__ == "__main__":
    debug_ignored_items("Minhaatividade_teste.html")
