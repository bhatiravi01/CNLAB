# client.py
import socket
import sys

# --- CONFIG ---
CLIENT_NAME = "Client of Ravindra"  # <-- replace YourFullName
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000

def recv_line(sock):
    data = b""
    while True:
        chunk = sock.recv(1)
        if not chunk:
            return None
        if chunk == b'\n':
            break
        data += chunk
    return data.decode('utf-8', errors='replace')

def run():
    global SERVER_HOST, SERVER_PORT
    if len(sys.argv) >= 2:
        SERVER_HOST = sys.argv[1]
    if len(sys.argv) >= 3:
        SERVER_PORT = int(sys.argv[2])

    # input integer
    while True:
        try:
            n = int(input("Enter an integer between 1 and 100: ").strip())
            break
        except ValueError:
            print("Please enter a valid integer.")

    # send to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print("Failed to connect to server:", e)
        return

    # send client name and number (each followed by newline)
    message = f"{CLIENT_NAME}\n{n}\n"
    s.sendall(message.encode('utf-8'))

    # wait for reply
    server_name = recv_line(s)
    server_num_str = recv_line(s)
    s.close()

    if server_name is None or server_num_str is None:
        print("No reply or incomplete reply from server.")
        return

    try:
        server_num = int(server_num_str.strip())
    except ValueError:
        print("Server sent non-integer.")
        return

    print("\n--- Received Reply ---")
    print("Client's name:", CLIENT_NAME)
    print("Server's name:", server_name)
    print("Client's integer:", n)
    print("Server's integer:", server_num)
    print("Sum:", n + server_num)

if __name__ == "__main__":
    run()
