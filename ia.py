from openai import APIConnectionError, APIError, AuthenticationError, BadRequestError, OpenAI, RateLimitError
from system import _System
from functools import lru_cache

class _IA:
    def __init__(self, system: _System)->None:
        self.system = system
        
        raw = self.system.read_file("api.txt")

        if raw is None:
            raw = ""

        cleaned = "\n".join([line for line in raw.splitlines() if not line.strip().startswith("```")])
        cleaned = cleaned.strip()

        key = ""
        for part in cleaned.split():
            if part.startswith("sk-"):
                key = part
                break

        if not key:
            key = cleaned

        if not key:
            raise ValueError("Chave da API não encontrada em 'api.txt'. Verifique o arquivo.")

        self.ia = OpenAI(api_key=key)
        pass
    
    lru_cache(maxsize=64)
    def send_message(self, message: str)->str:
        try:
            request_stream = self.ia.responses.create(
                model="gpt-5-nano",
                input=[{
                    "role": "user",
                    "content": f"Você é um assistente conciso, direto e simples, faça um resumo detalhado sobre o texto abaixo sem fazer perguntas após atender suas competências. Que são apenas resumir em PARÁGRAFOS uma trancrição de um vídeo que será passada agora:\n{message}"
                }],
                stream=True
            )

            return request_stream
        
        except RateLimitError:
            return "❌ Erro: limite de requisições atingido. Tente novamente mais tarde."
        except AuthenticationError:
            return "❌ Erro: chave da API inválida."
        except BadRequestError as e:
            return f"❌ Erro de requisição: {e}"
        except APIConnectionError:
            return "❌ Erro de conexão com a API."
        except APIError as e:
            return f"❌ Erro interno da API: {e}"
        except Exception as e:
            return f"❌ Erro inesperado: {type(e).__name__} - {e}"

def NewIA(system: _System)->_IA:
    return _IA(system=system)