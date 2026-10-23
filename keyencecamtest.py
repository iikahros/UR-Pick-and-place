import socket

KEYENCE_IP = "192.168.0.69"
KEYENCE_PORT = 8500

def get_keyence_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        s.connect((KEYENCE_IP, KEYENCE_PORT))
        s.sendall(b"TRG\r")
        
        buffer = ""
        data_line = ""
        while True:
            chunk = s.recv(1024).decode("ascii")
            if not chunk:
                break
            buffer += chunk
            lines = [line.strip() for line in buffer.split("\r") if line.strip()]
            
            if len(lines) >= 2:
                data_line = lines[1]
                break
            elif len(lines) == 1 and "," in lines[0]:
                data_line = lines[0]
                break

        parts = data_line.split(",")
        judgment = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        theta = float(parts[3])
        
        return judgment, x, y, theta

if __name__ == "__main__":
    judgment, x, y, theta = get_keyence_data()
    status = "PASS" if judgment == 1 else "FAIL"
    print(f"Judgment: {status} | X: {x:.3f} | Y: {y:.3f} | Theta: {theta:.3f}")