from youtube_transcript_api import YouTubeTranscriptApi 
from pytube import YouTube
from openai import OpenAI
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_console()

with open('api.txt', 'r') as api:
    key = api.read()

ia = OpenAI(api_key=key)
yt_transcript = YouTubeTranscriptApi()

# Passo 1: Receber o link do vídeo
url = input("Insira o link do vídeo a ser resumido (não pode ser link encurtado ou de mobile, somente vídeos com legendas disponíveis): ")
if not "https://www.youtube.com" in url:
    print("Esse link não é valido. Digite um link válido")
    time.sleep(1)
    clear_console()

else: 
    # Passo 2: Transcrever o vídeo
    print("Transcrevendo o vídeo da URL...")
    time.sleep(1)
    transcript = ""
    video_id = YouTube(url).video_id
    video_fetch = yt_transcript.fetch(video_id=video_id, languages=["pt", "en", "es", "de", "fr"])
    for snippet in video_fetch.snippets:
        transcript+=f"{snippet.text}\n"
    print("Trancrição feita! Iniciando resumo...")
    time.sleep(1.5)
    clear_console()

    # Passo 3: mandar a transcrição do vídeo para o chatgpt resumir
    request = ia.responses.create(
        model="gpt-5-nano",
        input=f"Você poderia me fazer um resumo detalhado dessa transcrição de um vídeo do youtube?\n{transcript}"
    )
    response = request.output_text
    
    # Passo 4: retornar o resumo
    print(response)
