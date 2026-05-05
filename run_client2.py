import pickle
from client   import *
from dbclient import *
from constRPC import *

if __name__ == "__main__":
    print(f"[Cliente 2] Iniciando na porta {PORTC2} ...")
    c2 = Client(PORTC2)

    print("[Cliente 2] Aguardando stub do Cliente 1 ...")
    data = c2.recvAny()
    dbC2 = pickle.loads(data)
    print("[Cliente 2] Stub recebido. Inserindo 'Client 2' na mesma lista remota.")
    dbC2.appendData('Client 2')

    print("[Cliente 2] Lista final no servidor:", dbC2.getValue())

    print(f"[Cliente 2] Enviando STOP ao servidor ({HOSTS}:{PORTS}).")
    c2.sendTo(HOSTS, PORTS, [STOP])
    print("[Cliente 2] Encerrado.")
