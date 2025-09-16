import cv2
import socket
import time
import struct
CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 9999
CHUNK_SIZE = 65500 
VIDEO_PATH = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4' 
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_addr = (CLIENT_IP, CLIENT_PORT)
    print(f"Streaming video to {CLIENT_IP}:{CLIENT_PORT}")
    try:
        vid = cv2.VideoCapture(VIDEO_PATH)
        if not vid.isOpened():
            print(f"Error: Could not open video file at {VIDEO_PATH}")
            return
    except Exception as e:
        print(f"Error opening video capture: {e}")
        return
    fps = vid.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 / fps if fps > 0 else 0.033
    print(f"Video FPS: {fps:.2f}, Frame Interval: {frame_interval:.4f}s")
    try:
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                print("End of video stream.")
                break
            frame = cv2.resize(frame, (640, 480))
            result, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not result:
                continue
            
            data = buffer.tobytes()
            data_size = len(data)
            num_chunks = (data_size // CHUNK_SIZE) + 1

            for i in range(num_chunks):
                start = i * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = data[start:end]
                marker = 1 if i == num_chunks - 1 else 0
                header = struct.pack('!B', marker)
                message = header + chunk
                server_socket.sendto(message, client_addr)
            time.sleep(frame_interval)
    finally:
        print("Closing resources.")
        vid.release()
        server_socket.close()
if __name__ == "__main__":
    main()