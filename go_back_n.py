import random
import time

# Adjustable parameters
TOTAL_FRAMES = 10       # total frames to send
WINDOW_SIZE = 4         # number of frames in one window
LOSS_PROBABILITY = 0.2  # 20% chance frame lost
TIMEOUT = 2             # seconds

def go_back_n_arq():
    print("---- Go-Back-N ARQ Simulation ----\n")
    base = 0  # first frame in the window

    while base < TOTAL_FRAMES:
        # Determine frames to send in this window
        end = min(base + WINDOW_SIZE, TOTAL_FRAMES)
        print(f"Sending frames {base} to {end - 1}")

        # Simulate sending each frame
        loss_happened = False
        lost_frame = None
        for frame in range(base, end):
            if random.random() < LOSS_PROBABILITY:
                print(f"Frame {frame} lost ❌")
                loss_happened = True
                lost_frame = frame
                break  # stop checking further (Go-Back-N rule)
            else:
                time.sleep(0.5)  # simulate small delay
                print(f"Frame {frame} sent successfully")

        # If any frame lost, retransmit all from the lost one
        if loss_happened:
            print(f"Timeout! Retransmitting frames {lost_frame} to {end - 1}\n")
            time.sleep(TIMEOUT)
            base = lost_frame  # go back to lost frame
        else:
            # Simulate ACK reception
            ack = end - 1
            time.sleep(1)
            print(f"ACK {ack} received ✅\n")
            base = end  # slide window forward

    print("All frames sent and acknowledged successfully!")

if __name__ == "__main__":
    go_back_n_arq()
