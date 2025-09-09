# server.py
import socket
import sys
import random

# --- CONFIG ---
SERVER_NAME = "Server of Ravindra"   # <-- replace YourFullName
HOST = "0.0.0.0"    # listen on all interfaces (change to "127.0.0.1" if needed)
PORT = 6000         # use port > 5000

def recv_line(conn):
    """Receive bytes until newline, return decoded string without newline."""
    data = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        if chunk == b'\n':
            break
        data += chunk
    return data.decode('utf-8', errors='replace')

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    # receive client name
    client_name = recv_line(conn)
    if client_name is None:
        print("Client closed connection immediately.")
        return False
    # receive client number
    client_num_str = recv_line(conn)
    if client_num_str is None:
        print("Client closed connection before sending number.")
        return False

    # parse number
    try:
        client_num = int(client_num_str.strip())
    except ValueError:
        print("Received non-integer from client. Closing.")
        return False

    print("Received from client:")
    print("  Client's name:", client_name)
    print("  Server's name:", SERVER_NAME)
    print("  Client's integer:", client_num)

    # check range
    if not (1 <= client_num <= 100):
        print("Client sent integer outside 1-100. Server will close and terminate.")
        # per assignment: close all sockets and terminate
        conn.close()
        return "TERMINATE"

    # pick server integer (fixed or random)
    server_num = random.randint(1, 100)
    total = client_num + server_num
    print("  Server's integer:", server_num)
    print("  Sum:", total)

    # send response: server name newline server number newline
    response = f"{SERVER_NAME}\n{server_num}\n"
    conn.sendall(response.encode('utf-8'))
    conn.close()
    return True

def run():
    global HOST, PORT
    # allow overriding host/port from command line
    if len(sys.argv) >= 2:
        HOST = sys.argv[1]
    if len(sys.argv) >= 3:
        PORT = int(sys.argv[2])

    print(f"Starting server on {HOST}:{PORT} ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Server listening. Press Ctrl+C to stop.")

    try:
        while True:
            conn, addr = s.accept()
            result = handle_client(conn, addr)
            if result == "TERMINATE":
                print("Terminating server as requested.")
                break
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")
    finally:
        s.close()
        print("Server sockets closed. Exiting.")

if __name__ == "__main__":
    run()

