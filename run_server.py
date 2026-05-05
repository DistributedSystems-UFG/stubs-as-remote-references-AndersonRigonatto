from server   import *
from constRPC import *

if __name__ == "__main__":
    print(f"[Servidor] Escutando em 0.0.0.0:{PORTS} ...")
    s = Server(PORTS)
    s.run()
    print("[Servidor] Encerrado.")
