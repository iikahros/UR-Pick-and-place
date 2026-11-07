import socket
import time
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.0.10"
SOCKET_PORT = 30002

# --- 1. Generate the Chessboard Dictionary ---
A1_X = -452.80
A1_Y = 683.07
Z_HEIGHT = 464.21
SQUARE_SIZE =57.2

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

board_positions = {}
for file_idx, file_letter in enumerate(files):
    for rank_idx, rank_number in enumerate(ranks):
        # Rank 1->8 moves in the +x direction
        x = A1_X + (rank_idx * SQUARE_SIZE)
        # File a->h moves in the -y direction
        y = A1_Y - (file_idx * SQUARE_SIZE)
        
        square_name = f"{file_letter}{rank_number}"
        
        # stores as meters
        board_positions[square_name] = {
            'x': round(x / 1000, 5),
            'y': round(y / 1000, 5),
            'z': round(Z_HEIGHT / 1000, 5)
        }

# communication
def send_urscript(cmd_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((ROBOT_IP, SOCKET_PORT))
        s.sendall((cmd_str + "\n").encode("utf-8"))

# --- 3. Connect and Get Initial Orientation ---
print("connecting")
rtde_r = RTDEReceiveInterface(ROBOT_IP)
start_pose = rtde_r.getActualTCPPose()

# constant tcp angle
rx, ry, rz = start_pose[3], start_pose[4], start_pose[5]

print("ready")
print("-" * 30)

# loop
try:
    while True:
        # user input
        target_square = input("Enter a square (ex: e4), q to quit: ").strip().lower()
        
        if target_square == 'q':
            print("closing.")
            break
            
        if target_square not in board_positions:
            print(f"invalid target: '{target_square}'. Enter something between a1 to h8.")
            continue
            
        # target coords
        pos = board_positions[target_square]
        x, y, z = pos['x'], pos['y'], pos['z']
        
        print(f"Moving to {target_square.upper()} -> X:{x:.4f}, Y:{y:.4f}, Z:{z:.4f}")
        
        # movel
        cmd = f"movel(p[{x:.6f}, {y:.6f}, {z:.6f}, {rx:.6f}, {ry:.6f}, {rz:.6f}], a=0.1, v=0.1)"
        send_urscript(cmd)
        
        # wait to complete move
        time.sleep(2.5) 

except KeyboardInterrupt:
    print("\nclosing")
finally:
    rtde_r.disconnect()
    print("disconnected.")