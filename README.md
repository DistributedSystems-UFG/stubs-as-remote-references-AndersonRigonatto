[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/TPGyf4AW)

# Stubs como Referências Remotas em RPC

Exemplo da Nota 4.8 (Tanenbaum & van Steen, 2025, Figs. 4.20 (a)–(d)) adaptado para execução em três máquinas distintas (instâncias EC2 na AWS).

---

## Estrutura dos arquivos

| Arquivo | Papel |
|---|---|
| `constRPC.py` | Constantes do protocolo (códigos de operação) e endereços/portas das três máquinas. |
| `server.py`   | Classe `Server`: aceita requisições `CREATE`, `APPEND`, `GETVALUE`, `STOP` sobre um conjunto de listas em memória. |
| `dbclient.py` | Classe `DBClient` — o **stub** que serve como referência remota a uma lista no servidor. |
| `client.py`   | Classe `Client`: comunicação ponto-a-ponto entre clientes (envio/recepção do stub). |
| `run.py`      | Execução local em uma única máquina via `multiprocessing` (parte **a**). |
| `run_server.py`  | Inicializa o servidor — máquina 1 (parte **b**). |
| `run_client1.py` | Inicializa o Cliente 1 — máquina 2 (parte **b**). |
| `run_client2.py` | Inicializa o Cliente 2 — máquina 3 (parte **b**). |

---

## Parte (a) — Execução local

Em uma única máquina, todos os processos são criados via `multiprocessing` e se comunicam por `localhost`:

```bash
python3 run.py
```

Saída esperada (impressa pelo Cliente 2):

```
['Client 1', 'Client 2']
```

---

## Parte (b) — Execução distribuída na AWS

### 1. Topologia

Três instâncias EC2 (Amazon Linux 2023 ou Ubuntu) na **mesma VPC default** (`172.31.0.0/16`):

| Papel    | IP privado (default VPC) | Porta TCP |
|---       |---                       |---        |
| Servidor | `172.31.16.42`           | `50004`   |
| Cliente 1| `172.31.20.118`          | `50053`   |
| Cliente 2| `172.31.24.205`          | `50054`   |

> Os IPs privados ficam estáveis enquanto a instância existir e o tráfego intra-VPC dispensa NAT/Internet Gateway.

### 2. Security Groups

Para permitir o tráfego entre as instâncias dentro da VPC, crie **regras de entrada (Inbound)** TCP em cada Security Group, com origem o próprio Security Group (ou o CIDR `172.31.0.0/16`):

- Servidor: TCP **50004**
- Cliente 1: TCP **50053**
- Cliente 2: TCP **50054**
- Todas: TCP **22** (SSH a partir do seu IP) para acesso administrativo

### 3. Provisionamento e cópia do código

Em cada instância, após o SSH (`ssh -i chave.pem ec2-user@<ip-publico>`):

```bash
sudo yum install -y git python3   # (no Ubuntu: sudo apt install -y git python3)
git clone https://github.com/DistributedSystems-UFG/stubs-as-remote-references-AndersonRigonatto.git
cd stubs-as-remote-references-AndersonRigonatto
```

### 4. Ordem de execução

A ordem importa porque tanto `Server.__init__` quanto `Client.recvAny` fazem `accept()` bloqueante:

```bash
# Máquina do Servidor:
python3 run_server.py

# Máquina do Cliente 2 (precisa estar pronto antes do Cliente 1 enviar o stub):
python3 run_client2.py

# Máquina do Cliente 1:
python3 run_client1.py
```

### 5. Saída esperada no Cliente 2

```
[Cliente 2] Iniciando na porta 50054 ...
[Cliente 2] Aguardando stub do Cliente 1 ...
[Cliente 2] Stub recebido. Inserindo 'Client 2' na mesma lista remota.
[Cliente 2] Lista final no servidor: ['Client 1', 'Client 2']
[Cliente 2] Enviando STOP ao servidor (172.31.16.42:50004).
[Cliente 2] Encerrado.
```

---

## Mudanças em relação à versão original (parte c, resumida)

1. **Bind em `0.0.0.0`** em `Server` e `Client` (antes: `'localhost'`), permitindo que sockets aceitem conexões de qualquer interface da EC2.
2. **`SO_REUSEADDR`** habilitado para evitar `Address already in use` ao reiniciar processos.
3. **`constRPC.py`** passa a carregar IPs privados reais das três instâncias.
4. Substituição do orquestrador `run.py` (multiprocessing) por **três scripts independentes**, um por máquina, já que não há mais fork local nem acesso compartilhado a memória.
5. **Buffer de recepção** em `dbclient.py` ampliado de `1024` para `4096` bytes, prevenindo truncagem de listas maiores na resposta de `GETVALUE`.
