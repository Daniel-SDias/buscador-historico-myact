import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer


def obter_data(div: BeautifulSoup) -> str | None:
    """Extrai a data do bloco de atividade."""
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None
    textos = [t.strip() for t in content_cell.find_all(
        string=True, recursive=False) if t.strip()]
    return textos[-1] if textos else None


def extrair_product(div: BeautifulSoup) -> str:
    """Extrai o produto do cabeçalho (YouTube ou YouTube Music)."""
    header = div.find("p", class_="mdl-typography--title")
    if header:
        return header.get_text(strip=True).replace("\n", "").strip()
    return "YouTube"


def extrair_action_e_title(div: BeautifulSoup) -> tuple[str | None, str | None]:
    """
    Extrai a action (Watched, Viewed, Searched for, etc.) e o título/conteúdo.
    Retorna tupla (action, title).
    """
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None, None

    primeiro_link = content_cell.find("a")
    if not primeiro_link:
        return None, None

    # Find index of first link to get text before it
    link_index = None
    for i, elem in enumerate(content_cell.contents):
        if elem is primeiro_link:
            link_index = i
            break

    textos_antes = []
    if link_index is not None:
        for elem in content_cell.contents[:link_index]:
            if isinstance(elem, str) and elem.strip():
                textos_antes.append(elem.strip())

    action_texto = " ".join(textos_antes).strip()
    action_texto = re.sub(r"\s+", " ", action_texto).rstrip(" ")

    title = primeiro_link.get_text(strip=True)

    return action_texto, title


def extrair_channel_info(div: BeautifulSoup) -> tuple[str | None, str | None]:
    """Extrai nome e URL do canal (segundo link, se existir)."""
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None, None

    links = content_cell.find_all("a")
    if len(links) >= 2:
        canal = links[1]
        return canal.get_text(strip=True), canal.get("href", "")
    return None, None


def extrair_clicked_product(div: BeautifulSoup) -> str | None:
    """Extrai produto clicado (merch), se houver."""
    content_cell = div.find(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    if not content_cell:
        return None

    texto_completo = content_cell.get_text()
    match = re.search(
        r"Clicked on product:\s*\u2022\s*([^\n]+)", texto_completo)
    if match:
        return match.group(1).strip()
    return None


def determinar_content_type(product: str, action: str) -> str:
    """Determina o content_type baseado no product e action."""
    action_lower = action.lower()

    if product == "YouTube Music":
        return "song"
    if action_lower == "viewed":
        return "post"
    if action_lower == "searched for":
        return "search"
    if action_lower == "subscribed to":
        return "subscription"
    if action_lower.startswith("dismissed"):
        return "removed"
    if action_lower in ("watched", "liked"):
        return "video"
    if action_lower == "tracking watch time points on":
        return "tracking"
    return "unknown"


def process_history(input_file: str = 'Minhaatividade.html', output_file: str = 'historico.json') -> list[dict]:
    caminho_arquivo = Path(input_file)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo de entrada não encontrado: {input_file}")

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        only_cells = SoupStrainer(
            "div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp")
        content = BeautifulSoup(file, "lxml", parse_only=only_cells)

    historico: list[dict] = []
    for div in content.find_all("div", class_="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"):
        data = obter_data(div)
        product = extrair_product(div)
        action, title = extrair_action_e_title(div)

        if not action or not title:
            continue

        url_tag = div.find("a")
        url = url_tag.get("href", "") if url_tag else ""

        channel, channel_url = extrair_channel_info(div)
        clicked_product = extrair_clicked_product(div)
        content_type = determinar_content_type(product, action)

        item = {
            "product": product,
            "action": action,
            "content_type": content_type,
            "title": title,
            "url": url,
            "date": data,
            "channel": channel,
            "channel_url": channel_url,
            "clicked_product": clicked_product,
        }

        historico.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

    return historico


if __name__ == "__main__":
    process_history()
