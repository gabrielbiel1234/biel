ULTRA_AI_CLOUD/server.py
import json
import os
import re
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT.parent / "ULTRA_AI_COMPLETO"
PROJECTS = ROOT / "projects"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
PORT = int(os.environ.get("PORT", "10000"))


def ask_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Configure GEMINI_API_KEY nas variáveis do Render.")

    url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    payload = {
        "model": MODEL,
        "input": prompt,
        "store": False
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))

    answer = data.get("output_text", "")
    if not answer:
        for step in reversed(data.get("steps", [])):
            for part in step.get("content", []):
                if part.get("type") == "text":
                    answer += part.get("text", "")

    if not answer:
        raise RuntimeError("A IA não retornou uma resposta.")

    return answer


class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def translate_path(self, path):
        clean = unquote(urlparse(path).path).lstrip("/")
        base = ROOT if clean.startswith("projects/") else FRONTEND
        target = (base / clean).resolve()

        if os.path.commonpath([str(base.resolve()), str(target)]) != str(base.resolve()):
            return str(base / "arquivo-invalido")

        return str(target)

    def send_json(self, status, data):
        content = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 100000:
                return self.send_json(413, {"error": "Pedido muito grande."})

            body = json.loads(self.rfile.read(length).decode("utf-8"))

            if self.path == "/api/chat":
                message = str(body.get("message", "")).strip()
                if not message:
                    return self.send_json(400, {"error": "Digite uma mensagem."})

                prompt = (
                    "Você é o ULTRA AI, assistente em português brasileiro. "
                    "Responda com clareza e honestidade. "
                    "Não diga que executou ações que não realizou.\n\n"
                    + message
                )
                return self.send_json(200, {
                    "reply": ask_gemini(prompt),
                    "model": MODEL
                })

            if self.path == "/api/create-app":
                description = str(body.get("description", "")).strip()
                if not description:
                    return self.send_json(400, {
                        "error": "Descreva o aplicativo."
                    })

                prompt = (
                    "Crie um aplicativo web funcional em HTML, CSS e JavaScript. "
                    "Retorne SOMENTE JSON válido no formato: "
                    '{"files":[{"path":"index.html","content":"..."},'
                    '{"path":"style.css","content":"..."},'
                    '{"path":"script.js","content":"..."}]}. '
                    "Use somente esses três arquivos. "
                    "O HTML deve carregar style.css e script.js. "
                    "Interface responsiva em português. "
                    "Descrição: " + description
                )

                answer = ask_gemini(prompt)
                answer = re.sub(r"^```(?:json)?\s*", "", answer.strip())
                answer = re.sub(r"\s*```$", "", answer)

                result = json.loads(answer)
                generated = result.get("files", [])
                allowed = {"index.html", "style.css", "script.js"}

                folder_name = re.sub(
                    r"[^a-zA-Z0-9_-]+", "-",
                    description[:35]
                ).strip("-_").lower() or "novo-app"

                folder = PROJECTS / folder_name
                folder.mkdir(parents=True, exist_ok=True)

                saved = []
                for item in generated:
                    name = Path(str(item.get("path", ""))).name
                    content = item.get("content")

                    if name in allowed and isinstance(content, str):
                        (folder / name).write_text(content, encoding="utf-8")
                        saved.append(name)

                if "index.html" not in saved:
                    raise RuntimeError("A IA não criou o arquivo index.html.")

                return self.send_json(200, {
                    "message": "Aplicativo criado!",
                    "files": saved,
                    "path": "projects/" + folder_name,
                    "preview": "/projects/" + folder_name + "/index.html"
                })

            return self.send_json(404, {"error": "Rota não encontrada."})

        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            print("Erro Gemini:", detail)
            return self.send_json(502, {
                "error": "Erro na API Gemini. Confira a chave e o modelo."
            })
        except Exception as error:
            print("Erro:", str(error))
            return self.send_json(500, {"error": str(error)})


if __name__ == "__main__":
    PROJECTS.mkdir(exist_ok=True)
    print("ULTRA AI CLOUD iniciado na porta", PORT)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
