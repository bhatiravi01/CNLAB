

def ip_to_binary(ip_address: str) -> str:
    octets = ip_address.split(".")
    binary_octets = [bin(int(o))[2:].zfill(8) for o in octets]
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    ip, prefix_len = ip_cidr.split("/")
    prefix_len = int(prefix_len)
    binary_ip = ip_to_binary(ip)
    return binary_ip[:prefix_len]

if __name__ == "__main__":
    print(ip_to_binary("192.168.1.1"))
    print(get_network_prefix("200.23.16.0/23"))
