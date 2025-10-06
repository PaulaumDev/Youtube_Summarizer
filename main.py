import threading, time
from system import NewSystem
from ia import NewIA
from video import NewTranscriptVideo

if __name__ == "__main__":
    system = NewSystem()
    ia = NewIA(system=system)
    transcriptorVideo = NewTranscriptVideo()
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=system.carregamento, args=(stop_event,))

    system.clear_console()
    
    url = system.input_link()
    
    system.clear_console()
    
    spinner_thread.start()
    system.delay(0.5) 
    transcript = transcriptorVideo.transcript(url)
    stop_event.set()
    spinner_thread.join()
    system.clear_console()

    if transcript != "":
        print("Transcrição obtida com sucesso!\n")
        system.delay(0.5)
        print("Processando sumarização...")

        response = ia.send_message(transcript)

        print("Concluído!\n")
        system.delay(0.5)
        system.clear_console()
        
        for event in response:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
    else:
        print("URL inválida. Certifique-se de que é um link do YouTube.")