# Agent Guide - Buscador Histórico MyActivity

## 🎯 Objetivo do Projeto
Extrair dados de navegação do YouTube a partir de dumps HTML do Google Takeout, transformando-os em JSON estruturado.

## ⚙️ Arquitetura Técnica
- **Linguagem:** Python.
- **Dependência Principal:** `BeautifulSoup`.
- **Fluxo:** `HTML (Minhaatividade.html)` $\rightarrow$ `BeautifulSoup Parsing` $\rightarrow$ `Lista de Dicionários` $\rightarrow$ `JSON (historico.json)`.

## 🔍 Lógica de Extração
Os itens são identificados pela classe `outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp`.
- **Vídeo:** Se o bloco possui mais de 2 links (`<a>`), assume-se que o primeiro é o vídeo e o segundo é o canal.
- **Pesquisa:** Se possui entre 1 e 2 links, assume-se que é uma pesquisa.
- **Ignorados:** Blocos sem links (ex: "Dismissed mix/shelf") são ignorados por não representarem consumo de conteúdo.

## ⚠️ Pontos de Atenção para Manutenção
- **Mudanças no HTML do Google:** Como o script depende de classes CSS específicas (`mdl-cell`, etc.), qualquer atualização na interface de exportação do Google pode quebrar o seletor.
- **Vídeos Removidos:** O script captura links mesmo de vídeos excluídos; o título pode vir como "Vídeo excluído" ou string vazia.
- **Encoding:** Sempre utilize `utf-8` ao ler ou escrever arquivos para evitar problemas com caracteres especiais brasileiros.
