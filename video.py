from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript
)
from pytube import YouTube
from pytube.exceptions import VideoUnavailable as PytubeVideoUnavailable
from functools import lru_cache

class _Video:
    def __init__(self)->None:
        pass
    
    lru_cache(maxsize=256)
    def transcript(self, url: str)->str:
        if not "https://youtube.com" in url:
            raise ValueError("URL inválida. Certifique-se de que é um link do YouTube.")
        else:
            try:
                try:
                    video_id = YouTube(url).video_id
                except PytubeVideoUnavailable:
                    print("O vídeo não está disponível no YouTube.")

                yt_transcriptor = YouTubeTranscriptApi()

                transcript_data = yt_transcriptor.fetch(
                    video_id=video_id,
                    languages=["pt", "en", "es", "de", "fr"]
                )

                transcript_str = "\n".join([snippet.text for snippet in transcript_data.snippets])
                return transcript_str

            except TranscriptsDisabled:
                print("As legendas do vídeo estão desativadas.")
            except NoTranscriptFound:
                print("Não foi possível encontrar legendas disponíveis para este vídeo.")
            except VideoUnavailable:
                print("O vídeo está indisponível (removido ou privado).")
            except CouldNotRetrieveTranscript:
                print("Erro ao tentar obter o transcript do vídeo.")
            except Exception as e:
                # Captura outros erros inesperados
                print(f"Ocorreu um erro inesperado: {e}")
    

def NewTranscriptVideo()->_Video:
    return _Video()