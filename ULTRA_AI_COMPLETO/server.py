import json
import os
import re
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, code, data):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self.send_json(400, {"error": "Pedido JSON inválido."})

        if self.path == "/api/chat":
            prompt = str(body.get("message", "")).strip()
            if not prompt:
                return self.send_json(400, {"error": "Digite uma mensagem."})
            system = ("Você é o ULTRA AI, um assistente útil que responde em português brasileiro. "
                      "Seja claro, honesto e objetivo. Não afirme que executou ações que não realizou.")
            payload = {
                "model": MODEL,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                "options": {"temperature": 0.4, "num_ctx": 2048}
            }
            try:
                req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=180) as response:
                    result = json.loads(response.read().decode("utf-8"))
                return self.send_json(200, {"reply": result.get("message", {}).get("content", ""), "model": MODEL})
            except urllib.error.URLError as e:
                return self.send_json(503, {"error": "Não consegui acessar o Ollama. Abra o Ollama e confirme que o modelo foi baixado. Detalhe: " + str(e)})
            except Exception as e:
                return self.send_json(500, {"error": "Erro ao consultar a IA: " + str(e)})

        if self.path == "/api/create-app":
            description = str(body.get("description", "")).strip()
            if not description:
                return self.send_json(400, {"error": "Descreva o aplicativo que deseja criar."})
            prompt = (
                "Crie um aplicativo web funcional com HTML, CSS e JavaScript puro, sem bibliotecas externas. "
                "Responda SOMENTE com JSON válido neste formato: "
                '{"files":[{"path":"index.html","content":"..."} ,'
                '{"path":"style.css","content":"..."},{"path":"script.js","content":"..."}]}. '
                "Use apenas esses três arquivos. Não use markdown nem cercas de código. "
                "O HTML deve carregar style.css e script.js. Faça uma interface responsiva e em português. "
                "Descrição do aplicativo: " + description
            )
            payload = {
                "model": MODEL, "stream": False,
                "messages": [
                    {"role": "system", "content": "Você é um desenvolvedor web experiente. Retorne somente JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                "format": "json",
                "options": {"temperature": 0.2, "num_ctx": 4096}
            }
            try:
                req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=300) as response:
                    result = json.loads(response.read().decode("utf-8"))
                content = result.get("message", {}).get("content", "")
                data = json.loads(content)
                generated = data.get("files", [])
                allowed = {"index.html", "style.css", "script.js"}
                if not generated:
                    raise ValueError("A IA não retornou arquivos.")
                folder = PROJECTS / re.sub(r"[^a-zA-Z0-9_-]+", "-", description[:35]).strip("-_").lower()
                folder.mkdir(parents=True, exist_ok=True)
                saved = []
                for item in generated:
                    name = Path(str(item.get("path", ""))).name
                    if name in allowed and isinstance(item.get("content"), str):
                        (folder / name).write_text(item["content"], encoding="utf-8")
                        saved.append(name)
                if "index.html" not in saved:
                    raise ValueError("A IA não criou index.html. Tente novamente com uma descrição mais simples.")
                return self.send_json(200, {"message": "Aplicativo criado!", "files": saved,
                    "path": str(folder.relative_to(ROOT)), "preview": "/" + str(folder.relative_to(ROOT)).replace("\\\\", "/") + "/index.html"})
            except urllib.error.URLError as e:
                return self.send_json(503, {"error": "O Ollama não está acessível. Abra o Ollama e tente novamente. " + str(e)})
            except Exception as e:
                return self.send_json(500, {"error": "Não consegui montar os arquivos. Tente novamente com uma descrição mais específica. Detalhe: " + str(e)})

        return self.send_json(404, {"error": "Rota não encontrada."})

    def log_message(self, format, *args):
        print("[ULTRA AI] " + (format % args))

if __name__ == "__main__":
    PROJECTS.mkdir(exist_ok=True)
    print("ULTRA AI disponível em http://localhost:8000")
    print("Modelo configurado:", MODEL)
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
