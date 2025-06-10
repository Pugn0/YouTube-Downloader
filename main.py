import yt_dlp
from pytube import Playlist, Channel
from concurrent.futures import ThreadPoolExecutor
import os

def download_video(video_url, download_path, format_type='mp4'):
    """Baixa um único vídeo do YouTube no diretório especificado."""
    try:
        if format_type == 'mp3':
            ydl_opts = {
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
            }
        else:  # mp4
            ydl_opts = {
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'quiet': False,
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Download completo: {video_url}")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {video_url}. Erro: {e}")

def download_playlist(playlist_url, download_path, format_type='mp4'):
    """Baixa todos os vídeos de uma playlist do YouTube, incluindo vídeos não listados."""
    try:
        pl = Playlist(playlist_url)
        num_cores = os.cpu_count() or 4
        print(f"Usando {num_cores} threads para o download.")
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(download_video, video.watch_url, download_path, format_type) for video in pl.videos]
            for future in futures:
                future.result()
    except Exception as e:
        print(f"Erro ao processar a playlist: {e}")

def download_all_videos_from_channel(channel_url, download_path, format_type='mp4'):
    """Baixa todos os vídeos de um canal do YouTube."""
    try:
        channel = Channel(channel_url)
        num_cores = os.cpu_count() or 4
        print(f"Usando {num_cores} threads para o download.")
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(download_video, video.watch_url, download_path, format_type) for video in channel.videos]
            for future in futures:
                future.result()
    except Exception as e:
        print(f"Erro ao processar os vídeos do canal: {e}")

def download_all_shorts_from_channel(channel_url, download_path, format_type='mp4'):
    """Baixa todos os shorts de um canal do YouTube."""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
        }
        url = channel_url + '/shorts/'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                num_cores = os.cpu_count() or 4
                print(f"Usando {num_cores} threads para o download.")
                with ThreadPoolExecutor(max_workers=num_cores) as executor:
                    futures = [executor.submit(download_video, f"https://www.youtube.com/watch?v={video['id']}", download_path, format_type) for video in result['entries']]
                    for future in futures:
                        future.result()
    except Exception as e:
        print(f"Erro ao processar os shorts do canal: {e}")

def main():
    try:
        opcoes = "Digite o número da opção desejada:\n1 - baixar um vídeo \n2 - baixar uma playlist completa \n3 - baixar todos os vídeos do canal \n4 - baixar todos os shorts do canal \n> "
        choice = int(input(opcoes))
        
        format_opcoes = "Escolha o formato de download:\n1 - MP4 (vídeo)\n2 - MP3 (áudio)\n> "
        format_choice = int(input(format_opcoes))
        format_type = 'mp3' if format_choice == 2 else 'mp4'
        
        url = input("Digite a URL do canal, vídeo ou da playlist: ")
        download_path = input("Digite o caminho do diretório para salvar o(s) arquivo(s): ")

        if choice == 1:
            download_video(url, download_path, format_type)
        elif choice == 2:
            download_playlist(url, download_path, format_type)
        elif choice == 3:
            download_all_videos_from_channel(url, download_path, format_type)
        elif choice == 4:
            download_all_shorts_from_channel(url, download_path, format_type)
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"Erro durante a execução do script: {e}")

if __name__ == "__main__":
    main()
