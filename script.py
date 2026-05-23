import os
import time
import re
import musicbrainzngs
from mutagen.id3 import ID3, TYER, TDRC, TPE1, TIT2, TALB, ID3NoHeaderError

# 1. Configuração da API
musicbrainzngs.set_useragent('NomeDoScript', '1.0', 'seu_email@email.com')

def limpar_nome_album(texto):
    if not texto: return ''
    # Remove parênteses e colchetes
    texto = re.sub(r'\([^)]*\)|\[[^\]]*\]', '', texto)
    return texto.strip()

def buscar_ano_online(artista, album):
    # REGRA: Pega apenas o primeiro artista caso haja ";" ou "/"
    # Ex: "Michael Jackson; Paul McCartney" -> "Michael Jackson"
    primeiro_artista = re.split(r'[;/]', artista)[0].strip()
    
    album_busca = limpar_nome_album(album)
    
    try:
        # Busca refinada com o primeiro artista apenas
        query = f'release:"{album_busca}" AND artist:"{primeiro_artista}"'
        resultado = musicbrainzngs.search_releases(query=query, limit=1)
        
        if not resultado['release-list']:
            # Backup: Busca apenas pelo nome do álbum
            resultado = musicbrainzngs.search_releases(release=album_busca, limit=1)

        if resultado['release-list']:
            data = resultado['release-list'][0].get('date', '')
            return data[:4] if data else None
    except:
        return None
    return None

def processar_biblioteca(diretorio):
    for raiz, _, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith('.mp3'):
                caminho = os.path.join(raiz, nome_arquivo)
                try:
                    try:
                        audio_leitura = ID3(caminho)
                    except ID3NoHeaderError:
                        audio_leitura = ID3()

                    # Lemos as tags brutas
                    artista_bruto = str(audio_leitura.get('TPE1', '')).strip()
                    titulo = str(audio_leitura.get('TIT2', '')).strip()
                    album = str(audio_leitura.get('TALB', '')).strip()
                    
                    if artista_bruto and album:
                        print(f'\nOriginal: {artista_bruto} - {album}')
                        
                        ano_correto = buscar_ano_online(artista_bruto, album)
                        time.sleep(1) 
                        
                        if ano_correto:
                            # LIMPEZA E RECONSTRUÇÃO (Mantendo o artista original com ";" no arquivo)
                            audio_leitura.delete(caminho)
                            
                            novas_tags = ID3()
                            # Aqui salvamos o artista bruto (com todos os nomes) para você não perder dados
                            novas_tags.add(TPE1(encoding=1, text=artista_bruto))
                            novas_tags.add(TIT2(encoding=1, text=titulo))
                            novas_tags.add(TALB(encoding=1, text=album))
                            novas_tags.add(TYER(encoding=1, text=ano_correto))
                            novas_tags.add(TDRC(encoding=1, text=ano_correto))
                            
                            novas_tags.save(caminho, v2_version=3)
                            print(f'>>> SUCESSO: {ano_correto} gravado.')
                        else:
                            print(f'>>> Não encontrado no MusicBrainz.')
                    else:
                        print(f'Pulado: {nome_arquivo} (Tags incompletas)')

                except Exception as e:
                    print(f'Erro em {nome_arquivo}: {e}')

processar_biblioteca('.')
