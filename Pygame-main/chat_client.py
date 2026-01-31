import socket
import threading

HOST = "127.0.0.1"
PORT = 5051

def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode().strip())
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "q":
            break
        sock.sendall(msg.encode())

    sock.close()

if __name__ == "__main__":
    main()
