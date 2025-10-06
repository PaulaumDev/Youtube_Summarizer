import threading
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
    
    print("--- Digite a url ---")
    url = system.input_link()
    
    system.clear_console()
    
    spinner_thread.start()
    
    transcript = transcriptorVideo.transcript(url)
    
    response = ia.send_message(transcript)
    
    stop_event.set()
    spinner_thread.join()
    
    system.clear_console()
    
    for event in response:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
