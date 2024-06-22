import socket
class PortScan():
    def __init__(self):
        self.target_ip = ""
        self.target_ports = set()
    
    def get_target_ip(self):
        target = input("Enter target IP or domain name to scan: ")
        try:
            target_ip = socket.gethostbyname(target)
            self.target_ip = target_ip
        except socket.gaierror as e:
            print(f"Error resolving hostname '{target}': {e}")
            return
        
    # need input validation
    def get_target_ports(self):
        user_defined_ports = input("Enter target ports to scan (seperate numbers and ranges by comma): ").split(',')
        for port in user_defined_ports:
            if '-' in port:
                start, end = map(int, port.split('-'))
                self.target_ports.update(range(start, end + 1))
            else:
                self.target_ports.add(int(port.strip()))
    
    def scan(self):
        for port in self.target_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(.1)  # Set timeout for socket connection
            result = sock.connect_ex((self.target_ip, port))
            if result == 0:
                print(f"Port {port} is open")
                sock.close()
                continue
            print(f"Port {port} is closed")
            sock.close()
            
                
    def run(self):
        self.get_target_ip()
        self.get_target_ports()
        self.scan()
                
