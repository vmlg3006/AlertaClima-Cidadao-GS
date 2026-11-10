import argparse
from app.api import criar_app
from app.database import inicializar
from app.tcp_status import iniciar_tcp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tcp', action='store_true', help='Executar o servidor TCP de status')
    args = parser.parse_args()
    if args.tcp:
        iniciar_tcp()
    else:
        inicializar()
        criar_app().run(host='127.0.0.1', port=5000, debug=False)


if __name__ == '__main__':
    main()
