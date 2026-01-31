import socket, json, threading, uuid
from entities import Bounds, NPC
from server_game_engine import ServerGameEngine

HOST, PORT = "0.0.0.0", 5050

def send(sock, obj):
    sock.sendall((json.dumps(obj) + "\n").encode())

def recv(sock):
    buf = b""
    while True:
        data = sock.recv(4096)
        if not data:
            return
        buf += data
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            yield json.loads(line)

def main():
    bounds = Bounds(0, 0, 100, 100)
    npcs = [
        NPC(20, 20, 2, 1),
        NPC(80, 70, -2, 2),
        NPC(40, 80, 1, -2),
    ]

    engine = ServerGameEngine(bounds, npcs)
    clients = {}

    def broadcast(state):
        dead = []
        for pid, c in clients.items():
            try:
                send(c, {"type": "state", "state": state})
            except:
                dead.append(pid)
        for pid in dead:
            clients.pop(pid, None)
            engine.remove_player(pid)

    def client_loop(sock, pid):
        send(sock, {"type": "id", "id": pid})
        for msg in recv(sock):
            if msg["type"] == "input":
                engine.set_input(pid, set(msg["keys"]))
        sock.close()
        clients.pop(pid, None)
        engine.remove_player(pid)

    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()

    threading.Thread(target=lambda: engine.run(broadcast), daemon=True).start()

    while True:
        sock, _ = s.accept()
        pid = uuid.uuid4().hex[:6]
        clients[pid] = sock
        engine.add_player(pid)
        threading.Thread(target=client_loop, args=(sock, pid), daemon=True).start()

if __name__ == "__main__":
    main()
