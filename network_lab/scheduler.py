from dataclasses import dataclass

@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int  # 0 = High, 1 = Medium, 2 = Low

def fifo_scheduler(packet_list: list) -> list:
    return packet_list

def priority_scheduler(packet_list: list) -> list:
    return sorted(packet_list, key=lambda p: p.priority)

if __name__ == "__main__":
    packets = [
        Packet("A", "B", "Data Packet 1", 2),
        Packet("A", "B", "Data Packet 2", 2),
        Packet("A", "B", "VOIP Packet 1", 0),
        Packet("A", "B", "Video Packet 1", 1),
        Packet("A", "B", "VOIP Packet 2", 0)
    ]

    fifo_result = [p.payload for p in fifo_scheduler(packets)]
    priority_result = [p.payload for p in priority_scheduler(packets)]

    print("FIFO order:", fifo_result)
    print("Priority order:", priority_result)
