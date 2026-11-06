import socket
import time
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.0.10"
SOCKET_PORT = 30002

rtde_r = RTDEReceiveInterface(ROBOT_IP)

def send_urscript(cmd_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((ROBOT_IP, SOCKET_PORT))
        s.sendall((cmd_str + "\n").encode("utf-8"))

# Read current position
start_pose = rtde_r.getActualTCPPose()
print(f"Start Pose (mm): X={start_pose[0]*1000:.2f}, Y={start_pose[1]*1000:.2f}, Z={start_pose[2]*1000:.2f}")

# Copy the pose and overwrite Rx, Ry, Rz to make it perfectly parallel to the ground
flat_pose = list(start_pose)
# flat_pose[0] = # x
# flat_pose[1] = # y
# flat_pose[2] = # z
flat_pose[3] = -2.2214  # Rx
flat_pose[4] = 2.2214   # Ry
flat_pose[5] = 0.0      # Rz

print("Moving to level J6 (parallel to ground plane)...")
cmd_level = f"movel(p[{flat_pose[0]:.6f}, {flat_pose[1]:.6f}, {flat_pose[2]:.6f}, {flat_pose[3]:.6f}, {flat_pose[4]:.6f}, {flat_pose[5]:.6f}], a=0.1, v=0.05)"
send_urscript(cmd_level)
time.sleep(2.0) 

# Verify the final orientation
level_pose = rtde_r.getActualTCPPose()
print(f"Leveled Pose: Rx={level_pose[3]:.4f}, Ry={level_pose[4]:.4f}, Rz={level_pose[5]:.4f}")

rtde_r.disconnect()