from time     import sleep
from client   import *
from dbclient import *
from constRPC import *

if __name__ == "__main__":
    print(f"[Cliente 1] Iniciando na porta {PORTC1} ...")
    c1 = Client(PORTC1)

    print(f"[Cliente 1] Solicitando criação de lista a {HOSTS}:{PORTS} ...")
    dbC1 = DBClient(HOSTS, PORTS)
    listID = dbC1.create()
    print(f"[Cliente 1] Lista criada (id={listID}). Inserindo 'Client 1'.")
    dbC1.appendData('Client 1')

    sleep(3)  # garante que o Cliente 2 já esteja em recvAny()
    print(f"[Cliente 1] Enviando stub para Cliente 2 em {HOSTC2}:{PORTC2} ...")
    c1.sendTo(HOSTC2, PORTC2, dbC1)
    print("[Cliente 1] Encerrado.")
