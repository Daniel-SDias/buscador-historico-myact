# Buscador Histórico MyActivity

Este projeto é uma ferramenta de extração de dados (scraper local) projetada para processar arquivos HTML exportados do "Minha Atividade" (My Activity) do Google. O foco principal é extrair o histórico de consumo de vídeos do YouTube e YouTube Music.

## 🚀 Funcionalidades

- **Extração de Vídeos:** Captura o título do vídeo, link do vídeo, nome do canal, link do canal e a data/hora da visualização.
- **Extração de Pesquisas:** Captura os termos pesquisados no YouTube e os respectivos links de pesquisa.
- **Saída Estruturada:** Converte a estrutura complexa do HTML do Google em um arquivo JSON organizado e fácil de manipular.

## 🛠️ Como usar

1. Exporte seus dados do Google via [Google Takeout](https://takeout.google.com/).
2. Salve o arquivo HTML de atividade do YouTube como `Minhaatividade.html` na raiz do projeto.
3. Execute o script de extração:
   ```bash
   python buscador.py
   ```
4. O resultado será gerado no arquivo `historico.json`.

## 📋 Requisitos

- Python 3.12+
- Biblioteca `beautifulsoup4`
