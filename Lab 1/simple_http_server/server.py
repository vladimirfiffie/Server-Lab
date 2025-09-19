import socket
import os
import mimetypes

HOST = "127.0.0.1"
PORT = 8080
ROOT = os.path.abspath("./www")

def build_response(status, content_type, body, keep_alive=False):
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        f"Connection: {'keep-alive' if keep_alive else 'close'}",
        "\r\n"
    ]
    return "\r\n".join(headers).encode() + body

def handle_request(request):
    lines = request.split("\n")
    try:
        method, path, _ = lines[0].split()
    except ValueError:
        return build_response("400 Bad Request", "text/plain", b"Bad Request"), False

    headers = {k.lower(): v.strip() for k, _, v in (line.partition(":") for line in lines[1:] if ":" in line)}
    keep_alive = headers.get("connection", "").lower() == "keep-alive"

    print(f"→ {method} {path} (keep-alive={keep_alive})")

    if method != "GET":
        return build_response("405 Method Not Allowed", "text/plain", b"Method Not Allowed", keep_alive), keep_alive

    if path == "/":
        path = "/index.html"

    filepath = os.path.abspath(os.path.join(ROOT, path.lstrip("/")))

    if not filepath.startswith(ROOT):
        return build_response("403 Forbidden", "text/plain", b"Forbidden", keep_alive), keep_alive

    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            body = f.read()
        content_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
        return build_response("200 OK", content_type, body, keep_alive), keep_alive
    else:
        error_page = os.path.join(ROOT, "404.html")
        if os.path.isfile(error_page):
            with open(error_page, "rb") as f:
                body = f.read()
            return build_response("404 Not Found", "text/html", body, keep_alive), keep_alive
        else:
            return build_response("404 Not Found", "text/plain", b"File Not Found", keep_alive), keep_alive

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server running on http://{HOST}:{PORT}/ (CTRL+C to stop)")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    while True:
                        request = client_socket.recv(1024).decode(errors="ignore")
                        if not request:
                            break
                        response, keep_alive = handle_request(request)
                        client_socket.sendall(response)
                        if not keep_alive:
                            break
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
