import random
import matplotlib.pyplot as plt

# Simulation parameters
TOTAL_ROUNDS = 30       # number of transmission rounds
LOSS_PROBABILITY = 0.15 # 15% chance of packet loss
INITIAL_SSTHRESH = 8    # slow start threshold

def tcp_congestion_control():
    cwnd = 1
    ssthresh = INITIAL_SSTHRESH
    cwnd_history = []

    print("---- TCP Congestion Control Simulation ----\n")

    for round_no in range(1, TOTAL_ROUNDS + 1):
        print(f"Round {round_no}: cwnd = {cwnd:.2f}", end=" ")

        # Simulate random packet loss
        if random.random() < LOSS_PROBABILITY:
            print("❌ Packet loss detected!")
            ssthresh = max(cwnd / 2, 1)
            cwnd = 1  # reset to 1 (Slow Start again)
            print(f"→ Timeout! ssthresh set to {ssthresh:.2f}, cwnd reset to {cwnd}\n")
        else:
            print("✅ ACK received")
            # Growth behavior based on phase
            if cwnd < ssthresh:
                # Slow Start phase (exponential)
                cwnd *= 2
                print("→ Slow Start: cwnd doubled")
            else:
                # Congestion Avoidance phase (linear)
                cwnd += 1
                print("→ Congestion Avoidance: cwnd increased linearly")

        cwnd_history.append(cwnd)

    # Plot congestion window evolution
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, TOTAL_ROUNDS + 1), cwnd_history, marker='o')
    plt.title("TCP Congestion Control: cwnd vs Transmission Round")
    plt.xlabel("Transmission Round")
    plt.ylabel("Congestion Window (cwnd)")
    plt.grid(True)
    plt.savefig("cwnd_plot.png")
    plt.show()

    print("\nSimulation complete. Plot saved as 'cwnd_plot.png'.")

if __name__ == "__main__":
    tcp_congestion_control()
