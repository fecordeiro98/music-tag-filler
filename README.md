# Script de Atualização de Ano em Arquivos MP3 via MusicBrainz

Este script em Python automatiza a busca e a gravação do ano de lançamento de álbuns musicais em arquivos `.mp3`. Ele lê as tags de metadados existentes, realiza uma busca na base de dados pública do **MusicBrainz** e atualiza as tags de ano (`TYER` e `TDRC`) mantendo a compatibilidade com a versão ID3v2.3.

## Funcionalidades

* **Varredura Recursiva:** Percorre o diretório indicado e subpastas em busca de arquivos `.mp3`.
* **Tratamento de Dados para Busca:**
  * Limpa o nome do álbum removendo textos entre parênteses e colchetes (ex: `(Deluxe Edition)` ou `[Remastered]`).
  * Trata artistas múltiplos separados por `;` ou `/`, utilizando apenas o primeiro integrante na busca para melhorar a precisão dos resultados.
* **Busca Refinada (Fallback):** Tenta primeiro buscar pela combinação exata de "Artista + Álbum". Caso não encontre, realiza uma segunda tentativa apenas pelo título do álbum.
* **Respeito aos Limites da API:** Implementa um intervalo de 1 segundo entre as requisições para evitar bloqueios pela API do MusicBrainz.

---

## Pré-requisitos e Dependências

Antes de executar o script, é necessário instalar as bibliotecas de terceiros utilizadas.

### 1. Instalação das dependências

```bash
pip install musicbrainzngs mutagen
```

* **`musicbrainzngs`**: Biblioteca cliente oficial para a API do MusicBrainz.
* **`mutagen`**: Biblioteca para manipulação de metadados de arquivos de áudio.

> [!IMPORTANT]
> ### 2. Configuração do User-Agent
>
> No início do script, há uma configuração de User-Agent exigida pelas diretrizes de uso da API do MusicBrainz:
>
> ```python
> musicbrainzngs.set_useragent('NomeDoScript', '1.0', 'seu_email@email.com')
> ```
>
> *Caso pretenda distribuir ou utilizar o script de forma persistente, recomenda-se alterar esses parâmetros para identificar sua própria aplicação.*

---

## Como o Script Funciona (Fluxo de Execução)

1. **Leitura do Arquivo:** O script varre o diretório e abre cada arquivo `.mp3` para ler as tags ID3 de Artista (`TPE1`), Título (`TIT2`) e Álbum (`TALB`).
2. **Normalização da Query:**
   * O nome do álbum é limpo de termos adicionais.
   * O nome do artista é truncado no primeiro caractere de divisão `;` ou `/`.
3. **Consulta à API:** Realiza a busca no MusicBrainz e extrai os 4 primeiros caracteres do campo de data (`YYYY`) do primeiro resultado retornado.
4. **Reescrita das Tags:** 
   * Se o ano for encontrado, as tags antigas do arquivo são limpas.
   * Um novo conjunto de tags ID3v2.3 é gravado contendo o Artista original bruto, o Título, o Álbum e as novas tags de ano: `TYER` (Year) e `TDRC` (Recording time).

---

## Como Executar

Por padrão, o script está configurado para processar a pasta atual onde ele se encontra (`'.'`).

1. Coloque o arquivo do script (ex: `atualizar_anos.py`) na pasta raiz da sua biblioteca de músicas (ou onde deseja testar).
2. Execute o script pelo terminal:

```bash
python atualizar_anos.py
```

---

## ⚠️ Atenção / Limitações Importantes

* **Substituição de Tags Existentes:** O método utilizado para salvar as novas tags (`audio_leitura.delete(caminho)`) remove **todas** as tags ID3 anteriores do arquivo antes de gravar as novas. Isso significa que outras tags que não sejam Artista, Título, Álbum e Ano (como gênero, número da faixa, capa do álbum ou comentários) **serão perdidas**. Recomenda-se testar o script em uma cópia de segurança dos seus arquivos antes de aplicá-lo em toda a biblioteca.
* **Dependência de Conexão:** O script requer conexão ativa com a internet para consultar a API do MusicBrainz.
* **Taxa de Acerto:** A precisão da busca depende diretamente da qualidade dos metadados iniciais (Artista e Álbum) e da presença da edição do álbum no banco de dados do MusicBrainz.

---

*Este texto foi gerado com inteligência artificial (IA)*
