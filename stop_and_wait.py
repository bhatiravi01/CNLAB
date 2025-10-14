import random
import time

# Simulation parameters
TOTAL_FRAMES = 5        # number of frames to send
LOSS_PROBABILITY = 0.3  # 30% chance frame is lost
TIMEOUT = 2             # seconds

def send_frame(frame_no):
    print(f"Sending Frame {frame_no}")

    # Simulate frame loss
    if random.random() < LOSS_PROBABILITY:
        print(f"Frame {frame_no} lost, retransmitting ...")
        time.sleep(TIMEOUT)
        send_frame(frame_no)
        return

    # Simulate ACK delay or loss
    time.sleep(1)
    if random.random() < LOSS_PROBABILITY:
        print(f"ACK {frame_no} lost, retransmitting Frame {frame_no} ...")
        time.sleep(TIMEOUT)
        send_frame(frame_no)
        return

    # Successful transmission
    print(f"ACK {frame_no} received\n")

def stop_and_wait_arq():
    print("---- Stop and Wait ARQ Simulation ----\n")
    for frame_no in range(TOTAL_FRAMES):
        send_frame(frame_no)
    print("All frames sent and acknowledged successfully!")

if __name__ == "__main__":
    stop_and_wait_arq()
