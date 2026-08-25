import yt_dlp
import os

def download_media(url, choice):
    """
    Скачивает медиа с YouTube, TikTok, SoundCloud.
    
    Аргументы:
        url (str): ссылка на видео/трек
        choice (str): 'video_1080_mp4', 'video_720_mp4', 'video_1080_mkv', 'video_720_mkv', 'audio_mp3', 'audio_m4a', 'audio_flac'
    
    Возвращает:
        tuple: (file_path, metadata) или (None, None) при ошибке
    """
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'writethumbnail': True,
        'postprocessors': [],
    }

    os.makedirs('downloads', exist_ok=True)

    parts = choice.split('_')
    media_type = parts[0]  # 'video' или 'audio'
    
    if media_type == 'video':
        height = parts[1]
        fmt = parts[2]  # mp4, mkv, webm
        ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
        ydl_opts['merge_output_format'] = fmt
    else:  # audio
        codec = parts[1]  # mp3, m4a, flac
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': codec, 'preferredquality': '192'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if media_type == 'audio':
                base, _ = os.path.splitext(filename)
                filename = f"{base}.{codec}"
            
            # Безопасное получение метаданных
            metadata = {
                'title': info.get('track', info.get('title', 'Unknown Title')),
                'artist': info.get('artist', info.get('uploader', 'Unknown Artist')),
                'thumbnail': info.get('thumbnail'),
            }
            return filename, metadata
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None, None