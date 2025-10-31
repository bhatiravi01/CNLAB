from ip_utils import ip_to_binary, get_network_prefix

class Router:
    def __init__(self, routes):
        self.forwarding_table = self.build_forwarding_table(routes)
    
    def build_forwarding_table(self, routes):
        table = []
        for cidr, link in routes:
            prefix_bin = get_network_prefix(cidr)
            table.append((prefix_bin, link))
        table.sort(key=lambda x: len(x[0]), reverse=True)
        return table
    
    def route_packet(self, dest_ip: str) -> str:
        dest_bin = ip_to_binary(dest_ip)
        for prefix_bin, link in self.forwarding_table:
            if dest_bin.startswith(prefix_bin):
                return link
        return "Default Gateway"

if __name__ == "__main__":
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    r = Router(routes)
    
    print(r.route_packet("223.1.1.100"))  # Link 0
    print(r.route_packet("223.1.2.5"))    # Link 1
    print(r.route_packet("223.1.250.1"))  # Link 4 (ISP)
    print(r.route_packet("198.51.100.1")) # Default Gateway
