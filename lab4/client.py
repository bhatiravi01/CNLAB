import cv2
import socket
import numpy as np
import struct

LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 9999
BUFFER_SIZE = 65536 

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((LISTEN_IP, LISTEN_PORT))
    print(f"Listening for video stream on {LISTEN_IP}:{LISTEN_PORT}")

    frame_buffer = b''

    try:
        while True:
            packet, _ = client_socket.recvfrom(BUFFER_SIZE)
            if not packet:
                continue

            header = struct.unpack('!B', packet[:1])[0]
            chunk = packet[1:]
            frame_buffer += chunk

            if header == 1:
                try:
                    np_arr = np.frombuffer(frame_buffer, dtype=np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        cv2.imshow("Video Stream", frame)
                    frame_buffer = b''
                except Exception as e:
                    print(f"Error decoding frame: {e}")
                    frame_buffer = b'' 
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        print("Closing socket and windows.")
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
