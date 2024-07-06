try:
    import yt_dlp
    from threading import Thread
    from pytube import Playlist, YouTube
    from concurrent.futures import ThreadPoolExecutor
    import os
except ImportError as e:
    missing_lib = str(e).split("'")[1]  # Captura a parte entre aspas da mensagem de erro
    print(f"Erro ao importar a biblioteca: {missing_lib}")
    print(f"Por favor, instale a biblioteca faltante usando o comando: pip install {missing_lib}")
    exit(1)


def clear_terminal():
    os_system = os.name  # 'posix' para Unix/Linux/Mac, 'nt' para Windows

    # Executa o comando de limpeza apropriado para o sistema operacional
    if os_system == 'posix':
        os.system('clear')  # Comando para Unix/Linux/Mac
    elif os_system == 'nt':
        os.system('cls')  # Comando para Windows
    else:
        print("Sistema operacional não suportado para limpeza de tela automática.")

def download_videos(video_info, directory):
    """Função para baixar um único vídeo usando yt-dlp."""
    ydl_opts = {
        'outtmpl': f'{directory}/%(title)s.%(ext)s',
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_info['id']}"])

def list_and_download_videos(url, directory, modelo):
    if modelo == 'videos':
        url += '/videos/'
    elif modelo == 'shorts':
        url += '/shorts/'

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    threads = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        if 'entries' in result:
            for video in result['entries']:
                if 'id' in video and video['id']:
                    # Criar e iniciar uma thread para cada vídeo
                    thread = Thread(target=download_videos, args=(video, directory))
                    thread.start()
                    threads.append(thread)
    
    # Esperar todas as threads terminarem
    for thread in threads:
        thread.join()

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
        clear_terminal()
        opcoes = "Digite o número da opção desejada:\n1 - baixar um vídeo \n2 - baixar uma playlist completa \n3 - baixar todos os vídeos do canal \n4 - baixar todos os shorts do canal \n> "
        choice = int(input(opcoes).lower())
        url = input("Digite a URL do canal, vídeo ou da playlist: ")
        download_path = input("Digite o caminho do diretório para salvar o(s) vídeo(s): ")

        if choice == 1:
            yt = YouTube(url)
            download_video(yt, download_path)
        elif choice == 2:
            download_playlist(url, download_path)
        elif choice == 3:
            list_and_download_videos(url, download_path, 'videos')
        elif choice == 4:
            list_and_download_videos(url, download_path, 'shorts')
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"Erro durante a execução do script: {e}")
        
if __name__ == "__main__":
    main()

