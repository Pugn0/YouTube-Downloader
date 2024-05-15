try:
    from pytube import Playlist, YouTube
    from concurrent.futures import ThreadPoolExecutor
    import os
except ImportError as e:
    missing_lib = str(e).split("'")[1]  # Captura a parte entre aspas da mensagem de erro
    print(f"Erro ao importar a biblioteca: {missing_lib}")
    print(f"Por favor, instale a biblioteca faltante usando o comando: pip install {missing_lib}")
    exit(1)

def download_video(video, download_path):
    """Baixa um único vídeo do YouTube no diretório especificado."""
    try:
        stream = video.streams.get_highest_resolution()
        video_path = os.path.join(download_path, f"{video.title}.mp4")

        if not os.path.exists(video_path):
            stream.download(download_path)
            print(f"Download completo: {video.title}")
        else:
            print(f"Arquivo já existe: {video.title}")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {video.title}. Erro: {e}")

def download_playlist(playlist_url, download_path):
    """Baixa todos os vídeos de uma playlist do YouTube usando múltiplas threads."""
    try:
        pl = Playlist(playlist_url)
        num_cores = os.cpu_count() or 4
        print(f"Usando {num_cores} threads para o download.")
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(download_video, video, download_path) for video in pl.videos]
            for future in futures:
                future.result()
    except Exception as e:
        print(f"Erro ao processar a playlist: {e}")

def main():
    try:
        choice = input("Digite 'video' para baixar um vídeo ou 'playlist' para baixar uma playlist completa: ").lower()
        url = input("Digite a URL do vídeo ou da playlist: ")
        download_path = input("Digite o caminho do diretório para salvar o(s) vídeo(s): ")

        if choice == 'video':
            yt = YouTube(url)
            download_video(yt, download_path)
        elif choice == 'playlist':
            download_playlist(url, download_path)
        else:
            print("Opção inválida. Por favor, digite 'video' ou 'playlist'.")
    except Exception as e:
        print(f"Erro durante a execução do script: {e}")
        
if __name__ == "__main__":
    main()

