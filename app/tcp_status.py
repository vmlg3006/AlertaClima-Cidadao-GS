import json
import socketserver


class StatusHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(3)
        try:
            comando = self.request.recv(32).decode('utf-8', errors='replace').strip().upper()
            resposta = {'servico': 'AlertaClima', 'status': 'ativo'} if comando == 'STATUS' else {'erro': 'Comando inválido'}
            self.request.sendall((json.dumps(resposta) + '\n').encode('utf-8'))
        except (OSError, UnicodeError):
            pass


class ServidorTCP(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def iniciar_tcp():
    # Restrito ao próprio computador: não expõe o status na internet.
    with ServidorTCP(('127.0.0.1', 5051), StatusHandler) as servidor:
        print('TCP STATUS em 127.0.0.1:5051')
        servidor.serve_forever()
