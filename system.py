import time, os, threading, itertools

class _System:
    def __init__(self)->None:
        pass
    
    def delay(self, seconds: int)->None:
        time.sleep(seconds)

    def clear_console(self)->None:
        os.system("cls" if os.name == "nt" else "clear")

    def read_file(self, filename: str)->str:
        try:
            with open(filename, "r") as file:
                return file.read()
        except FileNotFoundError:
            # Se o arquivo não for encontrado no cwd atual, tenta o caminho relativo a este módulo.
            base_dir = os.path.dirname(__file__)
            alt_path = os.path.join(base_dir, filename)
            try:
                with open(alt_path, "r") as file:
                    return file.read()
            except FileNotFoundError:
                return ""
    
    def input_link(self)->str:
        print("Insira o link do vídeo a ser resumido (não pode ser link encurtado ou de mobile, \nsomente vídeos com legendas disponíveis): ", end="\0")
        url = input()
        
        if not "https://www.youtube.com" in url:
            print("link enviado é inválido!")
            return ""
        
        return url

    def carregamento(self, stop_event: threading.Event)->None:
        spinner = itertools.cycle(["|", "/", "-", "\\"])
        while not stop_event.is_set():
            print(f"\rProcessando {next(spinner)}", end="", flush=True)
            time.sleep(0.1)
        print("\r", end="")

def NewSystem()->_System:
    return _System()