import socket, json, threading, pygame
from pygame_backend import PygameInputSystem, PygameGraphicsEngine
from entities import Bounds

HOST, PORT = "127.0.0.1", 5050

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

state = None
pid = None

def main():
    global state, pid

    sock = socket.socket()
    sock.connect((HOST, PORT))

    def reader():
        global state, pid
        for msg in recv(sock):
            if msg["type"] == "id":
                pid = msg["id"]
            if msg["type"] == "state":
                state = msg["state"]

    threading.Thread(target=reader, daemon=True).start()

    inp = PygameInputSystem()
    bounds = Bounds(0, 0, 100, 100)
    gfx = PygameGraphicsEngine(bounds)

    clock = pygame.time.Clock()

    while True:
        keys, quit_ = inp.scan_keys()
        if quit_:
            break
        send(sock, {"type": "input", "keys": list(keys)})

        if state:
            gfx.screen.fill((30, 30, 30))
            for n in state["npcs"]:
                pygame.draw.circle(gfx.screen, (0, 120, 255),
                                   gfx._map(n["x"], n["y"]), int(n["r"]))
            for i, p in state["players"].items():
                col = (255, 0, 0) if i == pid else (0, 255, 0)
                pygame.draw.circle(gfx.screen, col,
                                   gfx._map(p["x"], p["y"]), int(p["radius"]))
            pygame.display.flip()

        clock.tick(60)

    sock.close()
    gfx.close()

if __name__ == "__main__":
    main()
