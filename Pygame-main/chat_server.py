import socket
import threading

HOST = "0.0.0.0"
PORT = 5051

messages = []
clients = []
next_client_id = 1
lock = threading.Lock()

def handle_client(conn, addr):
    global next_client_id

    with lock:
        client_id = next_client_id
        next_client_id += 1
        clients.append(client_id)

    conn.sendall(f"Your ID is {client_id}\n".encode())

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode().strip()
            if not text:
                continue

            with lock:
                need_to_send = [cid for cid in clients if cid != client_id]
                messages.append({
                    "from": client_id,
                    "text": text,
                    "need_to_send": need_to_send
                })

            with lock:
                outgoing = []
                for m in messages:
                    if client_id in m["need_to_send"]:
                        outgoing.append(f'From {m["from"]}: {m["text"]}')
                        m["need_to_send"].remove(client_id)

            if outgoing:
                conn.sendall(("\n".join(outgoing) + "\n").encode())
            else:
                conn.sendall(b"No new messages for you for now!\n")

    finally:
        with lock:
            if client_id in clients:
                clients.remove(client_id)
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Chat server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()

if __name__ == "__main__":
    main()
